function toggleEdit(showForm) {
  const form = document.getElementById("editForm");
  const details = document.getElementById("detailSection");
  const editBtn = document.getElementById("editBtn");

  if (showForm) {
    form.classList.remove("d-none");
    details.classList.add("d-none");
    editBtn.classList.add("d-none");
  }
}
