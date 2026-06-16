/* ============================================================================
   CRIME LEDGER UI — reference PNG base + transparent dynamic overlays only.
   Blueprint: scripts/ledger-blueprint.json (473×1024 canvas)
   ============================================================================ */

const LEDGER_CANVAS = { w: 473, h: 1024 };

const LEDGER_BLUEPRINT = {
  home: {
    baseAsset: "assets/ledger/crime-ledger-home-base.png",
    totalCounter: { x: 130, y: 486, w: 213, h: 18 },
    rowCounters: [
      { id: "general", x: 268, y: 542, w: 92, h: 16 },
      { id: "rare", x: 238, y: 594, w: 92, h: 16 },
      { id: "superRare", x: 318, y: 646, w: 92, h: 16 },
      { id: "godlike", x: 268, y: 698, w: 72, h: 16 },
      { id: "goldenGodlike", x: 368, y: 750, w: 52, h: 16 },
    ],
    rowHits: [
      { id: "general", x: 17, y: 508, w: 439, h: 54 },
      { id: "rare", x: 17, y: 562, w: 439, h: 54 },
      { id: "superRare", x: 17, y: 616, w: 439, h: 54 },
      { id: "godlike", x: 17, y: 670, w: 439, h: 54 },
      { id: "goldenGodlike", x: 17, y: 724, w: 439, h: 54 },
    ],
    back: { x: 20, y: 934, w: 433, h: 48 },
  },
  general: {
    baseAsset: "assets/ledger/ledger-general-base.png",
    scroll: true,
    counter: { x: 60, y: 338, w: 353, h: 28 },
    listPanel: { x: 17, y: 382, w: 439, h: 528 },
    rowHeight: 38,
    back: { x: 20, y: 934, w: 433, h: 48 },
  },
  rare: {
    baseAsset: "assets/ledger/ledger-rare-base.png",
    scroll: false,
    counter: { x: 60, y: 328, w: 353, h: 28 },
    listPanel: { x: 17, y: 382, w: 439, h: 528 },
    rowHeight: 53,
    back: { x: 20, y: 934, w: 433, h: 48 },
  },
  superRare: {
    baseAsset: "assets/ledger/ledger-super-rare-base.png",
    scroll: false,
    counter: { x: 60, y: 328, w: 353, h: 28 },
    listPanel: { x: 17, y: 382, w: 439, h: 528 },
    rowHeight: 53,
    back: { x: 20, y: 934, w: 433, h: 48 },
  },
  godlike: {
    baseAsset: "assets/ledger/ledger-godlike-base.png",
    scroll: false,
    counter: { x: 60, y: 328, w: 353, h: 28 },
    listPanel: { x: 17, y: 382, w: 439, h: 528 },
    rowHeight: 106,
    back: { x: 20, y: 934, w: 433, h: 48 },
  },
  goldenGodlike: {
    baseAsset: "assets/ledger/ledger-golden-godlike-base.png",
    scroll: false,
    counter: { x: 60, y: 388, w: 353, h: 28 },
    listPanel: { x: 17, y: 432, w: 439, h: 478 },
    rowHeight: 72,
    back: { x: 20, y: 934, w: 433, h: 48 },
  },
};

function ledgerRectStyle(r) {
  const { w: W, h: H } = LEDGER_CANVAS;
  return `left:${(r.x / W) * 100}%;top:${(r.y / H) * 100}%;width:${(r.w / W) * 100}%;height:${(r.h / H) * 100}%`;
}

function ledgerCounterHtml(text, rect, cls) {
  return `<div class="ledger-counter${cls ? " " + cls : ""}" style="${ledgerRectStyle(rect)}">${text}</div>`;
}

function ledgerHitStyle(r) {
  return ledgerRectStyle(r);
}

function categoryCounterText(catId, found, total) {
  if (catId === "general") return `${found} / ${total} FOUND`;
  return `${found} OF ${total} DISCOVERED`;
}

function buildListRows(cat, ledger, focusId) {
  const isGeneral = cat.id === "general";
  return cat.achievements.map(a => {
    const unlocked = isUnlocked(ledger, a.id);
    const revealed = isRevealed(ledger, a.id);
    const focus = focusId === a.id ? " reveal-focus" : "";
    let iconCls = "locked";
    let icon = "◆";
    let title = "";
    let mark = "";
    if (revealed) {
      iconCls = "revealed";
      icon = "★";
      title = a.title;
      if (unlocked) mark = "✓";
    } else if (isGeneral) {
      title = "???";
    } else {
      title = "UNKNOWN";
    }
    const titleCls = revealed ? "" : " hidden";
    return `<div class="ledger-list-row${focus}" data-aid="${a.id}">
      <span class="ledger-row-icon ${iconCls}">${icon}</span>
      <div class="ledger-row-copy"><div class="ledger-row-title${titleCls}">${title}</div></div>
      <span class="ledger-row-mark">${mark}</span>
    </div>`;
  }).join("");
}

function ledgerShell(baseAsset, innerHtml, backRect) {
  const { w, h } = LEDGER_CANVAS;
  return `<div class="play ledger-play"><div class="ledger-art-screen"><div class="ledger-art-frame">
    <img src="${baseAsset}" width="${w}" height="${h}" decoding="async" alt="">
    <div class="ledger-overlay-layer">${innerHtml}</div>
    <button type="button" class="ledger-hit" id="ledgerBack" aria-label="Back" style="${ledgerHitStyle(backRect)}"></button>
  </div></div></div>`;
}

function runRevealAnimation(el, fullText, onDone) {
  const chars = fullText.length;
  const steps = Math.max(chars, 1);
  const duration = Math.min(1000, Math.max(500, chars * 35));
  const stepMs = duration / steps;
  let i = 0;
  el.textContent = "???";
  el.classList.add("hidden");
  el.closest(".ledger-list-row")?.classList.add("reveal-focus");
  const tick = () => {
    i++;
    const shown = Math.ceil((i / steps) * chars);
    el.textContent = fullText.slice(0, shown) + "?".repeat(Math.max(0, chars - shown));
    if (i >= steps) {
      el.textContent = fullText;
      el.classList.remove("hidden");
      const row = el.closest(".ledger-list-row");
      const markEl = row?.querySelector(".ledger-row-mark");
      if (markEl) markEl.textContent = "✓";
      const iconEl = row?.querySelector(".ledger-row-icon");
      if (iconEl) {
        iconEl.textContent = "★";
        iconEl.classList.remove("locked");
        iconEl.classList.add("revealed");
      }
      onDone();
      return;
    }
    setTimeout(tick, stepMs);
  };
  setTimeout(tick, stepMs);
}

const LedgerUI = {
  renderHome(app, ctx) {
    const bp = LEDGER_BLUEPRINT.home;
    const found = countDiscovered(ctx.ledger);
    const counters = ledgerCounterHtml(`${found} / ${LEDGER_TOTAL} FOUND`, bp.totalCounter, "total");
    const rowParts = bp.rowCounters.map(rc => {
      const cat = LEDGER_CATEGORIES.find(c => c.id === rc.id);
      const n = countUnlocked(ctx.ledger, rc.id);
      return ledgerCounterHtml(`${n} / ${cat.achievements.length}`, rc, "row");
    }).join("");
    const hits = bp.rowHits.map(rh => {
      const cat = LEDGER_CATEGORIES.find(c => c.id === rh.id);
      return `<button type="button" class="ledger-hit" data-cat="${rh.id}" aria-label="${cat.title}" style="${ledgerHitStyle(rh)}"></button>`;
    }).join("");
    app.innerHTML = ledgerShell(bp.baseAsset, counters + rowParts + hits, bp.back);
    bp.rowHits.forEach(rh => {
      const btn = app.querySelector(`[data-cat="${rh.id}"]`);
      if (btn) btn.onclick = () => ctx.onOpenCategory(rh.id);
    });
    document.getElementById("ledgerBack").onclick = ctx.onBackHome;
  },

  renderCategory(app, catId, ctx) {
    const cat = LEDGER_CATEGORIES.find(c => c.id === catId);
    const bp = LEDGER_BLUEPRINT[catId];
    if (!cat || !bp) {
      ctx.onBackHome();
      return;
    }
    const found = countUnlocked(ctx.ledger, catId);
    const rows = buildListRows(cat, ctx.ledger, ctx.focusId);
    const scrollCls = bp.scroll ? " scroll" : "";
    const panelStyle = ledgerRectStyle(bp.listPanel);
    const inner = ledgerCounterHtml(categoryCounterText(catId, found, cat.achievements.length), bp.counter, "cat")
      + `<div class="ledger-list-panel${scrollCls}" style="${panelStyle}">`
      + `<div class="ledger-list-inner" style="--row-h:${bp.rowHeight}px">${rows}</div></div>`;
    app.innerHTML = ledgerShell(bp.baseAsset, inner, bp.back);
    document.getElementById("ledgerBack").onclick = ctx.onBackCategory;
    if (ctx.focusId && isUnlocked(ctx.ledger, ctx.focusId) && !isRevealed(ctx.ledger, ctx.focusId) && catId === "general") {
      const row = app.querySelector(`[data-aid="${ctx.focusId}"] .ledger-row-title`);
      if (row) {
        runRevealAnimation(row, getAchievementTitle(ctx.focusId), () => {
          revealAchievement(ctx.ledger, ctx.focusId);
          ctx.onRevealComplete();
        });
      }
    } else if (ctx.focusId) {
      const row = app.querySelector(`[data-aid="${ctx.focusId}"]`);
      if (row) row.scrollIntoView({ block: "nearest" });
    }
  },

  render(app, ctx) {
    if (ctx.view === "category" && ctx.catId) {
      this.renderCategory(app, ctx.catId, ctx);
    } else {
      this.renderHome(app, ctx);
    }
  },
};

if (typeof module !== "undefined") {
  module.exports = { LedgerUI, LEDGER_BLUEPRINT, LEDGER_CANVAS };
}
