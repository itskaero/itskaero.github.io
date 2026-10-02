/* =====================================================================
   itskaero.github.io
   ---------------------------------------------------------------------
   1. Liquid card carousel  — spring position, velocity-driven stretch
                              and directional blur, depth by distance
   2. Accent sync           — the active card re-tints the whole page
   3. Page motion           — scroll reveals, word statement, nav state
   ===================================================================== */

(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clamp = function (v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; };

  /* ═══ 1. LIQUID CAROUSEL ═══════════════════════════════════════════ */

  (function carousel() {
    var vp = document.getElementById('lq');
    var track = document.getElementById('lq-track');
    if (!vp || !track) return;

    var cards = Array.prototype.slice.call(track.children);
    if (!cards.length) return;

    var rail = document.getElementById('lq-rail');
    var prevBtn = document.getElementById('lq-prev');
    var nextBtn = document.getElementById('lq-next');
    var counter = document.getElementById('lq-cur');

    var index = 0;        // active card
    var pos = 0;          // rendered track offset
    var goal = 0;         // where the spring is pulling to
    var vel = 0;          // px moved last frame — drives the liquid look
    var raf = null;
    var centers = [];     // offset that centres card i
    var metrics = [];     // cached {left, w} per card
    var half = 0;         // cached viewport midpoint

    /* ── measurement ───────────────────────────────────────────────────
       Geometry is read ONCE here, never inside the frame. Reading
       offsetLeft after writing the track's transform would force a
       synchronous layout on every card on every frame.              */

    function measure() {
      half = vp.clientWidth / 2;
      metrics = cards.map(function (el) {
        return { left: el.offsetLeft, w: el.offsetWidth || 1 };
      });
      centers = metrics.map(function (m) { return half - (m.left + m.w / 2); });
      goal = centers[index];
      if (!dragging) kick();
    }

    function nearest(x) {
      var best = 0, bestD = Infinity;
      for (var i = 0; i < centers.length; i++) {
        var d = Math.abs(centers[i] - x);
        if (d < bestD) { bestD = d; best = i; }
      }
      return best;
    }

    /* ── the frame ─────────────────────────────────────────────────────
       Depth lives on .lq-card, distortion on .lq-card__inner, so the
       two transforms never overwrite each other.                      */

    function render() {
      track.style.transform = 'translate3d(' + pos.toFixed(2) + 'px,0,0)';

      var speed = Math.min(Math.abs(vel), 90);

      // liquid: stretch along travel, squash across it, lean into the turn
      var stretch = reduce ? 0 : Math.min(speed * 0.0024, 0.13);
      var lean = reduce ? 0 : clamp(-vel * 0.05, -5, 5);
      var blur = reduce ? 0 : Math.min(speed * 0.16, 9);

      for (var i = 0; i < cards.length; i++) {
        var el = cards[i];
        var m = metrics[i];
        if (!m) continue;
        var d = (m.left + m.w / 2 + pos - half) / m.w;   // distance in card-widths
        var ad = Math.abs(d);

        // Far cards cost blur passes for nothing, and the viewport mask
        // hides them anyway.
        if (ad > 2.9) {
          if (el.style.visibility !== 'hidden') el.style.visibility = 'hidden';
          continue;
        }
        if (el.style.visibility) el.style.visibility = '';

        var adc = Math.min(ad, 2);
        el.style.transform =
          'translateZ(' + (-adc * 70).toFixed(1) + 'px) ' +
          'rotateY(' + (clamp(-d, -2.4, 2.4) * 8.5).toFixed(2) + 'deg) ' +
          'scale(' + (1 - adc * 0.11).toFixed(4) + ')';
        el.style.opacity = (1 - adc * 0.34).toFixed(3);
        el.style.zIndex = String(100 - Math.round(adc * 10));

        var inner = el.firstElementChild;
        if (!inner) continue;
        inner.style.transform =
          'scaleX(' + (1 + stretch).toFixed(4) + ') ' +
          'scaleY(' + (1 - stretch * 0.7).toFixed(4) + ') ' +
          'skewY(' + lean.toFixed(2) + 'deg)';
        inner.style.filter = blur > 0.3 ? 'blur(' + blur.toFixed(2) + 'px)' : '';
      }
    }

    function loop() {
      var prev = pos;
      pos += (goal - pos) * 0.14;
      vel = pos - prev;

      if (!dragging && Math.abs(goal - pos) < 0.08) {
        pos = goal; vel = 0; render(); raf = null; return;   // settled: sleep
      }
      render();
      raf = requestAnimationFrame(loop);
    }

    function kick() { if (!raf) raf = requestAnimationFrame(loop); }

    /* ── active state ──────────────────────────────────────────────── */

    function setIndex(i) {
      index = clamp(i, 0, cards.length - 1);
      goal = centers[index];

      cards.forEach(function (el, n) {
        var on = n === index;
        el.classList.toggle('is-active', on);
        // Keep invisible neighbour links out of reach of both the
        // pointer and the tab order.
        el.querySelectorAll('.lq-card__links a').forEach(function (a) {
          a.tabIndex = on ? 0 : -1;
          a.style.pointerEvents = on ? '' : 'none';
        });
      });

      // the page takes on the active member's accent
      var accent = cards[index].getAttribute('data-accent');
      if (accent) document.body.setAttribute('data-accent', accent);

      if (counter) counter.textContent = String(index + 1).padStart(2, '0');
      if (prevBtn) prevBtn.disabled = index === 0;
      if (nextBtn) nextBtn.disabled = index === cards.length - 1;
      if (rail) {
        Array.prototype.forEach.call(rail.children, function (b, n) {
          b.setAttribute('aria-current', n === index ? 'true' : 'false');
        });
      }
      kick();
    }

    function go(i) { setIndex(i); }

    /* ── drag ──────────────────────────────────────────────────────────
       The track follows the finger exactly; velocity comes from the
       pointer, not the spring, so the smear matches the gesture.      */

    var dragging = false, startX = 0, startPos = 0, lastX = 0, flick = 0, moved = 0;

    vp.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      dragging = true; moved = 0; flick = 0;
      startX = lastX = e.clientX;
      startPos = pos;
      vp.classList.add('is-dragging');
      try { vp.setPointerCapture(e.pointerId); } catch (err) { /* no capture: fine */ }
    });

    vp.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      flick = e.clientX - lastX;
      lastX = e.clientX;

      var prev = pos;
      // Rubber-band past the ends instead of stopping dead.
      var raw = startPos + dx;
      var lo = centers[centers.length - 1], hi = centers[0];
      if (raw > hi) raw = hi + (raw - hi) * 0.35;
      if (raw < lo) raw = lo + (raw - lo) * 0.35;
      pos = raw;
      vel = pos - prev;
      render();
    });

    function endDrag() {
      if (!dragging) return;
      dragging = false;
      vp.classList.remove('is-dragging');
      // a flick carries past the nearest card
      go(nearest(pos + flick * 6));
    }
    vp.addEventListener('pointerup', endDrag);
    vp.addEventListener('pointercancel', endDrag);

    // A drag that ends over a link must not count as a click on it.
    vp.addEventListener('click', function (e) {
      if (moved > 8) { e.preventDefault(); e.stopPropagation(); moved = 0; return; }
      var card = e.target.closest ? e.target.closest('.lq-card') : null;
      if (!card) return;
      var i = cards.indexOf(card);
      if (i > -1 && i !== index) { e.preventDefault(); go(i); }
    }, true);

    /* ── wheel, keys, focus ────────────────────────────────────────── */

    var wheelLock = 0;
    vp.addEventListener('wheel', function (e) {
      // Only take over for sideways intent; the page keeps vertical scroll.
      var dx = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : (e.shiftKey ? e.deltaY : 0);
      if (!dx) return;
      e.preventDefault();
      if (Date.now() < wheelLock) return;
      wheelLock = Date.now() + 260;
      go(index + (dx > 0 ? 1 : -1));
    }, { passive: false });

    vp.addEventListener('keydown', function (e) {
      var k = e.key;
      if (k === 'ArrowRight') { e.preventDefault(); go(index + 1); }
      else if (k === 'ArrowLeft') { e.preventDefault(); go(index - 1); }
      else if (k === 'Home') { e.preventDefault(); go(0); }
      else if (k === 'End') { e.preventDefault(); go(cards.length - 1); }
    });

    // If focus lands inside a card by any route, bring that card forward.
    vp.addEventListener('focusin', function (e) {
      var card = e.target.closest ? e.target.closest('.lq-card') : null;
      if (!card) return;
      var i = cards.indexOf(card);
      if (i > -1 && i !== index) go(i);
    });

    if (prevBtn) prevBtn.addEventListener('click', function () { go(index - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { go(index + 1); });

    /* ── rail ──────────────────────────────────────────────────────── */

    if (rail) {
      cards.forEach(function (el, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', el.getAttribute('aria-label') || 'Project ' + (i + 1));
        b.addEventListener('click', function () { go(i); });
        rail.appendChild(b);
      });
    }

    /* ── boot ──────────────────────────────────────────────────────── */

    measure();
    pos = goal;
    setIndex(0);
    render();

    var ro = window.ResizeObserver ? new ResizeObserver(measure) : null;
    if (ro) ro.observe(vp); else window.addEventListener('resize', measure);

    // Card widths are clamp()-based, but re-measuring once the display
    // face has loaded costs nothing and avoids a half-pixel drift.
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  }());

  /* ═══ 2. SCROLL REVEALS ════════════════════════════════════════════ */

  (function reveals() {
    var items = document.querySelectorAll('.nama-reveal, .step');
    if (!items.length) return;

    if (!('IntersectionObserver' in window) || reduce) {
      items.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });

    items.forEach(function (el) { io.observe(el); });
  }());

  /* ═══ 3. WORD-BY-WORD STATEMENT ════════════════════════════════════ */

  (function statement() {
    var el = document.getElementById('statement');
    if (!el) return;

    // Split text nodes into words in place, so the <em> survives.
    (function split(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.nodeValue.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var s = document.createElement('span');
            s.className = 'w';
            s.textContent = part;
            frag.appendChild(s);
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1) {
          split(child);
        }
      });
    }(el));

    var words = Array.prototype.slice.call(el.querySelectorAll('.w'));
    if (reduce) { words.forEach(function (w) { w.classList.add('is-on'); }); return; }

    var lit = -1;
    function paint() {
      var r = el.getBoundingClientRect();
      var from = window.innerHeight * 0.88;
      var to = window.innerHeight * 0.3;
      var p = clamp((from - r.top) / (from - to), 0, 1);
      var n = Math.round(p * words.length);
      if (n === lit) return;
      for (var i = 0; i < words.length; i++) words[i].classList.toggle('is-on', i < n);
      lit = n;
    }
    addEventListener('scroll', paint, { passive: true });
    addEventListener('resize', paint);
    paint();
  }());

  /* ═══ 4. NAV STATE + SCROLL PROGRESS ═══════════════════════════════ */

  (function nav() {
    var bar = document.getElementById('nav');
    var prog = document.getElementById('progress');
    if (!bar && !prog) return;

    var queued = false;
    function frame() {
      queued = false;
      var y = window.scrollY || 0;
      if (bar) bar.classList.toggle('is-stuck', y > 24);
      if (prog) {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        prog.style.width = (max > 0 ? (y / max) * 100 : 0).toFixed(2) + '%';
      }
    }
    addEventListener('scroll', function () {
      if (!queued) { queued = true; requestAnimationFrame(frame); }
    }, { passive: true });
    frame();
  }());

}());
