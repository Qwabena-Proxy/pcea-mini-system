const btnWithDebt = document.getElementById("btnWD");
const btnWithoutDebt = document.getElementById("btnWOD");
const contents = document.querySelectorAll("main > div");
const sliderSwitchers = document.querySelectorAll(".slider.dept > p");
const deptList = document.querySelectorAll(".student-container.debt");
const sliderWSwitchers = document.querySelectorAll(".slider.w-dept > p");
const deptWList = document.querySelectorAll(".student-container.w-debt");
const switcherBtnList = [btnWithDebt, btnWithoutDebt];

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
