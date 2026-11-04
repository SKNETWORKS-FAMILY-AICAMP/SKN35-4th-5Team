// 예상 매출 시나리오 대시보드: 큰 숫자가 세어 올라가고, 정지 기간 게이지, 월 매출 범위 · 원문 vs 추천 문구 차트(마우스를 올리면 값).
// 숫자는 템플릿이 먼저 글자로 찍어 두고(스크립트가 없어도 읽힌다), 여기서는 움직임과 그림만 더한다.
(() => {
  const el = document.getElementById("fc-data");
  if (!el) return;
  const D = JSON.parse(el.textContent);
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const css = getComputedStyle(document.documentElement);
  const C = { gold: "#E7AE55", goldSoft: "rgba(231,174,85,.18)", risk: "#E5564E", safe: "#1FA6A0", ink: css.getPropertyValue("--ink").trim() || "#F6EEE1",
              muted: "rgba(246,238,225,.62)", faint: "rgba(246,238,225,.32)", grid: "rgba(233,185,110,.12)", surface: "#15110C" };

  // 서버 humanize_won.won 과 같은 규칙
  const won = (v) => v == null ? "-" : Math.abs(v) >= 1e8 ? `${(v / 1e8).toLocaleString("ko-KR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}억 원`
    : Math.abs(v) >= 1e4 ? `${Math.round(v / 1e4).toLocaleString("ko-KR")}만 원` : `${Math.round(v).toLocaleString("ko-KR")}원`;

  // ── 숫자 세기 ──
  document.querySelectorAll("[data-count]").forEach((n) => {
    const target = +n.dataset.count, unit = n.dataset.unit, dec = +(n.dataset.dec || 0);
    if (!isFinite(target) || reduce) return;
    const fmt = (v) => unit ? `${v.toFixed(dec)}${unit}` : won(v);
    const prefix = n.querySelector("small")?.outerHTML ?? "";
    const t0 = performance.now(), dur = 1400;
    (function step(t) {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      n.innerHTML = (prefix ? prefix + " " : "") + fmt(target * e);
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  });

  // ── 정지 기간 게이지 (12개월 기준) ──
  const g = document.querySelector("[data-gauge]");
  if (g) {
    const c = g.querySelector(".g-val"), L = 2 * Math.PI * 40, m = Math.min(12, +g.dataset.gauge || 0);
    c.style.strokeDasharray = `${L}`;
    c.style.strokeDashoffset = `${L}`;
    requestAnimationFrame(() => requestAnimationFrame(() => { c.style.strokeDashoffset = `${L * (1 - m / 12)}`; }));
  }

  // ── 차트 공통 ──
  const NS = "http://www.w3.org/2000/svg";
  const mk = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent?.appendChild(e); return e; };
  // SVG 선언형 애니메이션 (동작 줄이기면 붙이지 않는다)
  const anim = (el, attrs, tag = "animate") => { if (!reduce) mk(tag, { repeatCount: "indefinite", ...attrs }, el); return el; };
  function defs(svg, id) {
    const d = mk("defs", {}, svg);
    // 위험 막대 줄무늬 (색만으로 구분하지 않게 하는 결 + 흐르는 움직임)
    const pat = mk("pattern", { id: `stripe-${id}`, width: 10, height: 10, patternUnits: "userSpaceOnUse", patternTransform: "rotate(45)" }, d);
    mk("rect", { width: 4, height: 10, fill: "rgba(255,255,255,.22)" }, pat);
    anim(pat, { attributeName: "patternTransform", type: "translate", from: "0 0", to: "10 0", dur: "0.9s", additive: "sum" }, "animateTransform");
    // 막대 위를 지나가는 빛
    const sh = mk("linearGradient", { id: `sheen-${id}`, x1: 0, x2: 1 }, d);
    [["0", 0], [".45", 0], [".5", .55], [".55", 0], ["1", 0]].forEach(([o, a]) => mk("stop", { offset: o, "stop-color": "#fff", "stop-opacity": a }, sh));
    anim(sh, { attributeName: "gradientTransform", type: "translate", from: "-1 0", to: "1 0", dur: "2.6s" }, "animateTransform");
    // 변화 폭 띠의 일렁임
    const bd = mk("linearGradient", { id: `band-${id}`, x1: 0, x2: 1 }, d);
    [["0", .10], [".5", .32], ["1", .10]].forEach(([o, a]) => mk("stop", { offset: o, "stop-color": C.gold, "stop-opacity": a }, bd));
    anim(bd, { attributeName: "gradientTransform", type: "translate", values: "-.5 0;.5 0;-.5 0", dur: "4s" }, "animateTransform");
    // 빛 번짐
    const gl = mk("filter", { id: `glow-${id}`, x: "-50%", y: "-50%", width: "200%", height: "200%" }, d);
    mk("feGaussianBlur", { stdDeviation: 3, result: "b" }, gl);
    const m = mk("feMerge", {}, gl); mk("feMergeNode", { in: "b" }, m); mk("feMergeNode", { in: "SourceGraphic" }, m);
  }

  function niceMax(v) { const p = Math.pow(10, Math.floor(Math.log10(v || 1))); return Math.ceil(v / p / 2) * 2 * p; }
  function tip(plot) {
    let t = plot.querySelector(".tip");
    if (!t) { t = document.createElement("div"); t.className = "tip"; t.setAttribute("role", "tooltip"); plot.appendChild(t); }
    return {
      show(x, y, html) { t.innerHTML = html; t.style.left = `${x}px`; t.style.top = `${y}px`; t.classList.add("on"); },
      hide() { t.classList.remove("on"); },
    };
  }
  function axis(svg, x, max, y0, h, w) {
    const n = w < 480 ? 2 : 4;   // 좁은 화면은 눈금을 줄여 글자가 겹치지 않게
    for (let i = 0; i <= n; i++) {
      const v = (max / n) * i, px = x(v);
      const gl = mk("line", { x1: px, x2: px, y1: y0 + h, y2: y0 + h, stroke: C.grid, "stroke-width": 1 }, svg);
      gl.style.transition = reduce ? "none" : `all .8s cubic-bezier(.2,.7,.2,1) ${i * 80}ms`;
      requestAnimationFrame(() => gl.setAttribute("y1", y0));   // 눈금선이 아래에서 위로 차례로 선다
      const t = mk("text", { x: Math.min(px, w - 4), y: y0 + h + 16, fill: C.faint, "font-size": 11, "text-anchor": i === 0 ? "start" : i === n ? "end" : "middle", "font-family": "IBM Plex Mono, monospace" }, svg);
      t.textContent = i === 0 ? "0" : won(v);
    }
  }

  // ① 월 매출 범위: 적게 ─ 보통 ─ 많이 + 문구 교체 시 변화 폭 띠
  function drawRange(plot) {
    plot.querySelector("svg")?.remove();
    const W = plot.clientWidth, H = 190, pad = 18, y = 86;
    const r = D.revenue, b = D.band;
    const max = niceMax(Math.max(r.high, b.high) * 1.05);
    const x = (v) => pad + (v / max) * (W - pad * 2);
    const svg = mk("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}` }, plot);
    defs(svg, "r");
    axis(svg, x, max, 30, 120, W);
    const T = tip(plot);
    // 변화 폭 띠 (일렁이는 금빛 + 테두리 점선이 흐른다)
    const band = mk("rect", { x: x(b.low), y: y - 18, width: Math.max(2, x(b.high) - x(b.low)), height: 36, rx: 8, fill: "url(#band-r)", stroke: C.gold, "stroke-dasharray": "4 4", "stroke-opacity": .6 }, svg);
    anim(band, { attributeName: "stroke-dashoffset", from: 0, to: -16, dur: "1.6s" });
    band.addEventListener("pointermove", (e) => T.show(e.offsetX, e.offsetY - 12, `<b>문구 교체 시 변화 폭</b>±${D.band_pct}% · ${won(b.low)} ~ ${won(b.high)}<br><small>방향 미정 (오를 수도 내릴 수도)</small>`));
    band.addEventListener("pointerleave", T.hide);
    // 범위 선
    const line = mk("line", { x1: x(r.low), x2: x(r.low), y1: y, y2: y, stroke: C.gold, "stroke-width": 6, "stroke-linecap": "round" }, svg);
    requestAnimationFrame(() => { line.style.transition = reduce ? "none" : "all 1.1s cubic-bezier(.2,.7,.2,1)"; line.setAttribute("x2", x(r.high)); });
    // 선을 따라 적게 → 많이 로 흐르는 빛 알갱이 3개
    if (!reduce) for (let k = 0; k < 3; k++) {
      const p = mk("circle", { cx: x(r.low), cy: y, r: 3.5, fill: "#FFF3D6", filter: "url(#glow-r)", opacity: 0 }, svg);
      anim(p, { attributeName: "cx", from: x(r.low), to: x(r.high), dur: "2.4s", begin: `${1.1 + k * .8}s` });
      anim(p, { attributeName: "opacity", values: "0;1;1;0", keyTimes: "0;.15;.8;1", dur: "2.4s", begin: `${1.1 + k * .8}s` });
    }
    // 점 · 직접 라벨 (가까우면 위아래로 엇갈린다)
    const pts = [["적게", r.low], ["보통", r.mid], ["많이", r.high]];
    pts.forEach(([name, v], i) => {
      const px = x(v), close = i > 0 && px - x(pts[i - 1][1]) < 96, up = !(close && i === 1);
      if (name === "보통") {   // 기준값에서 물결이 퍼진다
        const ring = mk("circle", { cx: px, cy: y, r: 9, fill: "none", stroke: C.gold, "stroke-width": 1.5, opacity: 0 }, svg);
        anim(ring, { attributeName: "r", values: "9;24", dur: "2s", begin: "1.2s" });
        anim(ring, { attributeName: "opacity", values: ".8;0", dur: "2s", begin: "1.2s" });
      }
      const dot = mk("circle", { cx: px, cy: y, r: name === "보통" ? 9 : 7, fill: C.gold, stroke: C.surface, "stroke-width": 2, class: "pop", style: `animation-delay:${.5 + i * .25}s` }, svg);
      const ty = up ? y - 34 : y + 44;
      const t1 = mk("text", { x: px, y: ty, fill: C.muted, "font-size": 11.5, "text-anchor": "middle", class: "rise", style: `animation-delay:${.7 + i * .25}s` }, svg); t1.textContent = name;
      const t2 = mk("text", { x: px, y: ty + 16, fill: C.ink, "font-size": 14, "font-weight": 700, "text-anchor": "middle", class: "rise", style: `animation-delay:${.75 + i * .25}s` }, svg); t2.textContent = won(v);
      const hit = mk("circle", { cx: px, cy: y, r: 22, fill: "transparent" }, svg);
      hit.addEventListener("pointermove", () => T.show(px, y - 18, `<b>월 매출 · ${name}</b>${won(v)}`));
      hit.addEventListener("pointerleave", T.hide);
      void dot;
    });
  }

  // ② 원문 vs 추천 문구: 처분 시 영향받는 매출 (보통 월 매출은 참고 점선)
  function drawCompare(plot) {
    plot.querySelector("svg")?.remove();
    const W = plot.clientWidth, H = 190, pad = 18;
    const risk = D.risk_status === "mapped" ? D.risk_amount || 0 : 0;
    const max = niceMax(Math.max(risk, D.revenue.high) * 1.08);
    const x = (v) => pad + (v / max) * (W - pad * 2);
    const svg = mk("svg", { width: W, height: H, viewBox: `0 0 ${W} ${H}` }, plot);
    defs(svg, "c");
    axis(svg, x, max, 22, 128, W);
    const T = tip(plot);
    const rows = [
      { name: "원문 그대로", v: risk, color: C.risk, y: 52, label: D.risk_status === "mapped" ? `${D.risk_is_estimate ? "" : "최대 "}${won(risk)}` : D.risk_status === "needs_review" ? "개별 검토 필요" : "위험 없음" },
      { name: "추천 문구", v: 0, color: C.safe, y: 112, label: D.has_best ? "0원 · 위험 없음" : "제안 없음" },
    ];
    const mx = x(D.revenue.mid);
    rows.forEach((row) => {
      const t = mk("text", { x: pad, y: row.y - 12, fill: C.muted, "font-size": 12 }, svg); t.textContent = row.name;
      const w = Math.max(6, x(row.v) - pad);
      const bar = mk("rect", { x: pad, y: row.y, width: 6, height: 22, rx: 4, fill: row.color }, svg);
      const isRisk = row.color === C.risk && row.v > 0;
      // 위험 막대: 흐르는 줄무늬 결 + 지나가는 빛 / 안전 막대: 은은하게 숨 쉬는 빛
      const over = isRisk ? [mk("rect", { x: pad, y: row.y, width: 6, height: 22, rx: 4, fill: "url(#stripe-c)" }, svg),
                             mk("rect", { x: pad, y: row.y, width: 6, height: 22, rx: 4, fill: "url(#sheen-c)" }, svg)] : [];
      if (!isRisk) { bar.setAttribute("filter", "url(#glow-c)"); anim(bar, { attributeName: "opacity", values: "1;.55;1", dur: "2.4s" }); }
      requestAnimationFrame(() => [bar, ...over].forEach((r) => { r.style.transition = reduce ? "none" : "width 1.1s cubic-bezier(.2,.7,.2,1)"; r.setAttribute("width", w); }));
      // 값 라벨: 막대 끝 오른쪽. 참고 점선과 겹치면 점선 뒤로, 오른쪽 끝을 넘으면 막대 안쪽으로
      let lx = pad + w + 10;
      if (lx < mx + 8 && lx + 110 > mx - 8) lx = mx + 10;
      const inside = lx > W - 120;
      const lab = mk("text", { x: inside ? pad + w - 10 : lx, y: row.y + 16, fill: inside ? "#120D08" : C.ink, "font-size": 14, "font-weight": 700, "text-anchor": inside ? "end" : "start" }, svg);
      lab.textContent = row.label;
      const hit = mk("rect", { x: pad, y: row.y - 8, width: Math.max(w, 120), height: 38, fill: "transparent" }, svg);
      hit.addEventListener("pointermove", (e) => T.show(e.offsetX, row.y - 6, `<b>${row.name}</b>${row.label}`));
      hit.addEventListener("pointerleave", T.hide);
    });
    // 참고: 월 예상 매출(보통)
    const ref = mk("line", { x1: mx, x2: mx, y1: 24, y2: 150, stroke: C.gold, "stroke-width": 1.5, "stroke-dasharray": "3 4" }, svg);
    anim(ref, { attributeName: "stroke-dashoffset", from: 0, to: -14, dur: "1.2s" });
    const rt = mk("text", { x: Math.max(80, Math.min(mx, W - 80)), y: 14, fill: C.muted, "font-size": 11, "text-anchor": "middle" }, svg); rt.textContent = `참고 · 월 매출 보통 ${won(D.revenue.mid)}`;
  }

  const range = document.querySelector('[data-chart="range"]'), compare = document.querySelector('[data-chart="compare"]');
  const draw = () => { range && drawRange(range); compare && drawCompare(compare); };
  draw();
  let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(draw, 150); });
})();
