// 챗봇 화면: 메시지를 /chat/<id>/send/ 로 보내고 응답을 그린다.
(() => {
  const log = document.getElementById("chat-log");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const csrf = form.querySelector("[name=csrfmiddlewaretoken]").value;
  const LEVELS = { 0: "가능", 1: "조건부", 2: "불가" };

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // assistant 응답에 검토·생성 결과가 있으면 요약 카드를 붙인다.
  function detailCard(response) {
    const card = el("div", "chat-detail");
    const review = response.review;
    if (review && review.result) {
      const r = review.result;
      const label = r.status === "판정" ? LEVELS[r.level] : r.status;
      card.appendChild(el("span", `badge badge-${r.level ?? "hold"}`, label));
      (review.candidates || []).forEach((c) => card.appendChild(el("p", "copy", c)));
    }
    const generation = response.generation;
    if (generation) {
      (generation.candidates || []).forEach((c) => {
        const item = el("p", "copy");
        item.appendChild(el("span", "badge", c.status));
        item.append(" " + c.text);
        card.appendChild(item);
      });
    }
    const citations = response.citations?.length ? response.citations : review?.result?.citations || [];
    if (citations.length) {
      const list = el("ul", "citations");
      citations.slice(0, 3).forEach((c) => list.appendChild(el("li", "", `${c.source} ${c.article}`)));
      card.appendChild(list);
    }
    return card.childNodes.length ? card : null;
  }

  function render(message) {
    const bubble = el("div", `bubble bubble-${message.role}`);
    bubble.appendChild(el("p", "", message.content));
    if (message.role === "assistant" && message.response) {
      const card = detailCard(message.response);
      if (card) bubble.appendChild(card);
    }
    log.appendChild(bubble);
    log.scrollTop = log.scrollHeight;
    return bubble;
  }

  JSON.parse(document.getElementById("chat-messages").textContent).forEach(render);

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    const button = form.querySelector("button");
    button.disabled = true;
    input.value = "";
    const pendingUser = render({ role: "user", content: message });
    const pending = render({ role: "assistant", content: "답변을 준비하고 있어요…" });
    try {
      const res = await fetch(form.dataset.sendUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      pending.remove();
      if (!res.ok) {
        // 실패한 메시지는 저장되지 않으므로 입력창에 되돌려 다시 보낼 수 있게 한다.
        pendingUser.remove();
        input.value = message;
        render({ role: "assistant", content: data.error || "요청에 실패했습니다." }).classList.add("bubble-error");
        return;
      }
      render(data.assistant);
    } catch (error) {
      pending.remove();
      pendingUser.remove();
      input.value = message;
      render({ role: "assistant", content: "서버에 연결하지 못했습니다." }).classList.add("bubble-error");
    } finally {
      button.disabled = false;
      input.focus();
    }
  });

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      form.requestSubmit();
    }
  });
})();
