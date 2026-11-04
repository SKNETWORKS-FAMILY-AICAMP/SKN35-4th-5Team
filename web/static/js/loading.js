// data-loading 속성이 있는 폼을 제출하면 버튼을 잠그고 안내 문구를 보여준다 (AI 응답이 느리므로).
document.querySelectorAll("form[data-loading]").forEach((form) => {
  form.addEventListener("submit", () => {
    const button = form.querySelector("button[type=submit]");
    if (button) {
      button.disabled = true;
      button.textContent = "처리 중…";
    }
    const note = document.createElement("p");
    note.className = "loading";
    note.textContent = form.dataset.loading;
    form.appendChild(note);
  });
});
