const btnWithDebt= document.getElementById("btnWD");
const btnWithoutDebt= document.getElementById("btnWOD");
const contents= document.querySelectorAll("main > div");
const switcherBtnList= [btnWithDebt, btnWithoutDebt]

btnWithDebt.addEventListener("click", () => {
    contents.forEach((x, i) => {
        x.classList.remove("active")
        switcherBtnList[i].classList.remove("active")
    });
    contents[0].classList.add("active");
    switcherBtnList[0].classList.add("active")
});

btnWithoutDebt.addEventListener("click", () => {
    contents.forEach((x, i) => {
        x.classList.remove("active")
        switcherBtnList[i].classList.remove("active")
    });
    contents[1].classList.add("active");
    switcherBtnList[1].classList.add("active")
});