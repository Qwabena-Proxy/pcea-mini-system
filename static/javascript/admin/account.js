const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const btnWithDebt = document.getElementById("btnWD");
const btnWithoutDebt = document.getElementById("btnWOD");
const contents = document.querySelectorAll("main > div");
const sliderSwitchers = document.querySelectorAll(".slider.dept > p");
const deptList = document.querySelectorAll(".student-container.debt");
const sliderWSwitchers = document.querySelectorAll(".slider.w-dept > p");
const deptWList = document.querySelectorAll(".student-container.w-debt");
const cards = document.querySelectorAll(".card");
const switcherBtnList = [btnWithDebt, btnWithoutDebt];

const address = "http://127.0.0.1:8000";

btnWithDebt.addEventListener("click", () => {
  contents.forEach((x, i) => {
    x.classList.remove("active");
    switcherBtnList[i].classList.remove("active");
  });
  contents[0].classList.add("active");
  switcherBtnList[0].classList.add("active");
});

btnWithoutDebt.addEventListener("click", () => {
  contents.forEach((x, i) => {
    x.classList.remove("active");
    switcherBtnList[i].classList.remove("active");
  });
  contents[1].classList.add("active");
  switcherBtnList[1].classList.add("active");
});

sliderWSwitchers.forEach((x, index) => {
  x.addEventListener("click", (e) => {
    sliderWSwitchers.forEach((y, yIndex) => {
      y.classList.remove("selected");
      deptWList[yIndex].classList.remove("active");
    });
    e.target.classList.add("selected");
    deptWList[index].classList.add("active");
  });
});

sliderSwitchers.forEach((x, index) => {
  x.addEventListener("click", (e) => {
    sliderSwitchers.forEach((y, yIndex) => {
      y.classList.remove("selected");
      deptList[yIndex].classList.remove("active");
    });
    e.target.classList.add("selected");
    deptList[index].classList.add("active");
  });
});

cards.forEach((element, index) => {
  const btn = element.querySelector("input");
  const stdIndexNumber = element.querySelector("p:first-of-type");

  let formData = new FormData();
  formData.append("indexNumber", stdIndexNumber.textContent);

  btn.addEventListener("click", (e) => {
    const url =
      e.target.value == "Clear student"
        ? "/apis/v1/clear-student/"
        : "/apis/v1/debt-student/";
    fetch(`${address}${url}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data); // Handle response
        window.location.reload();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});
