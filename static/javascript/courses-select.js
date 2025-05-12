import {getToken} from './general.js';

const registerbtn= document.querySelector("#btnRegister");
const modal= document.querySelector("body .modal");
const noBtn= document.getElementById("btnNo");
const yesBtn= document.getElementById("btnYes");
const courseContainer= document.querySelector(".courses-container");


registerbtn.addEventListener("click", () => {
    modal.style.display= 'flex';
    modal.style.visibility= 'visible';
})

noBtn.addEventListener("click", () => {
    modal.style.display= 'none';
    modal.style.visibility= 'hidden';
})

yesBtn.addEventListener("click", () => {
    modal.style.display= 'none';
    modal.style.visibility= 'hidden';
    const token= getToken();
    let formData= new FormData();
    formData.append("courses", selectedCourses);

    fetch('/apis/v1/register-course/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token[0]}`
        },
        body: formData,
    })
})

const getStudentCourses= () => {
    const token= getToken();
    fetch('/apis/v1/get-course/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token[0]}`
        }
      }).then(response => Promise.all([response.status, response.json()]))
      .then(([status, response]) => {
        if (status == 200){
            courseContainer.innerHTML= ''
            for(let element in response){
                    courseContainer.innerHTML += `
                        <div class="courses-card">
                    <div class="info">
                        <div class="upper">
                            <p>${response[element].CC}</p>
                            <p>${response[element].CCHR}</p>
                        </div>
                        <p>${response[element].CT}</p>
                        <input type="hidden" value="${response[element].ID}">
                    </div>
                    <input type="checkbox" name="" id="">
                </div>
                    `
            }
            addEvents();
        }
      })
}


let selectedCourses= [];
const addEvents= () => {
    const cardsChecks= courseContainer.querySelectorAll(".courses-card > input")
    const coursIDs= courseContainer.querySelectorAll(".courses-card .info > input")
    cardsChecks.forEach((element, index) => {
        element.addEventListener("click", () => {
            let currentID= coursIDs[index].value;
            if(selectedCourses.includes(currentID)){
                selectedCourses= selectedCourses.filter(IDs => IDs !== currentID);
            }else{
                selectedCourses.push(currentID);
            }
        })
    })
}




getStudentCourses();