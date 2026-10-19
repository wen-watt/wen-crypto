// wen-crypto.com: falling petals, menu, three-question quiz. No trackers, no external calls.
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // opened from disk (file://): folder links need index.html
  if (location.protocol === 'file:') [].forEach.call(document.querySelectorAll('a[href]'), function (a) {
    var h = a.getAttribute('href');
    if (!/^[a-z]+:/i.test(h) && !/^#/.test(h) && /\/$/.test(h.split('#')[0])) a.setAttribute('href', h.replace(/\/(#|$)/, '/index.html$1'));
  });

  // menu
  var btn = document.querySelector('.menu'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // quiz: answer once, show the fact either way
  [].forEach.call(document.querySelectorAll('.qcard'), function (card) {
    var opts = card.querySelectorAll('.opt'), fact = card.querySelector('.fact');
    [].forEach.call(opts, function (o) {
      o.addEventListener('click', function () {
        var ok = o.getAttribute('data-ok') === '1';
        [].forEach.call(opts, function (x) {
          x.disabled = true;
          if (x.getAttribute('data-ok') === '1') x.classList.add('right');
        });
        if (!ok) o.classList.add('wrong');
        card.classList.add('done', ok ? 'ok' : 'miss');
        if (fact) fact.hidden = false;
      });
    });
  });

  // shorts feed: counter, progress bar, newer/older buttons
  var reel = document.querySelector('.reel');
  if (reel) {
    var cards = reel.querySelectorAll('.reel-item'), count = document.querySelector('.shorts-count span'), bar = document.querySelector('.reel-bar i'), cur = 0;
    function mark(i) { cur = i; if (count) count.textContent = i + 1; if (bar) bar.style.width = ((i + 1) / cards.length * 100) + '%'; }
    mark(0);
    reel.addEventListener('scroll', function () { var i = Math.round(reel.scrollTop / reel.clientHeight); if (i !== cur && i >= 0 && i < cards.length) mark(i); }, { passive: true });
    [].forEach.call(document.querySelectorAll('.shorts-nav [data-dir]'), function (b) {
      b.addEventListener('click', function () {
        var i = Math.max(0, Math.min(cards.length - 1, cur + parseInt(b.getAttribute('data-dir'), 10)));
        reel.scrollTo({ top: i * reel.clientHeight, behavior: reduce ? 'auto' : 'smooth' });
      });
    });
  }

  // dancing cat shadow on the branch: pose keyframes, forward kinematics keeps the standing foot on the branch
  (function () {
    var root = document.getElementById('d-root');
    if (!root) return;
    var $ = function (id) { return document.getElementById(id); };
    var J = { tail: $('d-tail'), lt: $('d-lt'), ls: $('d-ls'), rt: $('d-rt'), rs: $('d-rs'), tor: $('d-tor'),
              la1: $('d-la1'), la2: $('d-la2'), ra1: $('d-ra1'), ra2: $('d-ra2'), head: $('d-head'), staff: $('d-staff') };
    var B = { x: 0, lean: 0, sp: 0, tor: 0, head: 0, lt: 6, ls: 0, rt: -6, rs: 0, la1: 14, la2: -12, ra1: -14, ra2: 12, tail: 30, st: 0, sa: 0, hop: 0 };
    function P(o) { var r = {}; for (var k in B) r[k] = B[k]; for (k in o) r[k] = o[k]; return r; }
    // [pose, seconds to reach it]
    var T = [
      [P({}), .8],
      [P({ x: -4, lean: -6, la1: 30, ra1: -5, tail: 45 }), .5], [P({ x: 4, lean: 6, la1: 5, ra1: -30, tail: 15 }), .5], [P({}), .4],
      // glide backwards: one leg straight and sliding, the other on its toe
      [P({ x: -6, lt: 12, ls: 0, rt: -24, rs: 38, la1: 25, ra1: -40, ra2: 40 }), .45], [P({ x: -12, lt: 24, ls: -38, rt: -10, rs: 0, la1: 40, la2: -40, ra1: -25 }), .45],
      [P({ x: -18, lt: 12, ls: 0, rt: -24, rs: 38, la1: 25, ra1: -40, ra2: 40 }), .45], [P({ x: -24, lt: 24, ls: -38, rt: -10, rs: 0, la1: 40, la2: -40, ra1: -25 }), .45],
      [P({ x: -24 }), .3],
      // toe stand with one arm up, then a double spin
      [P({ x: -24, hop: 6, lean: -8, lt: -6, rt: 6, la1: 40, la2: -20, ra1: -165, ra2: 0, tail: 60 }), .5], [P({ x: -24, hop: 6, lean: -8, lt: -6, rt: 6, la1: 40, la2: -20, ra1: -165, ra2: 0, tail: 60 }), .35],
      [P({ x: -10, sp: 2, la1: 8, la2: 0, ra1: -8, ra2: 0, lt: 2, rt: -2, tail: 90 }), .9],
      // crouch, flying side kick
      [P({ x: -4, sp: 2, lt: 45, ls: -85, rt: -45, rs: 85, la1: 70, la2: -60, ra1: -70, ra2: 60, tail: 10 }), .45],
      [P({ x: 4, sp: 2, hop: 14, lean: 18, lt: 4, ls: 0, rt: -100, rs: -4, la1: 120, la2: 0, ra1: -25, ra2: 40, tail: 70 }), .3],
      [P({ x: 4, sp: 2, hop: 14, lean: 18, lt: 4, ls: 0, rt: -100, rs: -4, la1: 120, la2: 0, ra1: -25, ra2: 40, tail: 70 }), .35],
      [P({ x: 0, sp: 2 }), .45],
      // staff twirl
      [P({ sp: 2, st: 1, ra1: -95, ra2: -10, la1: 30, lt: 14, rt: -14, sa: 0 }), .4],
      [P({ sp: 2, st: 1, ra1: -95, ra2: -10, la1: 30, lt: 14, rt: -14, sa: 1080, lean: 4 }), 1.5],
      [P({ sp: 2, st: 0, sa: 1080 }), .4],
      // bow
      [P({ sp: 2, tor: 0, head: 28, hop: -6, lt: 30, ls: -50, rt: -30, rs: 50, la1: 60, la2: -70, ra1: -60, ra2: 70, sa: 1080 }), .55],
      [P({ sp: 2, tor: 0, head: 28, hop: -6, lt: 30, ls: -50, rt: -30, rs: 50, la1: 60, la2: -70, ra1: -60, ra2: 70, sa: 1080 }), .5],
      [P({ sp: 2, sa: 1080 }), .6]
    ];
    var total = 0; T.forEach(function (t) { total += t[1]; });
    function ease(t) { return t * t * (3 - 2 * t); }
    function pose(time) {
      var t = time % total, prev = T[T.length - 1][0];
      for (var i = 0; i < T.length; i++) {
        var d = T[i][1];
        if (t <= d) {
          var a = prev, b = T[i][0], e = ease(t / d), r = {};
          for (var k in B) r[k] = a[k] + (b[k] - a[k]) * e;
          if (i === 0) { r.sp = b.sp; r.sa = b.sa; }   // loop seam: 2 turns == 0 turns
          return r;
        }
        t -= d; prev = T[i][0];
      }
      return T[0][0];
    }
    var R = Math.PI / 180;
    function foot(hx, th, sh) { return 22 * Math.cos(th * R) + 22 * Math.cos((th + sh) * R) + 2; }
    function tr(el, x, y, a) { el.setAttribute('transform', 'translate(' + x + ',' + y + ') rotate(' + a + ')'); }
    function draw(p) {
      var low = Math.max(foot(-6, p.lt, p.ls), foot(6, p.rt, p.rs));  // standing foot touches the branch
      var hipY = -low - p.hop;
      var sx = Math.cos(p.sp * 2 * Math.PI);
      root.setAttribute('transform', 'translate(' + p.x + ',0) rotate(' + p.lean + ') scale(' + sx.toFixed(3) + ',1)');
      tr(J.tail, 0, hipY, p.tail); tr(J.lt, -6, hipY, p.lt); tr(J.rt, 6, hipY, p.rt);
      tr(J.ls, 0, 22, p.ls); tr(J.rs, 0, 22, p.rs); tr(J.tor, 0, hipY, p.tor);
      tr(J.la1, -9, -30, p.la1); tr(J.la2, 0, 17, p.la2); tr(J.ra1, 9, -30, p.ra1); tr(J.ra2, 0, 17, p.ra2);
      tr(J.head, 0, -40, p.head); tr(J.staff, 0, 16, p.sa); J.staff.setAttribute('opacity', p.st.toFixed(2));
    }
    if (reduce) { draw(T[0][0]); return; }
    var on = true, t0 = null, acc = 0, running = false;
    function kick() { if (!running && on && !document.hidden) { running = true; t0 = null; requestAnimationFrame(step); } }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { on = es[0].isIntersecting; kick(); }).observe(root.ownerSVGElement);
    document.addEventListener('visibilitychange', kick);
    function step(ts) {
      if (!on || document.hidden || window.__danceHold) { running = false; return; }
      if (t0 === null) t0 = ts - acc * 1000;
      acc = (ts - t0) / 1000; draw(pose(acc)); requestAnimationFrame(step);
    }
    window.__wenDance = function (s) { draw(pose(s)); };   // used by the build check to render single frames
    draw(T[0][0]); setTimeout(kick, 1400);
  })();

  // Jupiter prototype: storms ride the bands (alternating winds), rings breathe a little in 3D
  (function () {
    var storms = document.getElementById('storms');
    if (!storms) return;
    var NS = 'http://www.w3.org/2000/svg', cx = 200, cy = 200, R = 170;
    var F = [  // y, start longitude, speed (rad/s), rx, ry, colour, opacity
      [258, 0.6, 0.10, 30, 14, '#c25a32', .95], [258, 0.6, 0.10, 21, 9, '#e08a55', .9],
      [300, 2.2, 0.16, 9, 4.5, '#f7ecd2', .9], [300, 3.4, 0.16, 8, 4, '#f7ecd2', .85], [300, 4.6, 0.16, 9, 4.5, '#f7ecd2', .85],
      [140, 1.0, -0.13, 14, 4, '#8f5a30', .8], [140, 3.9, -0.13, 11, 3.5, '#8f5a30', .75],
      [202, 0.3, 0.22, 10, 2.5, '#9b6436', .7], [202, 1.6, 0.22, 12, 2.5, '#9b6436', .7], [202, 2.9, 0.22, 9, 2, '#9b6436', .7],
      [202, 4.2, 0.22, 12, 2.5, '#9b6436', .7], [202, 5.5, 0.22, 10, 2.5, '#9b6436', .7],
      [96, 2.0, 0.08, 16, 3, '#f8e9c8', .6], [96, 5.0, 0.08, 13, 3, '#f8e9c8', .6], [330, 1.2, -0.06, 18, 3.5, '#cfa46b', .6]
    ];
    var E = F.map(function (f) { var e = document.createElementNS(NS, 'ellipse'); e.setAttribute('fill', f[5]); storms.appendChild(e); return e; });
    var rb = document.getElementById('ring-b'), rf = document.getElementById('ring-f');
    function ring(k) {
      function el(rx, ry) { return 'M' + (cx - rx) + ' ' + cy + 'a' + rx + ' ' + ry + ' 0 1 0 ' + 2 * rx + ' 0a' + rx + ' ' + ry + ' 0 1 0 ' + (-2 * rx) + ' 0Z'; }
      var d = el(300, 300 * k) + el(262, 262 * k) + el(250, 250 * k) + el(212, 212 * k);
      rb.setAttribute('d', d); rf.setAttribute('d', d);
    }
    function frame(t) {
      for (var i = 0; i < F.length; i++) {
        var f = F[i], lon = f[1] + f[2] * t, z = Math.cos(lon), rl = Math.sqrt(Math.max(0, R * R - (f[0] - cy) * (f[0] - cy)));
        if (z <= 0.02) { E[i].setAttribute('opacity', 0); continue; }
        E[i].setAttribute('cx', (cx + rl * Math.sin(lon)).toFixed(1)); E[i].setAttribute('cy', f[0]);
        E[i].setAttribute('rx', Math.max(0.5, f[3] * z).toFixed(2)); E[i].setAttribute('ry', f[4]);
        E[i].setAttribute('opacity', (f[6] * Math.min(1, z * 3)).toFixed(2));
      }
      ring(0.2 + 0.035 * Math.sin(t * 0.35));
    }
    frame(0);
    if (reduce) return;
    var t0 = null, on = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { var was = on; on = es[0].isIntersecting; if (on && !was) requestAnimationFrame(loop); }).observe(storms.ownerSVGElement);
    function loop(ts) { if (!on || window.__danceHold) return; if (t0 === null) t0 = ts; frame((ts - t0) / 1000); requestAnimationFrame(loop); }
    window.__wenPlanet = frame;
    requestAnimationFrame(loop);
  })();

  // petals: sakura with a few teal sparks
  var c = document.querySelector('.petals');
  if (!c || reduce || !c.getContext) return;
  var ctx = c.getContext('2d'), W, H, dpr = Math.min(window.devicePixelRatio || 1, 2), P = [], run = true;
  function size() { W = c.clientWidth; H = c.clientHeight; c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  function make(top) {
    var spark = Math.random() < 0.18;
    return { x: Math.random() * W, y: top ? -20 : Math.random() * H, r: spark ? 1.6 + Math.random() * 1.4 : 5 + Math.random() * 6,
      vx: -0.3 + Math.random() * 0.8, vy: 0.35 + Math.random() * 0.8, a: Math.random() * 6.28, va: -0.02 + Math.random() * 0.04,
      sw: Math.random() * 6.28, spark: spark, o: 0.35 + Math.random() * 0.45 };
  }
  size();
  var N = Math.round(Math.min(46, Math.max(14, W / 34)));
  for (var i = 0; i < N; i++) P.push(make(false));
  window.addEventListener('resize', size);
  document.addEventListener('visibilitychange', function () { run = !document.hidden; if (run) requestAnimationFrame(tick); });
  function tick() {
    if (!run) return;
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < P.length; i++) {
      var p = P[i];
      p.sw += 0.02; p.x += p.vx + Math.sin(p.sw) * 0.5; p.y += p.vy; p.a += p.va;
      if (p.y > H + 20 || p.x < -30 || p.x > W + 30) { P[i] = make(true); continue; }
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.globalAlpha = p.o;
      if (p.spark) {
        ctx.fillStyle = '#57b3ad'; ctx.beginPath(); ctx.arc(0, 0, p.r, 0, 6.28); ctx.fill();
      } else {
        ctx.fillStyle = '#f2a7c3'; ctx.beginPath();
        ctx.moveTo(0, -p.r); ctx.quadraticCurveTo(p.r * 0.9, -p.r * 0.2, 0, p.r);
        ctx.quadraticCurveTo(-p.r * 0.9, -p.r * 0.2, 0, -p.r); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(-0.6, -p.r * 0.6, 1.2, p.r * 0.9);
      }
      ctx.restore();
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
