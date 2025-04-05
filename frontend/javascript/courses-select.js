const registerbtn= document.querySelector("#btnRegister");
const modal= document.querySelector("body .modal");
const noBtn= document.getElementById("btnNo");


registerbtn.addEventListener("click", () => {
    modal.style.display= 'flex';
    modal.style.visibility= 'visible';
})

noBtn.addEventListener("click", () => {
    modal.style.display= 'none';
    modal.style.visibility= 'hidden';
})