// 로그인 ↔ 회원가입 슬라이드. 탭 · 아래 링크를 눌러 넘어갈 때만 움직인다
// (폼 오류로 같은 화면이 다시 뜨거나, 뒤로 가기 · 주소로 바로 들어오면 움직이지 않는다).
// <head> 에서 읽는다: pagereveal 은 첫 그림 전에 오므로 그 전에 듣고 있어야 한다.
(() => {
  const me = document.currentScript?.dataset.me;        // login | signup
  if (!me) return;
  const dir = (to) => (to === "signup" ? "fwd" : "back"); // 회원가입은 오른쪽에서, 로그인은 왼쪽에서 들어온다
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const vt = "CSSViewTransitionRule" in window;
  const KEY = "auth-slide";
  const take = () => { try { const v = sessionStorage.getItem(KEY); sessionStorage.removeItem(KEY); return v; } catch { return null; } };
  const keep = (v) => { try { sessionStorage.setItem(KEY, v); } catch { /* 저장 못 하면 그냥 넘어간다 */ } };
  const html = document.documentElement;

  const arrive = (d) => {
    html.classList.add("auth-arrive", `auth-dir-${d}`);
    setTimeout(() => html.classList.remove("auth-arrive"), 1600);
  };

  // 들어온 쪽
  const came = take() === me && !reduce;
  if (vt) {
    addEventListener("pagereveal", (e) => {
      if (!e.viewTransition) { if (came) arrive(dir(me)); return; }
      if (!came) { e.viewTransition.skipTransition(); return; }
      e.viewTransition.types.add(`auth-${dir(me)}`);
      arrive(dir(me));
    });
  } else if (came) {
    html.classList.add(`auth-enter-${dir(me)}`);
    arrive(dir(me));
  }

  // 나가는 쪽
  addEventListener("DOMContentLoaded", () => document.querySelectorAll("[data-auth-go]").forEach((a) => {
    a.addEventListener("click", (e) => {
      const to = a.dataset.authGo;
      if (to === me || e.metaKey || e.ctrlKey || e.shiftKey || e.button) { if (to === me) e.preventDefault(); return; }
      keep(to);
      if (vt || reduce) return;                  // 전환은 브라우저가 맡는다
      e.preventDefault();
      html.classList.add(`auth-leave-${dir(to)}`);
      setTimeout(() => { location.href = a.href; }, 400);
    });
  }));
})();
