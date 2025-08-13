const submitIndexNumber = document.getElementById("submit-id-btn");
const submitDetails = document.getElementById("submit-details-btn");

submitIndexNumber.addEventListener("click", (e) => {
  const icon = submitIndexNumber.querySelector("span > i");
  const iconContainer = submitIndexNumber.querySelector("span.icon");
  const textContainer = submitIndexNumber.querySelector("span.text");
  icon.classList.replace("ri-send-plane-line", "ri-loader-4-line");
  iconContainer.style.animationName = "loader";
  textContainer.textContent = "Verifying";
});

submitDetails.addEventListener("click", (e) => {
  const icon = submitDetails.querySelector("span > i");
  const iconContainer = submitDetails.querySelector("span.icon");
  const textContainer = submitDetails.querySelector("span.text");
  icon.classList.replace("ri-send-plane-line", "ri-loader-4-line");
  iconContainer.style.animationName = "loader";
  textContainer.textContent = "Processing";
});
