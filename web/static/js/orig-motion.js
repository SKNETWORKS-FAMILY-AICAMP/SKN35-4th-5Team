
(function () {
  document.documentElement.classList.add('bw-js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function count(scope) {
    scope.querySelectorAll('[data-count]:not([data-counted])').forEach(function (el) {
      el.setAttribute('data-counted', '1');
      var to = +el.getAttribute('data-count');
      if (reduce || !to) return;
      var t0 = performance.now(), dur = 1200;
      el.textContent = '0';
      (function step(t) {
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(to * e).toLocaleString('ko-KR');
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    });
  }

  function reveal() {
    var els = document.querySelectorAll('.bw-h .rv:not([data-rv])');
    if (!els.length) return;
    if (reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.setAttribute('data-rv', '1'); el.classList.add('is-in'); count(el); });
      return;
    }
    if (!window.__bwRv) {
      window.__bwRv = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.classList.add('is-in');
          window.__bwRv.unobserve(en.target);
          count(en.target);
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -8% 0px' });
    }
    els.forEach(function (el) { el.setAttribute('data-rv', '1'); window.__bwRv.observe(el); });
  }

  function demo() {
    document.querySelectorAll('[data-demo]:not([data-run])').forEach(play);
  }
  function play(box) {
    box.setAttribute('data-run', '1');
    if (reduce) return;
    var exs = box.querySelectorAll('.ex'), dots = box.querySelectorAll('.dots i');
    var ext = box.getAttribute('data-buddy') ? document.querySelector(box.getAttribute('data-buddy')) : null;   // 히어로: 사진 위 토끼
    var say = (ext || box).querySelector('.say'), buddy = ext || box.querySelector('.buddy');
    var SAY = {"start": "문구를 읽고 있어요", "marks": "위험 표현에 밑줄을 그었어요", "nomarks": "근거 조항을 찾고 있어요", "verdict": "규정 기준으로 판정했어요", "hold": "판단하기 어려운 문구예요", "cites": "근거 조항을 달았어요", "fix": "이렇게 고쳐 보면 어때요?", "nofix": "담당자 확인이 필요해요"};
    var STEPS = [300, 1000, 1700, 2500, 3500], HOLD = 7600, timers = [];
    function talk(text) {
      if (!say || !text) return;
      say.textContent = text;
      say.classList.remove('pop'); void say.offsetWidth; say.classList.add('pop');
      if (buddy) { buddy.classList.remove('hop'); void buddy.offsetWidth; buddy.classList.add('hop'); }
    }
    function line(ex, step) {
      if (step === 1) return ex.querySelector('.bw-mark:not(.is-verified)') ? SAY.marks : SAY.nomarks;
      if (step === 2) return ex.classList.contains('is-hold') ? SAY.hold : SAY.verdict;
      if (step === 3) return ex.querySelector('.cites') ? SAY.cites : '';
      if (step === 4) return ex.querySelector('.fix.is-hold') ? SAY.nofix : SAY.fix;
      return '';
    }
    function show(n) {
      timers.forEach(clearTimeout); timers = [];
      if (!document.body.contains(box)) return;
      exs.forEach(function (e, k) { e.classList.remove('on', 's1', 's2', 's3', 's4', 's5'); if (k === n) e.classList.add('on'); });
      dots.forEach(function (d, k) { d.classList.toggle('on', k === n); });
      talk(SAY.start);
      STEPS.forEach(function (ms, k) {
        timers.push(setTimeout(function () { exs[n].classList.add('s' + (k + 1)); talk(line(exs[n], k + 1)); }, ms));
      });
      timers.push(setTimeout(function () { show((n + 1) % exs.length); }, HOLD));
    }
    show(0);
  }

  // 4) 히어로 사진 마우스 시차(--mx · --my) 5) 상단 스크롤 진행선(--p) 6) 사진 띠 스크롤 시차(--py) 7) 지금 섹션의 메뉴 표시(.on)
  //    리스너는 문서에 한 번만 — Streamlit 이 노드를 다시 그려도 매번 다시 찾는다
  function scene() {
    if (window.__bwScene) return;
    window.__bwScene = true;
    var queued = false;
    function frame() {
      queued = false;
      var main = document.querySelector('[data-testid="stMain"]'), top = document.querySelector('.st-key-home_top');
      if (!main || !top) return;
      var max = main.scrollHeight - main.clientHeight, vh = window.innerHeight;
      top.style.setProperty('--p', max > 0 ? (main.scrollTop / max).toFixed(4) : '0');
      var current = '';
      document.querySelectorAll('.bw-h-sec[id]').forEach(function (s) { if (s.getBoundingClientRect().top < vh * 0.4) current = s.id; });
      document.querySelectorAll('.bw-h-nav a').forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + current); });
      if (reduce) return;
      var hero = document.querySelector('.st-key-home_hero');
      if (hero) {   // 히어로를 지나갈수록 0 → 1 (떠 있는 사물이 흩어진다)
        var hr = hero.getBoundingClientRect();
        hero.style.setProperty('--hs', Math.min(1, Math.max(0, -hr.top / Math.max(1, hr.height))).toFixed(3));
      }
      document.querySelectorAll('.bw-h-photo[data-par]').forEach(function (f) {
        var r = f.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        f.style.setProperty('--py', (((r.top + r.height / 2) - vh / 2) / vh).toFixed(4));
      });
    }
    function ask() { if (!queued) { queued = true; requestAnimationFrame(frame); } }
    document.addEventListener('scroll', ask, { capture: true, passive: true });
    window.addEventListener('resize', ask);
    document.addEventListener('mousemove', function (e) {
      if (reduce) return;
      var hero = document.querySelector('.st-key-home_hero');
      if (!hero) return;
      var r = hero.getBoundingClientRect();
      if (e.clientY > r.bottom) return;
      hero.style.setProperty('--mx', ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      hero.style.setProperty('--my', ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    }, { passive: true });
    ask();
  }

  function run() { reveal(); demo(); scene(); }
  run();
  setTimeout(run, 250);
  setTimeout(run, 1200);
})();
