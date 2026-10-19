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
