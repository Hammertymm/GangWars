/* Event popup presentation for Gang Wars.
   This module does not own game state; callers provide modal/render hooks. */
(function(root){
  const EV_IMG = {
    feds:     'events/the_feds.jpg',
    mugging:  'events/ambushed_rolled.jpg',
    find:     'events/dead_drop.jpg',
    gun:      'events/packing_iron.jpg',
    stash:    'events/upgrade_available.jpg',
    shortage: 'events/shortage.jpg',
    frenzy:   'events/buying_frenzy.jpg',
    flood:    'events/flooded_market.jpg',
    celeb:    'events/super_rare_event.jpg',
    intel:    'events/rare_event_intel.jpg',
    bigdaddy: 'cards/big-daddy-j.jpg',
  };

  function create(ctx){
    const app = ctx.app;
    const render = ctx.render;
    const audioPlay = ctx.audioPlay;
    const bindModalCard = ctx.bindModalCard;
    const versionEventImage = ctx.versionEventImage;
    const setModal = ctx.setModal;
    const clearModal = ctx.clearModal;
    const setModalEscape = ctx.setModalEscape;

    function eventImgSrc(imgKeyOrPath){
      if (typeof imgKeyOrPath === 'string' && imgKeyOrPath.includes('/')) return versionEventImage(imgKeyOrPath);
      return versionEventImage(EV_IMG[imgKeyOrPath] || EV_IMG.intel);
    }

    function fitEventPopupToImage(src){
      const popup = app.querySelector(".ev-popup");
      const left = popup && popup.querySelector(".ev-left");
      if (!popup || !left || !src){ if (popup) popup.classList.add("ev-ready"); return; }
      popup.classList.add("ev-measuring");
      const reveal = ()=>{ popup.classList.remove("ev-measuring"); popup.classList.add("ev-ready"); };
      const fit = (naturalWidth, naturalHeight)=>{
        if (naturalWidth && naturalHeight){
          const leftWidth = left.getBoundingClientRect().width || popup.getBoundingClientRect().width / 2;
          const maxHeight = Math.floor(window.innerHeight * 0.88);
          const imageHeight = Math.round(leftWidth * naturalHeight / naturalWidth);
          popup.style.height = `${Math.min(imageHeight, maxHeight)}px`;
        }
        reveal();
      };
      const img = new Image();
      img.onload = ()=>fit(img.naturalWidth, img.naturalHeight);
      img.onerror = reveal;
      img.src = src;
      if (img.complete && img.naturalWidth) fit(img.naturalWidth, img.naturalHeight);
    }

    function showEvent(imgKey, body, btn, cb){
      setModal(function(){
        audioPlay("sfx.events.modalOpen");
        const imgSrc = eventImgSrc(imgKey);
        app.innerHTML=`<div class="modal"><div class="ev-popup" role="dialog" aria-modal="true">
          <div class="ev-left" style="background-image:url('${imgSrc}')" role="img" aria-label="Event illustration"></div>
          <div class="ev-right">
            <div class="ev-body"><div>${body}</div></div>
            <div class="ev-acts"><button class="amber full" id="ok">${btn||'OK'}</button></div>
          </div>
        </div></div>`;
        fitEventPopupToImage(imgSrc);
        const advance = ()=>{ audioPlay("sfx.events.modalClose"); clearModal(); cb(); };
        document.getElementById("ok").onclick=advance;
        setModalEscape(advance);
      });
      render();
    }

    function showTierEvent(imgKey, title, desc, cb){
      setModal(function(){
        audioPlay("sfx.events.modalOpen");
        const imgSrc = eventImgSrc(imgKey);
        app.innerHTML=`<div class="modal modal-event"><div class="ev-tier" role="dialog" aria-modal="true" aria-label="${title}">
          <div class="ev-tier-head">
            <div class="ev-tier-title">${title}</div>
            <div class="ev-tier-desc">${desc}</div>
          </div>
          <div class="ev-tier-art"><img src="${imgSrc}" alt="" decoding="async"></div>
          <div class="ev-tier-acts"><button class="amber full" id="ok">NEXT</button></div>
        </div></div>`;
        const advance = ()=>{ audioPlay("sfx.events.modalClose"); clearModal(); cb(); };
        document.getElementById("ok").onclick=advance;
        setModalEscape(advance);
      });
      render();
    }

    function showEventAsk(imgKey, body, yesLabel, onYes, noLabel, onNo){
      setModal(function(){
        audioPlay("sfx.events.modalOpen");
        const imgSrc = eventImgSrc(imgKey);
        app.innerHTML=`<div class="modal"><div class="ev-popup" role="dialog" aria-modal="true">
          <div class="ev-left" style="background-image:url('${imgSrc}')" role="img" aria-label="Event illustration"></div>
          <div class="ev-right">
            <div class="ev-body"><div>${body}</div></div>
            <div class="ev-acts">
              <button class="amber full" id="yes">${yesLabel}</button>
              <button class="full" id="no">${noLabel}</button>
            </div>
          </div>
        </div></div>`;
        fitEventPopupToImage(imgSrc);
        const yes = ()=>{ audioPlay("sfx.events.modalClose"); clearModal(); onYes(); };
        const pass = ()=>{ audioPlay("sfx.events.modalClose"); clearModal(); onNo(); };
        document.getElementById("yes").onclick=yes;
        document.getElementById("no").onclick=pass;
        setModalEscape(pass);
      });
      render();
    }

    function toast(title, body, btn, cb){
      setModal(function(){
        app.innerHTML=`<div class="modal"><div class="card" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <h2 id="modal-title">${title}</h2><p>${body}</p>
          <button class="full amber" id="ok">${btn||"OK"}</button>
        </div></div>`;
        bindModalCard(app.querySelector(".card"));
        document.getElementById("ok").onclick=()=>{ clearModal(); cb(); };
      });
      render();
    }

    return {
      eventImgSrc,
      fitEventPopupToImage,
      showEvent,
      showTierEvent,
      showEventAsk,
      toast,
    };
  }

  const api = { EV_IMG, create };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.GangWarsEventUI = api;
})(typeof window !== "undefined" ? window : globalThis);
