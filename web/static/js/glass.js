// 3차 원본 홈 위 유리 효과. 원본 스크립트(교정 장면 · 방울 물결)는 그대로 두고 옆에서 돈다.
//  1) 히어로 화보에 김이 서린다 → 커서(손가락)로 문지르면 닦이고, 닦인 가장자리에서 물방울이 맺혀 흘러내리며 맑은 줄을 남긴다.
//     시간이 지나면 다시 김이 서린다. (레퍼런스 2 — 샤워 유리)
//  2) 유리 패널 위 하이라이트가 손을 따라 움직인다. 3) 화보를 가로지르는 빛줄기. (레퍼런스 1)
// '동작 줄이기'면 김 · 물방울 · 빛줄기를 켜지 않고 패널 유리만 남긴다.
(() => {
  const root = document.documentElement;
  root.classList.add("bw-glass");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ── 패널 하이라이트 ──
  document.addEventListener("pointermove", (e) => {
    const p = e.target.closest?.(".bw-h-proof, .bw-h-demo .card");
    if (!p) return;
    const r = p.getBoundingClientRect();
    p.style.setProperty("--gx", `${e.clientX - r.left}px`);
    p.style.setProperty("--gy", `${e.clientY - r.top}px`);
  }, { passive: true });

  if (reduce) return;
  const ph = document.querySelector(".bw-h-scene .ph");
  if (!ph) return;

  // ── 빛줄기 ──
  const beam = document.createElement("i");
  beam.className = "bw-beam";
  ph.appendChild(beam);

  // ── 김 서린 유리 ──
  const steam = document.createElement("div");
  steam.className = "bw-steam";
  const drops = document.createElement("canvas");
  drops.className = "bw-steam-drops";
  ph.append(steam, drops);

  const K = 5;                       // 마스크 해상도 = 화면 1/5 (가장자리가 부드럽게 번진다)
  const mask = document.createElement("canvas");
  const mx = mask.getContext("2d");
  const dx = drops.getContext("2d");
  let W = 0, H = 0, dpr = 1;
  function size() {
    W = ph.offsetWidth; H = ph.offsetHeight; dpr = Math.min(devicePixelRatio || 1, 2);
    const keep = mask.width ? mx.getImageData(0, 0, mask.width, mask.height) : null;
    mask.width = Math.max(1, Math.ceil(W / K)); mask.height = Math.max(1, Math.ceil(H / K));
    if (keep) mx.putImageData(keep, 0, 0);
    drops.width = W * dpr; drops.height = H * dpr;
    dx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  size();
  new ResizeObserver(size).observe(ph);   // 사진 상자 크기는 글꼴 · 사진을 다 불러온 뒤에 정해진다

  // 처음엔 맑은 유리 → 몇 초에 걸쳐 김이 서린다 (마스크: 흰색 = 김)
  let fog = 0, dirty = true, last = 0, wiped = false;
  const REFOG = 0.0026;              // 프레임당 다시 서리는 정도 (닦인 자리가 약 8초에 다시 흐려진다)

  function wipe(x, y, r) {
    const g = mx.createRadialGradient(x / K, y / K, 0, x / K, y / K, r / K);
    g.addColorStop(0, "rgba(0,0,0,1)"); g.addColorStop(.62, "rgba(0,0,0,.9)"); g.addColorStop(1, "rgba(0,0,0,0)");
    mx.globalCompositeOperation = "destination-out";
    mx.fillStyle = g;
    mx.beginPath(); mx.arc(x / K, y / K, r / K, 0, Math.PI * 2); mx.fill();
    mx.globalCompositeOperation = "source-over";
    dirty = true;
  }

  // 물방울: 닦인 가장자리에 맺혔다가 하나씩 미끄러져 내린다
  const list = [];
  function spawn(x, y, r) {
    if (list.length > 60) return;
    const a = Math.random() * Math.PI * 2;
    list.push({ x: x + Math.cos(a) * r * .9, y: y + Math.abs(Math.sin(a)) * r * .8, r: 1.6 + Math.random() * 3.6,
                v: 0, hold: 400 + Math.random() * 2600, born: performance.now() });
  }
  function drawDrop(d) {
    const g = dx.createRadialGradient(d.x - d.r * .35, d.y - d.r * .4, d.r * .1, d.x, d.y, d.r);
    g.addColorStop(0, "rgba(255,255,255,.95)"); g.addColorStop(.35, "rgba(255,255,255,.25)");
    g.addColorStop(.8, "rgba(120,90,40,.18)"); g.addColorStop(1, "rgba(60,40,15,.35)");
    dx.fillStyle = g;
    dx.beginPath(); dx.ellipse(d.x, d.y, d.r, d.r * 1.12, 0, 0, Math.PI * 2); dx.fill();
  }

  let lx = null, ly = null;
  function stroke(x, y) {
    const R = Math.max(46, Math.min(W, H) * .085);
    if (lx == null) { wipe(x, y, R); } else {
      const n = Math.ceil(Math.hypot(x - lx, y - ly) / (R / 3));
      for (let i = 1; i <= n; i++) wipe(lx + (x - lx) * i / n, ly + (y - ly) * i / n, R);
    }
    if (Math.random() < .35) spawn(x, y, R);
    lx = x; ly = y; wiped = true;
  }
  document.addEventListener("pointermove", (e) => {
    const r = ph.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    if (x < W * .24 || x > W || y < 0 || y > H || fog < .5) { lx = ly = null; return; }   // 왼쪽 24% 는 글자 뒤로 흐려지는 자리
    stroke(x, y);
  }, { passive: true });

  // 손이 없는 화면(터치 · 발표 화면)을 위해: 김이 다 서리면 한 번 스스로 닦는다
  function demoWipe() {
    if (wiped) return;
    const pts = [], t0 = performance.now();
    for (let i = 0; i <= 40; i++) { const t = i / 40; pts.push([W * (.5 + .38 * t), H * (.42 + .16 * Math.sin(t * Math.PI * 2.2))]); }
    let i = 0;
    (function step() { if (i < pts.length) { stroke(...pts[i++]); requestAnimationFrame(step); } else { lx = ly = null; } })();
    void t0;
  }
  setTimeout(demoWipe, 4200);

  function frame(now) {
    const dt = Math.min(64, now - (last || now)); last = now;
    // 김이 서리고 · 다시 서린다
    if (fog < 1) { fog = Math.min(1, fog + dt / 3200); }
    mx.globalCompositeOperation = "source-over";
    mx.fillStyle = `rgba(255,255,255,${fog < 1 ? dt / 3200 : REFOG * dt / 16})`;
    mx.fillRect(0, 0, mask.width, mask.height);
    dirty = true;

    // 물방울
    dx.clearRect(0, 0, W, H);
    for (let i = list.length - 1; i >= 0; i--) {
      const d = list[i];
      if (now - d.born > d.hold) {
        d.v = Math.min(d.v + .05 * d.r, 2.2 + d.r * .5) * (Math.random() < .08 ? .2 : 1);   // 멈칫멈칫 흘러내린다
        const ny = d.y + d.v;
        mx.globalCompositeOperation = "destination-out";
        mx.strokeStyle = "rgba(0,0,0,.85)"; mx.lineWidth = Math.max(1, d.r * 1.3 / K); mx.lineCap = "round";
        mx.beginPath(); mx.moveTo(d.x / K, d.y / K); mx.lineTo(d.x / K, ny / K); mx.stroke();
        mx.globalCompositeOperation = "source-over";
        d.y = ny; d.x += (Math.random() - .5) * .6; d.r *= .9993;
      }
      if (d.y > H + 10 || d.r < 1) { list.splice(i, 1); continue; }
      drawDrop(d);
    }

    if (dirty) {
      const url = `url(${mask.toDataURL()})`;
      steam.style.webkitMaskImage = url; steam.style.maskImage = url;
      dirty = false;
    }
    requestAnimationFrame(frame);
  }
  // 첫 마스크는 맑은 상태
  mx.clearRect(0, 0, mask.width, mask.height);
  requestAnimationFrame(() => { steam.classList.add("on"); requestAnimationFrame(frame); });
})();
