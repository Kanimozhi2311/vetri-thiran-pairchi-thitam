const form = document.getElementById("comic-form");
const button = document.getElementById("generate-button");
if (form && button) {
  form.addEventListener("submit", () => {
    button.disabled = true;
    button.querySelector("span").textContent = "Generating your comic...";
    button.style.opacity = "0.7";
  });
}
