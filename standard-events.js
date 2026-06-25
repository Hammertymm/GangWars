/* Standard non-combat travel events for Gang Wars. */
(function(root){
  function create(ctx){
    const getState = ctx.getState;
    const money = ctx.money;
    const randInt = ctx.randInt;
    const pick = ctx.pick;

    function eventMugging(next){
      const S = getState();
      ctx.emitTipEvent("event:mugging", {});
      const loss = Math.min(S.cash, randInt(50, Math.max(100, Math.round(S.cash * 0.15))));
      S.cash -= loss;
      ctx.logMsg(`Ambushed \u2014 lost ${money(loss)}.`);
      const mugV = pick([
        `A welcoming committee was waiting around the corner. They were fast, organised, and ${money(loss)} richer when they left.`,
        `The beating was free. Stealing ${money(loss)} was business.`,
        `You were robbed of ${money(loss)} by a man pretending to be a lamppost. In hindsight, he was unusually bright.`,
        `Three professionals took ${money(loss)}. "Tell whoever sent you the answer's still no." Nobody sent you.`,
        `A priest heard your confession and left with ${money(loss)}. He definitely wasn't a priest.`,
        `A man representing Big Daddy J collected an "associate fee" of ${money(loss)}. You paid promptly.`,
        `Four men relieved you of ${money(loss)}. The fifth apologised for the inconvenience.`,
        `You were pickpocketed of ${money(loss)} so elegantly you almost checked whether he'd left a receipt.`,
        `A street magician made ${money(loss)} disappear. He then disappeared as well.`,
        `The note simply read: "Mr J appreciates your contribution." The missing ${money(loss)} agreed.`,
      ]);
      ctx.showEvent('mugging', mugV, "DAMN", next);
    }

    function eventFind(next){
      const S = getState();
      if (ctx.spaceLeft(S) <= 0){ next(); return; }
      const d = pick(ctx.GOODS);
      const n = Math.min(ctx.spaceLeft(S), randInt(2, 7));
      S.inventory[d.id] = (S.inventory[d.id] || 0) + n;
      ctx.logMsg(`Dead drop \u2014 picked up ${n} ${d.name}.`);
      const findV = pick([
        `Someone hid ${n} ${d.name} and never returned. You decide waiting would be impolite.`,
        `Whatever went down in that garage on Clark Street, the men who stashed ${n} ${d.name} won't be coming back. You will.`,
        `The Gennas are gone. Their ${n} ${d.name} isn't. You collect the inheritance.`,
        `The chalk outline's still fresh. The ${n} ${d.name} isn't going anywhere.`,
        `A crate of ${n} ${d.name}. A letter signed with one initial. You keep the goods. The fire keeps the letter.`,
        `The hearse is empty. The crate beside it isn't. ${n} ${d.name} has changed addresses.`,
        `The warehouse door stood open. The lock lay beside ${n} ${d.name}. Nobody else was coming back.`,
        `The cloakroom ticket and ${n} ${d.name} was still in the coat. The owner wasn't.`,
        `A warehouse foreman tipped his hat. ${n} ${d.name} is "Already paid for." He wouldn't say by whom.`,
        `A crate bore tomorrow's newspaper. Inside was ${n} ${d.name}. You ignored the headline.`,
      ]);
      ctx.showEvent('find', findV, "NICE", next);
    }

    function eventStash(next){
      const S = getState();
      const { add, cost } = ctx.rollStashUpgrade();
      if (S.cash < cost){ next(); return; }
      const sv = pick([
        `A mechanic studies your vehicle, nods once, and offers +${add} hidden crates for ${money(cost)}.`,
        `A man waves a patent for hidden crates. Genuine or not, he'll add +${add} for ${money(cost)}.`,
        `A blind carpenter measures by touch alone. The +${add} hidden crates fit perfectly. ${money(cost)}.`,
        `"Mr J covered the labour," the mechanic says. You only pay ${money(cost)} for +${add} hidden crates.`,
        `A stranger predicts computers. You settle for +${add} hidden crates instead. Cost: ${money(cost)}.`,
        `An undertaker offers +${add} hidden crates for ${money(cost)}. "Nobody inspects my work twice."`,
        `A locksmith smiles. "Locks keep honest people honest." He adds +${add} hidden crates for ${money(cost)}.`,
        `A theatre illusionist asks where you'd like the cargo to disappear. ${money(cost)} buys +${add} hidden crates.`,
        `A work order already bears your name. Nobody remembers writing it. ${money(cost)} finishes the job.`,
        `A bank vault engineer says your vehicle has "wasted space." ${money(cost)} fixes the problem.`,
      ]);
      ctx.showEventAsk('stash', sv, 'BUY',
        ()=>{ S.cash -= cost; S.space += add; ctx.recordSpaceChange(S); ctx.logMsg(`+${add} stash space.`); ctx.clearModal(); next(); },
        'PASS', ()=>{ ctx.clearModal(); next(); }
      );
    }

    function eventGun(next){
      const S = getState();
      ctx.emitTipEvent("event:gunOffer", {});
      if (S.guns >= ctx.CONFIG.maxGuns){ next(); return; }
      const base = randInt(1500, 2500);
      const cost = ctx.gunEventCost(base, S.guns);
      if (S.cash < cost){ next(); return; }
      const gv = pick([
        `An alley merchant opens a canvas bag just wide enough. Clean piece. ${money(cost)}. No promises.`,
        `A quiet veteran unwraps a well-kept sidearm. "I was hoping never to see it again." ${money(cost)}.`,
        `The piece on the table has a history you don't want to know about. ${money(cost)}, no questions, no paperwork. In this city that's a bargain.`,
        `Ness's men seized it Tuesday. It's for sale again today. ${money(cost)}.`,
        `"Big Daddy prefers his associates breathing." A clean piece costs ${money(cost)}.`,
        `"One day this belongs in a museum," he says. Today it's ${money(cost)}.`,
        `A Pinkerton detective hangs up his badge and slides a clean piece across the table. ${money(cost)}.`,
        `A pawnbroker shrugs. "Nobody pawns happy memories." The piece costs ${money(cost)}.`,
        `A tailor measures your jacket before recommending the firearm. "Fit matters." ${money(cost)}.`,
        `A bartender reaches beneath the counter. "Big Daddy said you might need this." ${money(cost)}.`,
      ]);
      ctx.showEventAsk('gun', gv, 'BUY',
        ()=>{ S.cash -= cost; S.guns += 1; ctx.logMsg(`Bought a gun.`); ctx.clearModal(); next(); },
        'PASS', ()=>{ ctx.clearModal(); next(); }
      );
    }

    return {
      eventMugging,
      eventFind,
      eventStash,
      eventGun,
    };
  }

  const api = { create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.GangWarsStandardEvents = api;
})(typeof window !== "undefined" ? window : globalThis);
