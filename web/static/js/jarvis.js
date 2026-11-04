// 가로 8장 화면 넘기기 · 자비스 HUD (배경 사진 · 금빛 입자 · 시계 · 장 이름 표시).
// 원본 스크립트(orig-motion.js 교정 장면 · orig-drip.js 방울 물결)와 glass.js(김 서림)는 따로 돈다.
(() => {
  const body = document.body;
  const slides = [...document.querySelectorAll(".jv-slide")];
  const steps = [...document.querySelectorAll("[data-go]")];
  const cur = document.querySelector("[data-cur]");
  const read = document.querySelector("[data-read]");
  const bg = document.querySelector(".jv-bg-photo");
  const prev = document.querySelector('[data-step="-1"]'), next = document.querySelector('[data-step="1"]');
  const narrow = matchMedia("(max-width: 900px)");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let i = -1, lock = 0;

  function show(n, push = true) {
    n = Math.max(0, Math.min(slides.length - 1, n));
    if (n === i) return;
    const back = n < i;
    i = n;
    slides.forEach((s, k) => {
      s.classList.toggle("is-on", k === n);
      s.classList.toggle("is-prev", k < n);
      s.setAttribute("aria-hidden", String(k !== n));
      s.inert = k !== n && !narrow.matches;
    });
    steps.forEach((b, k) => (k === n ? b.setAttribute("aria-current", "step") : b.removeAttribute("aria-current")));
    body.dataset.slide = n;
    cur.textContent = String(n + 1).padStart(2, "0");
    prev.disabled = n === 0; next.disabled = n === slides.length - 1;
    const s = slides[n];
    if (read) read.innerHTML = `SECTION ${String(n + 1).padStart(2, "0")} // ${s.dataset.title}<br>STATUS · ${back ? "RECALL" : "LOADED"}`;
    // 배경: 그 장의 원본 사진 (없으면 앞 장 사진을 어둡게 유지)
    if (s.dataset.bg) { bg.classList.remove("on"); requestAnimationFrame(() => { bg.style.backgroundImage = `url("${s.dataset.bg}")`; bg.classList.add("on", "is-clear"); }); }
    else bg.classList.remove("on");
    s.querySelector(".jv-body").scrollTop = 0;
    body.classList.remove("is-moving"); void body.offsetWidth; body.classList.add("is-moving");
    if (push) history.replaceState(null, "", "#" + s.id);
    // 원본 스크립트가 보이는 칸만 움직이게 하므로, 새 장에 들어오면 다시 확인하게 한다
    dispatchEvent(new Event("scroll"));
  }
  const go = (d) => { if (performance.now() < lock) return; lock = performance.now() + 950; show(i + d); };

  steps.forEach((b, k) => b.addEventListener("click", () => show(k)));
  prev.addEventListener("click", () => show(i - 1));
  next.addEventListener("click", () => show(i + 1));
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const k = slides.findIndex((s) => "#" + s.id === a.hash || s.querySelector(a.hash));
    if (k >= 0 && !narrow.matches) { e.preventDefault(); show(k); }
  });
  addEventListener("keydown", (e) => {
    if (narrow.matches || e.target.closest("input, textarea")) return;
    if (["ArrowRight", "PageDown"].includes(e.key)) { e.preventDefault(); show(i + 1); }
    if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); show(i - 1); }
    if (e.key === "Home") show(0);
    if (e.key === "End") show(slides.length - 1);
  });
  // 휠: 장 안에 더 내릴 내용이 있으면 먼저 내리고, 끝에 닿으면 다음 장으로
  addEventListener("wheel", (e) => {
    if (narrow.matches) return;
    const d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    if (Math.abs(d) < 8) return;
    const sc = slides[i].querySelector(".jv-body");
    const canDown = sc.scrollTop + sc.clientHeight < sc.scrollHeight - 2, canUp = sc.scrollTop > 2;
    if ((d > 0 && canDown) || (d < 0 && canUp)) return;
    e.preventDefault();
    go(d > 0 ? 1 : -1);
  }, { passive: false });
  // 터치: 옆으로 밀기
  let tx = null, ty = null;
  addEventListener("touchstart", (e) => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  addEventListener("touchend", (e) => {
    if (tx == null || narrow.matches) return;
    const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.4) go(dx < 0 ? 1 : -1);
    tx = ty = null;
  }, { passive: true });

  const start = Math.max(0, slides.findIndex((s) => "#" + s.id === location.hash));
  show(start, false);

  // 시계
  const clock = document.querySelector("[data-clock]");
  const tick = () => { const d = new Date(); clock.textContent = d.toLocaleTimeString("ko-KR", { hour12: false }); };
  tick(); setInterval(tick, 1000);

  // 금빛 입자 (먼지처럼 떠오른다)
  if (reduce) return;
  const cv = document.querySelector(".jv-particles"), cx = cv.getContext("2d");
  let W, H, P = [];
  const size = () => {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = innerWidth; H = innerHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    P = Array.from({ length: Math.round(W * H / 16000) }, () => ({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.6 + .3, v: Math.random() * .25 + .05, a: Math.random() * .6 + .2, p: Math.random() * 6 }));
  };
  size(); addEventListener("resize", size);
  (function loop(t) {
    cx.clearRect(0, 0, W, H);
    for (const q of P) {
      q.y -= q.v; q.x += Math.sin(t / 2400 + q.p) * .15;
      if (q.y < -4) { q.y = H + 4; q.x = Math.random() * W; }
      cx.globalAlpha = q.a * (.6 + .4 * Math.sin(t / 700 + q.p));
      cx.fillStyle = "#FFDFA6"; cx.beginPath(); cx.arc(q.x, q.y, q.r, 0, 6.283); cx.fill();
    }
    cx.globalAlpha = 1;
    requestAnimationFrame(loop);
  })(0);
})();
