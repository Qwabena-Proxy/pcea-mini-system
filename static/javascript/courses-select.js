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
    const totalCourseSelected= document.getElementById("couuse-select");
    const totalCreditHours= document.getElementById("tcrh");
    let formData= new FormData();
    formData.append("courses", selectedCourses);

    fetch('/apis/v1/register-course/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token[0]}`
        },
        body: formData,
    }).then(response => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
        if (status == 200){
            getStudentCourses();
            alert("Courses registered successfully!");
            window.location.href= '/students/academics/registered-courses/';
        }else{
            alert("Error registering courses. Please try again.");
        }
    }).catch(error => {
        console.error('Error:', error);
        alert("An error occurred while registering courses.");
    });
    selectedCourses= [];
    courseContainer.querySelectorAll(".courses-card > input").forEach(element => {
        element.checked= false;
    });
    totalCourseSelected.textContent= `Courses Selected: 0`
    totalCreditHours.textContent= `Total Credit Hours: 0`
    modal.style.display= 'none';
    modal.style.visibility= 'hidden';
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
                            <p>Code: ${response[element].CC}</p>
                            <p>CRH: ${response[element].CCHR}</p>
                        </div>
                        <p>${response[element].CT}</p>
                        <input type="hidden" id="ID" value="${response[element].ID}">
                        <input type="hidden" id="CCHR" value="${response[element].CCHR}">
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
let totalCreditHoursCalculated= 0;
const addEvents= () => {
    const cardsChecks= courseContainer.querySelectorAll(".courses-card > input")
    const coursIDs= courseContainer.querySelectorAll(".courses-card .info > input#ID")
    const coursecrh= courseContainer.querySelectorAll(".courses-card .info > input#CCHR")
    const totalCourseSelected= document.getElementById("couuse-select");
    const totalCreditHours= document.getElementById("tcrh");
    cardsChecks.forEach((element, index) => {
        element.addEventListener("click", () => {
            let currentID= coursIDs[index].value;
            if(selectedCourses.includes(currentID)){
                selectedCourses= selectedCourses.filter(IDs => IDs !== currentID);
                totalCreditHoursCalculated -= parseInt(coursecrh[index].value)
            }else{
                selectedCourses.push(currentID);
                totalCreditHoursCalculated += parseInt(coursecrh[index].value)
            }
            totalCourseSelected.textContent= `Courses Selected: ${selectedCourses.length}`
            totalCreditHours.textContent= `Total Credit Hours: ${totalCreditHoursCalculated}`
        })
    })
}




getStudentCourses();