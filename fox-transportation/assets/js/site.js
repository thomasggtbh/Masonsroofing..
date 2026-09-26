/* Fox Transportation · interactions. Vanilla JS, no dependencies. */
(() => {
  const doc = document.documentElement;
  const rmQuery = matchMedia('(prefers-reduced-motion: reduce)');
  let reduced = rmQuery.matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ease = t => 1 - Math.pow(1 - t, 3);

  /* ---------- Year ---------- */
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ---------- Nav ---------- */
  const nav = document.querySelector('[data-nav]');
  const toggle = document.querySelector('[data-nav-toggle]');
  const panel = document.querySelector('[data-nav-panel]');
  const setMenu = open => {
    toggle.setAttribute('aria-expanded', String(open));
    panel.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };
  if (toggle && panel) {
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    panel.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
    addEventListener('keydown', e => {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
    });
    matchMedia('(min-width: 901px)').addEventListener('change', e => { if (e.matches) setMenu(false); });
  }

  /* ---------- Reveals ---------- */
  const revealEls = document.querySelectorAll('[data-reveal], [data-reveal-lines], [data-reveal-rule], .reason');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-in'));
  }

  /* ---------- Counters ---------- */
  const counters = document.querySelectorAll('[data-count]');
  const fmt = (n, plain) => plain ? String(n) : n.toLocaleString('en-US');
  if ('IntersectionObserver' in window && !reduced) {
    const cio = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        const el = en.target, end = +el.dataset.count, plain = 'plain' in el.dataset;
        const start = plain ? end - 35 : 0, t0 = performance.now(), dur = 1600;
        const tick = now => {
          const p = clamp((now - t0) / dur);
          el.textContent = fmt(Math.round(start + (end - start) * ease(p)), plain);
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.6 });
    counters.forEach(el => cio.observe(el));
  }

  /* ---------- Map drawing helpers ---------- */
  const maps = [...document.querySelectorAll('[data-map]')];
  const mapParts = maps.map(m => ({
    root: m,
    roads: [...m.querySelectorAll('.road')],
    ring: m.querySelector('[data-ring]'),
    pin: m.querySelector('[data-pin]'),
    outs: [...m.querySelectorAll('.out-draw')],
    heads: [...m.querySelectorAll('[data-end]')],
    labels: [...m.querySelectorAll('.out-label')],
  }));
  const setRoads = (mp, p) => mp.roads.forEach((r, i) => {
    const local = clamp(p * 1.6 - i * 0.05);
    r.style.strokeDasharray = r.classList.contains('road--minor') ? '' : '1';
    if (!r.classList.contains('road--minor')) r.style.strokeDashoffset = String(1 - ease(local));
    else r.style.opacity = String(0.55 * local);
  });
  const setRing = (mp, p) => {
    const e = ease(clamp(p));
    mp.ring.style.transformOrigin = '442px 250px';
    mp.ring.style.transform = `scale(${0.08 + 0.92 * e})`;
    mp.ring.style.opacity = String(clamp(p * 3));
  };
  const setPin = (mp, p) => {
    const e = ease(clamp(p));
    mp.pin.style.opacity = String(clamp(p * 2));
    mp.pin.setAttribute('transform', `translate(348 ${242 - 40 * (1 - e)})`);
  };
  const setOuts = (mp, p) => {
    mp.outs.forEach((o, i) => {
      const local = ease(clamp(p * 1.4 - i * 0.08));
      o.style.strokeDasharray = '1';
      o.style.strokeDashoffset = String(1 - local);
    });
    mp.heads.forEach((h, i) => { h.style.opacity = String(clamp((p * 1.4 - i * 0.08 - 0.85) * 8)); });
    mp.labels.forEach(l => { l.style.opacity = String(clamp((p - 0.55) * 3)); });
  };
  const finalMap = mp => { setRoads(mp, 1); setRing(mp, 1); setPin(mp, 1); setOuts(mp, 1); };

  /* Non-hero maps: draw once when seen */
  mapParts.forEach(mp => {
    if (reduced || !('IntersectionObserver' in window)) { finalMap(mp); return; }
    setRoads(mp, 0); setRing(mp, 0); setPin(mp, 0); setOuts(mp, 0);
    const o = new IntersectionObserver(([en]) => {
      if (!en.isIntersecting) return;
      o.disconnect();
      const t0 = performance.now();
      const run = now => {
        const t = (now - t0) / 2600;
        setRoads(mp, clamp(t / 0.45)); setPin(mp, clamp((t - 0.3) / 0.2));
        setRing(mp, clamp((t - 0.4) / 0.3)); setOuts(mp, clamp((t - 0.6) / 0.4));
        if (t < 1) requestAnimationFrame(run);
      };
      requestAnimationFrame(run);
    }, { threshold: 0.3 });
    o.observe(mp.root);
  });

  /* ---------- Hero: scroll-scrubbed video (10K engineering standard) ---------- */
  const scrub = document.querySelector('[data-scrub]');
  if (scrub) {
    // These five strings match the CSS @media list in site.css exactly.
    const STATIC_GATES = [
      '(max-width: 720px)',
      '(orientation: portrait) and (max-width: 1024px)',
      '(orientation: portrait) and (pointer: coarse)',
      '(orientation: landscape) and (pointer: coarse) and (max-height: 560px)',
      '(prefers-reduced-motion: reduce)'
    ];
    const MQLS = STATIC_GATES.map(q => matchMedia(q));
    const video = scrub.querySelector('[data-video]');
    const still = scrub.querySelector('[data-still]');
    const ring = scrub.querySelector('[data-ring-load]');
    const cue = scrub.querySelector('[data-cue]');
    const VIDEO_URL = scrub.dataset.video;
    const POSTER_URL = scrub.dataset.poster;
    const ENDING_URL = scrub.dataset.ending;
    const VIDEO_BYTES = +scrub.dataset.bytes || 7000000;
    const smoothstep = (p, e0, e1) => { const t = clamp((p - e0) / (e1 - e0)); return t * t * (3 - 2 * t); };

    // Split titles into word spans once, with seeded thresholds (identical every load).
    const rng = seed => { let s = seed >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; };
    scrub.querySelectorAll('[data-split]').forEach((el, n) => {
      const r = rng(17 + n);
      const label = el.textContent.replace(/\s+/g, ' ').trim();
      const words = [];
      const walk = (node, into) => {
        node.childNodes.forEach(c => {
          if (c.nodeType === 3) {
            c.textContent.split(/(\s+)/).forEach(part => {
              if (!part) return;
              if (/^\s+$/.test(part)) { into.appendChild(document.createTextNode(' ')); return; }
              const w = document.createElement('span'); w.className = 'w'; w.textContent = part;
              into.appendChild(w); words.push(w);
            });
          } else if (c.nodeType === 1) {
            const clone = c.cloneNode(false); into.appendChild(clone); walk(c, clone);
          }
        });
      };
      const vis = document.createElement('span'); vis.setAttribute('aria-hidden', 'true');
      walk(el, vis);
      words.forEach((w, i) => w.style.setProperty('--th', (i / words.length * 0.4 + r() * 0.05).toFixed(3)));
      const sr = document.createElement('span'); sr.className = 'sr-only'; sr.textContent = label;
      el.textContent = ''; el.append(sr, vis);
    });

    const bands = [...scrub.querySelectorAll('[data-band]')].map((el, i, all) => ({
      el, a: +el.dataset.a, b: +el.dataset.b, ramp: +el.dataset.ramp || 0,
      first: i === 0, last: i === all.length - 1, op: -1, k: -1, on: null
    }));

    let scrubOn = false, heroOnScreen = true, inited = false;
    let target = 0, shown = 0, rafId = null, lastTick = 0, loadK = 0, loadStart = 0;
    let seekBusy = false, pendingTime = null;

    const heroProgress = () => {
      const r = scrub.getBoundingClientRect();
      const span = scrub.offsetHeight - (innerHeight - (nav ? nav.offsetHeight : 0));
      return span > 0 ? clamp(-r.top / span) : 0;
    };

    function requestSeek(t) {
      if (!video.duration || !isFinite(t)) return;
      if (seekBusy) { pendingTime = t; return; }
      seekBusy = true;
      video.currentTime = Math.min(t, video.duration - 0.001);
    }
    video.addEventListener('seeked', () => {
      seekBusy = false;
      if (pendingTime !== null) { const t = pendingTime; pendingTime = null; requestSeek(t); }
    });
    video.addEventListener('error', () => { seekBusy = false; pendingTime = null; failVideo(); });

    function updateCaptions(p) {
      bands.forEach(b => {
        const f = Math.min(0.02, (b.b - b.a) / 3);
        const inO = b.first ? 1 : smoothstep(p, b.a, b.a + f);
        const outO = b.last ? 1 : 1 - smoothstep(p, b.b - f, b.b);
        const op = p < b.a - 0.0001 && !b.first ? 0 : (p > b.b && !b.last ? 0 : inO * outO);
        const rampLen = b.ramp || Math.min(0.025, (b.b - b.a) * 0.35);
        let k = clamp((p - b.a) / rampLen);
        if (b.first) k = Math.max(k, loadK);
        if (Math.abs(op - b.op) > 0.004) { b.el.style.opacity = op.toFixed(3); b.op = op; }
        if (Math.abs(k - b.k) > 0.008 || (k === 1 && b.k !== 1)) { b.el.style.setProperty('--k', k.toFixed(3)); b.k = k; }
        const on = op > 0.5;
        if (on !== b.on) { b.el.classList.toggle('is-active', on); b.on = on; }
      });
      if (cue) { const o = p > 0.03 ? '0' : '1'; if (cue.style.opacity !== o) cue.style.opacity = o; }
    }

    function tick(now) {
      const dt = Math.min(100, now - (lastTick || now));
      lastTick = now;
      if (loadK < 1) loadK = ease(clamp((now - loadStart) / 1400));
      shown += (target - shown) * (1 - Math.pow(1 - 0.16, dt / 16.667));
      const settled = Math.abs(target - shown) < 0.0005 && loadK >= 1;
      if (settled) shown = target;
      requestSeek(shown * (video.duration || 0));
      updateCaptions(shown);
      if (settled || !heroOnScreen) { rafId = null; lastTick = 0; }
      else rafId = requestAnimationFrame(tick);
    }
    const kick = () => { if (rafId === null && scrubOn) rafId = requestAnimationFrame(tick); };
    function onScroll() { target = heroProgress(); if (heroOnScreen) kick(); }

    function failVideo() {
      scrub.classList.add('video-failed');
      if (ENDING_URL) still.style.backgroundImage = `url("${ENDING_URL}")`;
    }

    let fetchStarted = false;
    async function loadHeroBlob() {
      const ctrl = new AbortController();
      let watchdog = setTimeout(() => ctrl.abort(), 20000);
      const res = await fetch(VIDEO_URL, { priority: 'low', signal: ctrl.signal, mode: 'cors' });
      if (!res.ok || !res.body) throw new Error('video ' + res.status);
      const total = Number(res.headers.get('Content-Length')) || VIDEO_BYTES;
      const reader = res.body.getReader();
      const chunks = [];
      let got = 0, lastRing = 0;
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        clearTimeout(watchdog);
        watchdog = setTimeout(() => ctrl.abort(), 20000);
        chunks.push(value);
        got += value.length;
        const frac = Math.min(1, got / total);
        const t = performance.now();
        if (t - lastRing > 100 || frac === 1) { lastRing = t; ring.style.setProperty('--ld', Math.round(126 * (1 - frac))); }
      }
      clearTimeout(watchdog);
      ring.style.setProperty('--ld', 0);
      video.src = URL.createObjectURL(new Blob(chunks, { type: 'video/mp4' }));
      video.load();
      video.addEventListener('canplay', () => {
        requestSeek(heroProgress() * video.duration);
        scrub.classList.add('video-ready');
      }, { once: true });
    }
    function startBlobFetch() {
      if (fetchStarted || !VIDEO_URL) return;
      fetchStarted = true;
      loadHeroBlob().catch(failVideo);
    }
    function initHeroOnce() {
      if (inited) return;
      inited = true;
      loadStart = performance.now();
      if (POSTER_URL) {
        still.style.backgroundImage = `url("${POSTER_URL}")`;
        const img = new Image();
        img.onload = startBlobFetch; img.onerror = startBlobFetch; img.src = POSTER_URL;
        setTimeout(startBlobFetch, 4000);
      } else startBlobFetch();
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(([en]) => { heroOnScreen = en.isIntersecting; if (heroOnScreen) onScroll(); }).observe(scrub);
      }
    }

    function enableScrub() {
      if (scrubOn) return;
      scrubOn = true;
      initHeroOnce();
      addEventListener('scroll', onScroll, { passive: true });
      bands.forEach(b => { b.op = -1; b.k = -1; b.on = null; b.el.style.removeProperty('opacity'); b.el.style.removeProperty('--k'); });
      target = shown = heroProgress();
      onScroll(); kick();
    }
    function disableScrub() {
      if (scrubOn) { scrubOn = false; removeEventListener('scroll', onScroll); if (rafId !== null) { cancelAnimationFrame(rafId); rafId = null; } }
      // Static hero: the ending frame, with band one composed over it.
      bands.forEach(b => { b.el.style.removeProperty('opacity'); b.el.style.removeProperty('--k'); b.el.classList.remove('is-active'); b.op = b.k = -1; b.on = null; });
      if (ENDING_URL) still.style.backgroundImage = `url("${ENDING_URL}")`;
    }
    const applyHeroMode = () => (MQLS.some(m => m.matches) ? disableScrub() : enableScrub());
    MQLS.forEach(m => m.addEventListener('change', applyHeroMode));
    addEventListener('resize', () => { if (scrubOn) onScroll(); });
    applyHeroMode();
  }

  /* ---------- Equipment configurator ---------- */
  document.querySelectorAll('[data-rig]').forEach(form => {
    const section = form.closest('section');
    const svg = section.querySelector('[data-truck]');
    const rear = section.querySelector('.rig__rear');
    const cap = section.querySelector('[data-rear-cap]');
    const rUnit = section.querySelector('[data-r-unit]');
    const rRear = section.querySelector('[data-r-rear]');
    const rUse = section.querySelector('[data-r-use]');
    const update = () => {
      const unit = form.unit.value, len = +form.len.value, door = form.door.value;
      const straight = unit === 'straight';
      svg.querySelector('[data-unit="tractor"]').style.opacity = straight ? '0' : '1';
      svg.querySelector('[data-unit="straight"]').style.opacity = straight ? '1' : '0';
      form.querySelectorAll('[data-for="tractor"]').forEach(fs => { fs.disabled = straight; fs.style.opacity = straight ? '.4' : '1'; });
      const L = len * 10, delta = (len - 53) * 10;
      svg.querySelectorAll('[data-unit="tractor"] [data-box]').forEach(el => {
        const inset = el.classList.contains('box-ribs') ? 8 : 0;
        el.style.width = (L - inset) + 'px';
      });
      svg.querySelectorAll('[data-unit="tractor"] [data-move]').forEach(el => { el.style.transform = `translateX(${delta}px)`; });
      svg.querySelectorAll('[data-unit="tractor"] [data-half]').forEach(el => { el.style.transform = `translateX(${delta / 2}px)`; });
      svg.querySelector('[data-len]').textContent = `${len} ft trailer`;
      const shownDoor = straight ? 'lift' : door;
      rear.querySelectorAll('[data-door]').forEach(g => { g.style.opacity = g.dataset.door === shownDoor ? '1' : '0'; });
      cap.textContent = straight ? 'Rear view · lift gate' : `Rear view · ${door} ${door === 'swing' ? 'doors' : 'door'}`;
      rUnit.textContent = straight ? 'Straight truck with lift gate' : `${len} ft trailer`;
      rRear.textContent = straight ? 'Lift gate lowers freight to the ground'
        : door === 'swing' ? 'Swing doors, full-width opening' : 'Roll door, lifts straight up';
      rUse.textContent = straight ? 'Curbside and no-dock deliveries'
        : len === 48 ? 'Tighter docks, yards and city streets' : 'Full truckloads to a dock';
    };
    form.addEventListener('change', update);
    update();
  });

  /* ---------- Photo slots ----------
     Drop a real Fox photo into assets/photos/ under the name its slot asks for,
     then list that file here. Slots not listed keep their line drawing. */
  const PHOTOS = [
    // 'terminal.jpg', 'yard.jpg', 'trailer-53.jpg', 'trailer-48.jpg', 'straight-truck.jpg',
  ];
  document.querySelectorAll('[data-photo]').forEach(fig => {
    const src = fig.dataset.photo;
    if (!/^https?:/.test(src) && !PHOTOS.includes(src.split('/').pop())) return;
    const img = new Image();
    img.decoding = 'async';
    img.loading = 'lazy';
    img.alt = fig.dataset.alt || '';
    img.onload = () => { fig.classList.add('has-photo'); requestAnimationFrame(() => img.classList.add('is-loaded')); };
    img.onerror = () => img.remove();
    img.src = fig.dataset.photo;
    fig.prepend(img);
  });

  /* ---------- Parallax on terminal photos + timeline fill ---------- */
  const para = [...document.querySelectorAll('.terminal .photo')];
  const timeline = document.querySelector('[data-timeline]');
  let ticking = false;
  const onScrollFx = () => {
    ticking = false;
    if (reduced) return;
    const vh = innerHeight;
    para.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      const p = (r.top + r.height / 2 - vh / 2) / vh;
      el.style.setProperty('--py', (p * -40).toFixed(1) + 'px');
    });
    if (timeline) {
      const r = timeline.getBoundingClientRect();
      timeline.style.setProperty('--tp', clamp((vh * 0.85 - r.top) / (r.height + vh * 0.3)).toFixed(3));
    }
    if (nav) nav.classList.toggle('is-scrolled', scrollY > 8);
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScrollFx); } }, { passive: true });
  onScrollFx();
  if (nav) nav.classList.toggle('is-scrolled', scrollY > 8);
  if (reduced && timeline) timeline.style.setProperty('--tp', '1');

  /* ---------- Quote form: validate, then compose an email to dispatch ---------- */
  const form = document.querySelector('[data-quote]');
  if (form) {
    const done = form.querySelector('[data-done]');
    let body = '';
    const err = (input, msg) => {
      const e = document.getElementById(input.id + '-e');
      input.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (e) e.textContent = msg || '';
      return !msg;
    };
    const check = () => {
      let ok = true, first = null;
      const need = (el, msg) => { const good = err(el, el.value.trim() ? '' : msg); if (!good) { ok = false; first = first || el; } };
      need(form.pickup, 'Add a pickup city or ZIP.');
      need(form.delivery, 'Add a delivery city or ZIP.');
      need(form.name, 'Add your name.');
      const email = form.email.value.trim(), phone = form.phone.value.trim();
      const emailOk = !email || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      if (!email && !phone) {
        err(form.phone, 'Add a phone number or an email so dispatch can reply.');
        err(form.email, ''); ok = false; first = first || form.phone;
      } else {
        err(form.phone, '');
        if (!err(form.email, emailOk ? '' : 'That email looks incomplete.')) { ok = false; first = first || form.email; }
      }
      if (first) first.focus();
      return ok;
    };
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!check()) return;
      const v = n => (form.elements[n] && form.elements[n].value || '').trim() || '-';
      const radio = n => { const c = form.querySelector(`input[name="${n}"]:checked`); return c ? c.value : '-'; };
      body = [
        `Service: ${radio('service')}`, `Equipment: ${radio('equipment')}`, `Weight / pallets: ${v('weight')}`,
        `Hazmat: ${v('hazmat')}`, '', `Pickup: ${v('pickup')}`, `Delivery: ${v('delivery')}`,
        `Ready date: ${v('date')}`, `Frequency: ${v('frequency')}`, '', `Name: ${v('name')}`,
        `Company: ${v('company')}`, `Phone: ${v('phone')}`, `Email: ${v('email')}`, '', `Notes: ${v('notes')}`,
      ].join('\n');
      const subject = `Quote request: ${v('pickup')} to ${v('delivery')}`;
      location.href = `mailto:dispatch@foxtrans.net?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      form.classList.add('is-sent');
      done.focus();
    });
    form.addEventListener('input', e => { if (e.target.getAttribute('aria-invalid') === 'true') err(e.target, ''); });
    const copy = form.querySelector('[data-copy]');
    if (copy) copy.addEventListener('click', async e => {
      e.preventDefault();
      try { await navigator.clipboard.writeText(body); copy.textContent = 'copied'; }
      catch { copy.textContent = 'copy failed, please call instead'; }
    });
  }

  /* Reduced motion switched on mid-visit: pin everything to its end state. */
  rmQuery.addEventListener('change', e => {
    reduced = e.matches;
    if (!reduced) return;
    revealEls.forEach(el => el.classList.add('is-in'));
    mapParts.forEach(finalMap);
    counters.forEach(el => { el.textContent = fmt(+el.dataset.count, 'plain' in el.dataset); });
    if (timeline) timeline.style.setProperty('--tp', '1');
  });
})();
