/* Travel destination picker for Gang Wars. */
(function(root){
  const DISTRICT_IMG = {
    "Little Italy":       "assets/little-italy.jpg",
    "Dock #13":           "assets/dock-13.jpg",
    "Kitty Kat Club":     "assets/kitty-kat-club.jpg",
    "Uptown":             "assets/uptown.jpg",
    "Warehouse":          "assets/warehouse-district.jpg",
    "City Hall":          "assets/city-hall.jpg",
  };

  function create(ctx){
    const app = ctx.app;
    const render = ctx.render;
    const setModal = ctx.setModal;

    function renderTravel(locations, currentLocation, onTravel, onCancel){
      setModal(function(){
        app.innerHTML = `<div class="play scores-play travel-play" role="dialog" aria-modal="true" aria-labelledby="travel-title">
          <div class="scores-hero">
            <div class="scores-hero-title">
              <span class="eos-orn-line"></span>
              <span class="scores-hero-text" id="travel-title">ON THE MOVE</span>
              <span class="eos-orn-line r"></span>
            </div>
          </div>
          <div class="scores-lb-wrap travel-list">
          ${locations.map(l=>{
            const here = l === currentLocation;
            return `<button type="button" class="slb-row travel-row${here?' here':''}" data-go="${l}" ${here?'disabled aria-disabled="true"':''} aria-label="${here?'Current location: ':'Travel to '}${l}">
              <span class="travel-thumb"><img src="${DISTRICT_IMG[l]}" alt="" decoding="async" onerror="this.onerror=null;this.style.display='none'"></span>
              <span class="travel-row-name">${l}</span>
              ${here?'<span class="travel-here-badge">HERE</span>':'<span class="travel-chev" aria-hidden="true">&rsaquo;</span>'}
            </button>`;
          }).join("")}
          </div>
          <div class="scores-foot travel-foot">
            <div class="travel-cost-note">Moving costs you a day</div>
            <button type="button" class="full" id="cancel">GO BACK</button>
          </div>
        </div>`;
        app.querySelectorAll("[data-go]:not([disabled])").forEach(b=> b.onclick=()=> onTravel(b.dataset.go));
        document.getElementById("cancel").onclick=onCancel;
      });
      render();
    }

    return { renderTravel };
  }

  const api = { DISTRICT_IMG, create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.GangWarsTravelUI = api;
})(typeof window !== "undefined" ? window : globalThis);
