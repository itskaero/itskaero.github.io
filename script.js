/* =====================================================================
   KAERO · The Systems Atlas
   ---------------------------------------------------------------------
   1. Chrome        chapter tracking, bar surface, progress, mobile menu
   2. Reveals       one IntersectionObserver for every entrance
   3. Filters       project plates by field
   4. Method        the six-step cycle
   5. Process       manifesto diagram drawn by scroll position
   6. Parallax      hero layers, a few pixels at most
   No libraries. Every part degrades to a finished, static page.
   ===================================================================== */

(function () {
  'use strict';

  var motionOK = window.matchMedia('(prefers-reduced-motion: no-preference)');
  var clamp = function (v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; };
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ═══ 1. CHROME ════════════════════════════════════════════════════ */

  var bar = $('#bar');
  var rail = $('#chapters');
  var progress = $('#progress');
  var nowNum = $('#now-num');
  var nowName = $('#now-name');
  var menuBtn = $('#menu-btn');
  var chapters = $$('main > .ch');
  var railLinks = $$('#chapters a');
  // anything with its own surface colour, in document order
  var surfaces = $$('main > .ch, .plate--dark, .foot');

  function surfaceOf(el) {
    if (el.classList.contains('ch--forest') || el.classList.contains('plate--dark') || el.classList.contains('foot')) return 'forest';
    if (el.classList.contains('ch--charcoal')) return 'charcoal';
    return 'paper';
  }

  // the innermost surface under a given viewport y (dark plates sit inside paper chapters)
  function surfaceAt(y) {
    var hit = null;
    for (var i = 0; i < surfaces.length; i++) {
      var r = surfaces[i].getBoundingClientRect();
      if (r.top <= y && r.bottom > y && !surfaces[i].hidden) hit = surfaces[i];
    }
    return hit ? surfaceOf(hit) : 'paper';
  }

  var current = -1;
  function setChapter(i) {
    if (i === current || i < 0) return;
    current = i;
    var ch = chapters[i];
    if (nowNum) nowNum.textContent = ch.getAttribute('data-chapter');
    if (nowName) nowName.textContent = ch.getAttribute('data-name');
    railLinks.forEach(function (a, n) {
      if (n === i) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }

  var queued = false;
  function frame() {
    queued = false;
    var vh = window.innerHeight;
    var y = window.scrollY || window.pageYOffset || 0;
    var max = document.documentElement.scrollHeight - vh;
    if (progress) progress.style.transform = 'scaleX(' + (max > 0 ? clamp(y / max, 0, 1) : 0).toFixed(4) + ')';

    var probe = vh * 0.4;
    var idx = 0;
    for (var i = 0; i < chapters.length; i++) {
      if (chapters[i].getBoundingClientRect().top <= probe) idx = i;
    }
    setChapter(idx);

    var barH = bar ? bar.offsetHeight : 56;
    if (bar) bar.setAttribute('data-surface', surfaceAt(barH + 1));
    if (rail && !rail.classList.contains('is-open')) rail.setAttribute('data-surface', surfaceAt(vh / 2));

    processFrame(vh);
    parallaxFrame(y, vh);
  }
  function request() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', request, { passive: true });
  addEventListener('resize', request);

  // mobile: the rail becomes a drop-down chapter list
  if (menuBtn && rail) {
    var setOpen = function (open, returnFocus) {
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      rail.classList.toggle('is-open', open);
      if (open) {
        rail.removeAttribute('data-surface');
        var first = rail.querySelector('a');
        if (first) first.focus();
      } else if (returnFocus) {
        menuBtn.focus();
      }
    };
    menuBtn.addEventListener('click', function () {
      setOpen(menuBtn.getAttribute('aria-expanded') !== 'true');
    });
    rail.addEventListener('click', function (e) {
      if (e.target.closest('a') && rail.classList.contains('is-open')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && rail.classList.contains('is-open')) setOpen(false, true);
    });
    document.addEventListener('click', function (e) {
      if (rail.classList.contains('is-open') && !rail.contains(e.target) && !menuBtn.contains(e.target)) setOpen(false);
    });
    // a desktop-width resize must not leave a stranded panel
    window.matchMedia('(min-width: 1180px)').addEventListener('change', function (m) { if (m.matches) setOpen(false); });
  }

  /* ═══ 2. REVEALS ═══════════════════════════════════════════════════ */

  (function reveals() {
    var items = $$('.reveal, .plate, .next, .invite');
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });

    // arriving on a deep link (#nabz, #about…) must not show an empty plate
    if (location.hash) {
      var target = document.getElementById(location.hash.slice(1));
      var plate = target && target.closest ? target.closest('.plate') : null;
      if (plate) plate.classList.add('is-in');
    }
  }());

  /* ═══ 3. FILTERS ═══════════════════════════════════════════════════ */

  (function filters() {
    var buttons = $$('.filter');
    var plates = $$('.plate');
    var status = $('#filter-status');
    var empty = $('#work-empty');
    if (!buttons.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-filter');
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        var shown = 0;
        plates.forEach(function (p) {
          var on = f === 'all' || (' ' + p.getAttribute('data-cats') + ' ').indexOf(' ' + f + ' ') > -1;
          p.hidden = !on;
          if (on) { shown++; p.classList.add('is-in'); }
        });
        if (empty) empty.hidden = shown > 0;
        if (status) status.textContent = 'Showing ' + shown + ' of ' + plates.length + ' projects.';
        request();
      });
    });
  }());

  /* ═══ 4. METHOD ════════════════════════════════════════════════════ */

  (function method() {
    var steps = $$('.step');
    var panels = $$('.sp');
    var nodes = $$('.cy-node');
    var arc = $('#cy-arc');
    var centre = $('#cy-centre');
    if (!steps.length) return;

    function show(i) {
      steps.forEach(function (s, n) { s.setAttribute('aria-pressed', n === i ? 'true' : 'false'); });
      panels.forEach(function (p, n) { p.classList.toggle('is-on', n === i); });
      nodes.forEach(function (g, n) {
        g.classList.toggle('is-on', n === i);
        g.classList.toggle('is-done', n < i);
      });
      if (arc) arc.style.strokeDasharray = Math.max(i, 0.02) + ' 6';
      if (centre) centre.textContent = steps[i].textContent.replace(/^\s*\d+\s*/, '');
    }

    steps.forEach(function (s, i) {
      s.addEventListener('click', function () { show(i); });
      s.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = (i + 1) % steps.length;
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = (i - 1 + steps.length) % steps.length;
        if (n === null) return;
        e.preventDefault();
        steps[n].focus();
        show(n);
      });
    });
    // the diagram is a pointer shortcut; the buttons remain the accessible control
    nodes.forEach(function (g, i) { g.addEventListener('click', function () { show(i); }); });
    show(0);
  }());

  /* ═══ 5. PROCESS ═══════════════════════════════════════════════════ */

  var proc = $('.process');
  var procParts = [];
  if (proc) {
    $$('.pr-line, .pr-dot, .pr-step', proc).forEach(function (el) {
      var x;
      if (el.classList.contains('pr-step')) {
        x = 20 + Number(el.getAttribute('data-step')) * 200 + 100;
      } else {
        try { var b = el.getBBox(); x = b.x + b.width / 2; } catch (e) { x = 0; }
      }
      procParts.push({ el: el, i: clamp(Math.floor((x - 20) / 200), 0, 5), dot: !el.classList.contains('pr-line') });
    });
  }
  var lastP = -1;
  function processFrame(vh) {
    if (!proc || !motionOK.matches) return;
    var r = proc.getBoundingClientRect();
    if (r.bottom < -100 || r.top > vh + 100) return;
    // 0 as the figure enters at the bottom, complete by the time it reaches the upper half
    var p = clamp((vh - r.top) / (vh * 0.6), 0, 1);
    if (Math.abs(p - lastP) < 0.003) return;
    lastP = p;
    procParts.forEach(function (o) {
      var local = clamp(p * 6.6 - o.i, 0, 1);
      if (o.dot) o.el.style.setProperty('--op', local > 0.55 ? '1' : '0');
      else o.el.style.setProperty('--off', (1 - local).toFixed(3));
    });
  }

  /* ═══ 6. PARALLAX ══════════════════════════════════════════════════ */

  var layers = $$('.hero__art .a-strata, .hero__art .a-city, .hero__art .a-tree, .hero__art .a-net');
  var depth = [0.06, 0.1, 0.14, 0.14];
  var heroEl = $('#entering');
  function parallaxFrame(y, vh) {
    if (!layers.length || !motionOK.matches || y > vh * 1.2) return;
    layers.forEach(function (l, i) { l.style.transform = 'translateY(' + (y * depth[i]).toFixed(1) + 'px)'; });
  }
  if (heroEl && layers.length) {
    motionOK.addEventListener('change', function (m) {
      if (!m.matches) layers.forEach(function (l) { l.style.transform = ''; });
      request();
    });
  }

  frame();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(request);
}());
