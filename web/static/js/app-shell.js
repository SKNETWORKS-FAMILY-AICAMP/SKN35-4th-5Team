// 로그인 후 화면 공통: 사이드바 미끄러지는 표시 · 카드 위 빛 · 시계 · 금빛 입자.
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 사이드바: 금빛 표시가 지금 화면에 앉아 있다가, 마우스가 다른 메뉴로 가면 따라 미끄러진다
  const nav = document.querySelector("[data-rail]");
  if (nav) {
    const ind = nav.querySelector(".rail-ind");
    const links = [...nav.querySelectorAll("a")];
    const here = links.find((a) => a.hasAttribute("aria-current"));
    const place = (a) => { if (!a) { ind.classList.remove("on"); return; } ind.style.top = `${a.offsetTop}px`; ind.classList.add("on"); };
    place(here);
    links.forEach((a) => {
      a.addEventListener("mouseenter", () => { links.forEach((x) => x.classList.toggle("is-hover", x === a)); });
      a.addEventListener("mouseleave", () => a.classList.remove("is-hover"));
      a.addEventListener("click", () => place(a));   // 누르면 표시가 먼저 그 메뉴로 날아간다
    });
    const replace = () => place(links.find((a) => a.hasAttribute("aria-current")));
    addEventListener("resize", replace);
    // 글꼴을 다 불러오면 그룹 이름 높이가 달라져 메뉴 위치가 몇 px 움직인다 → 그때 다시 맞춘다
    document.fonts?.ready.then(replace);
    addEventListener("load", replace);
  }

  // 카드 위를 따라가는 빛
  document.addEventListener("pointermove", (e) => {
    const c = e.target.closest?.(".card");
    if (!c) return;
    const r = c.getBoundingClientRect();
    c.style.setProperty("--sx", `${e.clientX - r.left}px`);
    c.style.setProperty("--sy", `${e.clientY - r.top}px`);
  }, { passive: true });

  // 시계
  const clock = document.querySelector("[data-clock]");
  if (clock) {
    const tick = () => { const d = new Date(); clock.textContent = `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")} · ${d.toLocaleTimeString("ko-KR", { hour12: false })}`; };
    tick(); setInterval(tick, 1000);
  }

  // 금빛 입자
  const cv = document.querySelector(".app-particles");
  if (!cv || reduce) return;
  const cx = cv.getContext("2d");
  let W, H, P = [];
  const size = () => {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    W = innerWidth; H = innerHeight; cv.width = W * dpr; cv.height = H * dpr; cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    P = Array.from({ length: Math.round(W * H / 22000) }, () => ({ x: Math.random() * W, y: Math.random() * H, r: Math.random() * 1.4 + .3, v: Math.random() * .2 + .04, a: Math.random() * .5 + .15, p: Math.random() * 6 }));
  };
  size(); addEventListener("resize", size);
  (function loop(t) {
    cx.clearRect(0, 0, W, H);
    for (const q of P) {
      q.y -= q.v; q.x += Math.sin(t / 2600 + q.p) * .12;
      if (q.y < -4) { q.y = H + 4; q.x = Math.random() * W; }
      cx.globalAlpha = q.a * (.6 + .4 * Math.sin(t / 800 + q.p));
      cx.fillStyle = "#FFDFA6"; cx.beginPath(); cx.arc(q.x, q.y, q.r, 0, 6.283); cx.fill();
    }
    cx.globalAlpha = 1;
    requestAnimationFrame(loop);
  })(0);
})();
