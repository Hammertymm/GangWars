const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const {
  CONFIG, DRUG, DRUGS, HOME, LOCATIONS, RARE_EVENTS, SUPER_RARE_EVENTS,
  rollMarket, buy, sell, newGame, migrateSave, resolveTravelMarket,
  bankBorrow, bankRepay, avgCost, profitPct, applyTerritoryPrice,
  TERRITORY_MODIFIERS, FAM_LUXURY,
} = require('./engine.js');

describe('rollMarket', () => {
  it('returns prices for all goods at a location', () => {
    const { prices } = rollMarket(HOME);
    assert.equal(Object.keys(prices).length, DRUGS.length);
  });

  it('applies Uptown luxury bonus to diamonds', () => {
    const base = 100000;
    const d = DRUG.diamonds;
    const uptown = applyTerritoryPrice(d, 'Uptown', base);
    const home = applyTerritoryPrice(d, HOME, base);
    assert.ok(uptown > home);
    assert.equal(uptown, Math.round(base * (1 + TERRITORY_MODIFIERS.Uptown.luxuryBonus)));
  });

  it('widens variance at Dock #13', () => {
    const samples = Array.from({ length: 40 }, () => rollMarket('Dock #13').prices.bathgin).filter(Boolean);
    const homeSamples = Array.from({ length: 40 }, () => rollMarket(HOME).prices.bathgin).filter(Boolean);
    const dockSpread = Math.max(...samples) - Math.min(...samples);
    const homeSpread = Math.max(...homeSamples) - Math.min(...homeSamples);
    assert.ok(dockSpread >= homeSpread);
  });
});

describe('buy / sell', () => {
  it('tracks cost basis and profit', () => {
    const s = newGame();
    s.prices.bathgin = 100;
    s.cash = 1000;
    assert.equal(buy(s, 'bathgin', 5), null);
    assert.equal(avgCost(s, 'bathgin'), 100);
    s.prices.bathgin = 150;
    assert.equal(profitPct(s, 'bathgin', 150), 50);
    assert.equal(sell(s, 'bathgin', 2), null);
    assert.equal(s.inventory.bathgin, 3);
  });
});

describe('bank', () => {
  it('enforces borrow cap', () => {
    const s = newGame();
    assert.match(bankBorrow(s, CONFIG.maxBorrow + 1), /won't lend/);
    assert.equal(bankBorrow(s, 1000), null);
    assert.equal(s.cash, CONFIG.startCash + 1000);
  });
});

describe('migrateSave', () => {
  it('remaps legacy item ids', () => {
    const s = migrateSave({ inventory: { spices: 3, artwork: 1 }, costBasis: { spices: 50 }, events: {} });
    assert.equal(s.inventory.cigars, 3);
    assert.equal(s.inventory.art, 1);
    assert.equal(s.costBasis.cigars, 50);
  });
});

describe('RARE_EVENTS', () => {
  it('every entry has a district and commodity', () => {
    for (const re of RARE_EVENTS) {
      assert.ok(re.district, `${re.id} missing district`);
      assert.ok(LOCATIONS.includes(re.district), `${re.id} invalid district`);
      assert.ok(re.commodity && DRUG[re.commodity], `${re.id} invalid commodity`);
    }
  });
});

describe('resolveTravelMarket', () => {
  it('applies rare spike only in matching district on event day', () => {
    const re = RARE_EVENTS[0];
    const s = newGame();
    s.day = 10;
    s.events.rare = { ...re, day: 10 };
    const wrong = resolveTravelMarket(s, HOME);
    const right = resolveTravelMarket(s, re.district);
    assert.notEqual(wrong.prices[re.commodity], right.prices[re.commodity]);
    assert.ok(right.prices[re.commodity] >= DRUG[re.commodity].low * 3);
  });

  it('applies godlike x10 only in matching district', () => {
    const s = newGame();
    s.day = 12;
    s.events.godlike = { lines: ['A', 'B'], day: 12, district: 'Uptown' };
    s.prices = rollMarket(HOME).prices;
    const elsewhere = resolveTravelMarket(s, HOME);
    const uptown = resolveTravelMarket(s, 'Uptown');
    const ids = DRUGS.map(d => d.id).filter(id => elsewhere.prices[id] && uptown.prices[id]);
    assert.ok(ids.length > 0);
    const id = ids[0];
    assert.ok(uptown.prices[id] >= elsewhere.prices[id] * 5);
  });

  it('applies super rare x3 in matching district', () => {
    const sr = SUPER_RARE_EVENTS[0];
    const rand = Math.random;
    Math.random = () => 0.42;
    try {
      const s = newGame();
      s.day = 8;
      s.events.superRare = { ...sr, day: 8 };
      const withEvent = resolveTravelMarket(s, sr.district);
      delete s.events.superRare;
      const without = resolveTravelMarket(s, sr.district);
      const id = DRUGS.find(d => withEvent.prices[d.id] && without.prices[d.id])?.id;
      assert.ok(id);
      assert.equal(withEvent.prices[id], Math.round(without.prices[id] * 3));
    } finally {
      Math.random = rand;
    }
  });
});

describe('newGame', () => {
  it('starts at home with rolled prices', () => {
    const s = newGame();
    assert.equal(s.location, HOME);
    assert.equal(s.day, 1);
    assert.ok(s.prices.bathgin != null || s.prices.cigars != null);
  });
});
