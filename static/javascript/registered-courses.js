import {getToken} from './general.js';

const tableContent= document.querySelector(".course-table > table > tbody");
// const modal= document.querySelector("body .modal");
// const noBtn= document.getElementById("btnNo");
// const yesBtn= document.getElementById("btnYes");
// const courseContainer= document.querySelector(".courses-container");

const getStudentRegisteredCourses= () => {
    const token= getToken();
    fetch('/apis/v1/register-course/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token[0]}`
        }
      }).then(response => Promise.all([response.status, response.json()]))
      .then(([status, response]) => {
        if (status == 200){
        tableContent.innerHTML = '';
        const courses = response.data;
        for (let key in courses) {
                const course = courses[key];
                tableContent.innerHTML += `
                    <tr>
                        <td>${course.code}</td>
                        <td colspan="4">${course.title}</td>
                        <td>${course.crh}</td>
                    </tr>
                `;
            }                   
    // addEvents();
}
      })
}

const getStudentRegisterInfo= () => {
    const token= getToken();
    fetch('/apis/v1/student-register-course/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token[0]}`
        }
      }).then(response => Promise.all([response.status, response.json()]))
      .then(([status, response]) => {
        if (status == 200){
            const userInfo = response.data;
            console.log(userInfo.indexNumber)
            document.getElementById('index-number').textContent= `Index Number: ${userInfo.indexNumber}`
            document.getElementById('name').textContent= `Full Name: ${userInfo.fullName}`
            document.getElementById('program').textContent= `Program: ${userInfo.program}`
            document.getElementById('level').textContent= `Level: ${userInfo.level}`
            document.getElementById('semester').textContent= `Semester: ${userInfo.current_semester}`              
    }
    })
   .catch(err => console.error(err))   
}

getStudentRegisterInfo()
getStudentRegisteredCourses()