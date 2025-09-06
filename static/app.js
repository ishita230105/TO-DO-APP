// Toggle, Edit (inline), Delete — all via fetch, no full reload.
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("button");
  if (!btn) return;

  const card = btn.closest(".task-card");
  const id = card?.dataset.id;
  const action = btn.dataset.action;

  // Toggle complete
  if (action === "toggle" && id) {
    const res = await fetch(`/toggle/${id}`, { method: "POST" });
    const data = await res.json();
    if (data.ok) location.reload(); // quick and reliable
  }

  // Delete
  if (action === "delete" && id) {
    if (!confirm("Delete this task?")) return;
    const res = await fetch(`/delete/${id}`, { method: "POST" });
    const data = await res.json();
    if (data.ok) card.remove();
  }

  // Show inline editor
  if (action === "edit" && id) {
    const editor = card.querySelector(".inline-editor");
    editor.classList.toggle("d-none");
  }
});

// Submit inline editor
document.addEventListener("submit", async (e) => {
  const form = e.target.closest(".inline-editor");
  if (!form) return;
  e.preventDefault();

  const id = form.dataset.id;
  const fd = new FormData(form);

  const res = await fetch(`/edit/${id}`, { method: "POST", body: fd });
  const data = await res.json();
  if (data.ok) location.reload();
});

// Bootstrap validation for add form
(() => {
  const forms = document.querySelectorAll(".needs-validation");
  Array.from(forms).forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    }, false);
  });
})();