// 내 제품: 유형 · 일반/기능성으로 거르기. 비어 있는 묶음은 숨기고, 묶음마다 개수를 단다.
(() => {
  const bar = document.querySelector("[data-pd-filter]");
  if (!bar) return;
  bar.hidden = false;
  let g = "all", c = "all";
  function apply() {
    bar.querySelectorAll("[data-g]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.g === g)));
    bar.querySelectorAll("[data-c]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.c === c)));
    document.querySelectorAll(".pd-group").forEach((grp) => {
      let n = 0;
      grp.querySelectorAll(".pd-card").forEach((card) => {
        const on = (g === "all" || grp.dataset.group === g) && (c === "all" || card.dataset.cat === c);
        card.hidden = !on;
        if (on) n++;
      });
      grp.hidden = n === 0;
      grp.querySelector("[data-count]").textContent = n ? `${n}` : "";
    });
  }
  bar.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.g) g = b.dataset.g;
    if (b.dataset.c) c = b.dataset.c;
    apply();
  });
  apply();
})();
