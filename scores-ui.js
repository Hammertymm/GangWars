/* Scoreboard helpers for Gang Wars.
   Kept framework-free so the app can remain a static classic-script PWA. */
(function(root){
  function sortHighscores(hs){
    return (Array.isArray(hs) ? hs : [])
      .slice()
      .sort((a, b) => b.worth - a.worth || String(a.date || "").localeCompare(String(b.date || "")));
  }

  function scoreEntryMatch(a, b){
    return a && b && a.worth === b.worth && a.score === b.score && a.date === b.date;
  }

  function defaultLeaderboardRows(ranks){
    const seeds = [50000000,45000000,40000000,35000000,30000000,25000000,20000000,15000000,10000000,5000000];
    return [...ranks].reverse().map((rank, i) => ({ rank, worth: seeds[i], isDefault: true }));
  }

  function buildTop10Leaderboard(hs, ranks, getRank){
    const seeds = defaultLeaderboardRows(ranks);
    if (!hs || !hs.length) return seeds;
    const real = sortHighscores(hs).map(entry => ({ rank: getRank(entry.worth), worth: entry.worth, isDefault: false, entry }));
    const combined = [...real, ...seeds].sort((a, b) => b.worth - a.worth || (a.isDefault ? 1 : -1));
    return combined.slice(0, 10);
  }

  function rankPortrait(rank){
    const r = rank.toLowerCase().replace(/ /g,'-');
    return `cards/${r}-portrait.jpg`;
  }

  function mkScoresLbRow(row, pos, isYou, formatMoney){
    return `<div class="slb-row${isYou ? ' you' : ''}">
      <span class="slb-pos">${pos}.</span>
      <img class="slb-portrait" src="${rankPortrait(row.rank)}" alt="${row.rank}">
      <span class="slb-rank">${row.rank.toUpperCase()}</span>
      <span class="slb-score">${formatMoney(row.worth)}</span>
      ${isYou ? '<span class="slb-you">&larr; YOU</span>' : ''}
    </div>`;
  }

  const api = {
    sortHighscores,
    scoreEntryMatch,
    defaultLeaderboardRows,
    buildTop10Leaderboard,
    rankPortrait,
    mkScoresLbRow,
  };

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.GangWarsScoresUI = api;
})(typeof window !== "undefined" ? window : globalThis);
