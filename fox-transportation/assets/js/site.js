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
  mapParts.filter(mp => !mp.root.hasAttribute('data-hero-map')).forEach(mp => {
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

  /* ---------- Hero: scroll-driven route ---------- */
  const hero = document.querySelector('[data-hero]');
  if (hero) {
    const mp = mapParts.find(m => m.root.hasAttribute('data-hero-map'));
    const beats = [...hero.querySelectorAll('[data-beat]')];
    const progs = [...hero.querySelectorAll('[data-prog]')];
    const progLabel = hero.querySelector('[data-prog-label]');
    const cue = hero.querySelector('[data-cue]');
    const labels = ['Terminal', '45-mile ring', 'Beyond'];
    let intro = 0, target = 0, shown = -1, lastBeat = -1, rafId = 0, running = false, isStatic = false;

    const staticGate = () => reduced || innerWidth < 900 || innerHeight < 600 || matchMedia('(pointer: coarse)').matches;

    const render = p => {
      // p: 0..1 across the pinned hero. Roads come from the intro; scroll owns the rest.
      setRoads(mp, intro);
      setPin(mp, clamp(intro * 1.4 - 0.4));
      setRing(mp, clamp((p - 0.18) / 0.3));
      setOuts(mp, clamp((p - 0.55) / 0.35));
      const b = p < 0.3 ? 0 : p < 0.62 ? 1 : 2;
      if (b !== lastBeat) {
        beats.forEach((el, i) => el.classList.toggle('is-on', i === b));
        progLabel.textContent = labels[b];
        lastBeat = b;
      }
      progs.forEach((el, i) => el.style.setProperty('--p', clamp(p * 3 - i).toFixed(3)));
      cue.style.opacity = p > 0.04 ? '0' : '1';
    };

    const measure = () => {
      const r = hero.getBoundingClientRect();
      const span = hero.offsetHeight - innerHeight;
      return span > 0 ? clamp(-r.top / span) : 0;
    };

    const loop = () => {
      const diff = target - shown;
      if (Math.abs(diff) < 0.0005 && intro >= 1) { shown = target; render(shown); running = false; return; }
      shown += diff * 0.14;
      if (intro < 1) intro = Math.min(1, intro + 0.012);
      render(shown);
      rafId = requestAnimationFrame(loop);
    };
    const kick = () => { if (!running && !isStatic) { running = true; rafId = requestAnimationFrame(loop); } };
    const onScroll = () => { if (isStatic) return; target = measure(); kick(); };

    const setMode = () => {
      const s = staticGate();
      if (s === isStatic && shown !== -1) return;
      isStatic = s;
      hero.classList.toggle('is-static', s);
      cancelAnimationFrame(rafId); running = false;
      if (s) {
        beats.forEach(el => el.classList.add('is-on'));
        finalMap(mp);
        shown = 1;
      } else {
        lastBeat = -1;
        target = measure();
        shown = target;
        kick();
      }
    };
    setMode();
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', setMode);
    rmQuery.addEventListener('change', e => { reduced = e.matches; setMode(); });
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
    if (!PHOTOS.includes(fig.dataset.photo.split('/').pop())) return;
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
