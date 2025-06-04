const sendBtn= document.getElementById("send");
const levelInputElement= document.getElementById("level-input");
const programInputElement= document.getElementById("program-input");


//Btns
const levelSubmit= document.getElementById("submit-level");
const levelClear= document.getElementById("clear-level");
const programSubmit= document.getElementById("submit-program");
const progamClear= document.getElementById("clear-program");
const courseSubmit= document.getElementById("submit-course");
const courseClear= document.getElementById("clear-course");


const address= 'http://127.0.0.1:8000'
const singleStudentCreateApiUrl= `/apis/v1/create-student/`;
const levelCreateApiUrl= `/apis/v1/create-level/`;
const programCreateApiUrl= `/apis/v1/create-program/`;
const courseCreateApiUrl= `/apis/v1/create-course/`;
const getupdate= `/apis/v1/get-update`;


const clearBtns= [levelClear, progamClear]
const clearInputs= [levelInputElement, programInputElement]

clearBtns.forEach((element, index) => {
    element.addEventListener("click", (e) => {
        clearElement(clearInputs[index])
        clearInputs[index].focus()
    })
})
// levelClear.addEventListener("click", (e) => {
//     clearElement(levelInputElement);
// })

levelSubmit.addEventListener("click", (e) => {
    e.preventDefault();
    if (levelInputElement.value === "") {
        alert("Please enter a level name.");
        return;
    }
    levelSubmitHandler(e);
    clearElement(levelInputElement);
});

programSubmit.addEventListener("click", (e) => {
    e.preventDefault();
    if (programInputElement.value === "") {
        alert("Please enter a program name.");
        return;
    }
    programSubmitHandler(e);
    clearElement(programInputElement);
});

courseSubmit.addEventListener("click", (e) => {
    courseSubmitHandler(e);
});



const clearElement= (e) => {
    e.value = "";
    e.focus();
}

const levelSubmitHandler = (e) => {
    let formData= new FormData();
    formData.append("name", levelInputElement.value);
    fetch(`${address}${levelCreateApiUrl}`, {
    method: 'POST',
    body: formData
    })
    .then(response => response.json())
    .then(data => {
    console.log(data); // Handle response
    })
    .catch(error => {
    console.error('Error:', error);
    });
}

const programSubmitHandler = (e) => {
    let formData= new FormData();
    formData.append("name", programInputElement.value);
    fetch(`${address}${programCreateApiUrl}`, {
    method: 'POST',
    body: formData
    })
    .then(response => response.json())
    .then(data => {
    console.log(data); // Handle response
    })
    .catch(error => {
    console.error('Error:', error);
    });
}

const courseSubmitHandler = (e) => {
    const courseCodeInputElement= document.getElementById("course-code");
    const courseTitleInputElement= document.getElementById("course-title");
    const courseCreditInputElement= document.getElementById("course-credit");
    const courseLevelInputElement= document.getElementById("course-level");
    const courseProgramInputElement= document.getElementById("course-program");
    const semesterValue = document.querySelector('input[name="semester"]:checked')?.value;
    e.preventDefault();
    if (courseCodeInputElement.value === "" || courseTitleInputElement.value === "" || courseCreditInputElement.value === "" || courseLevelInputElement.value === "" || courseProgramInputElement.value === "" || !semesterValue) {
        alert("Please fill in all fields.");
        return;
    }
    
    let formData= new FormData();
    formData.append("code", courseCodeInputElement.value);
    formData.append("name", courseTitleInputElement.value);
    formData.append("crh", courseCreditInputElement.value);
    formData.append("level", courseLevelInputElement.value);
    formData.append("program", courseProgramInputElement.value);
    formData.append("semester", semesterValue);
    fetch(`${address}${courseCreateApiUrl}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Handle response
    })
    .catch(error => {
        console.error('Error:', error);
    });


}
// sendBtn.addEventListener("click", () => {
//     const email= document.getElementById("email");
//     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     let formData= new FormData();

//     formData.append("email", email.value)
//     formData.append("csrfmiddlewaretoken", csrfToken);
//     fetch(apiUrl,{
//         method: 'POST',
//         body: formData,
//     }).then(response => response.json()).
//     then(response => {
//         console.log(response)
//     }).catch(err => console.error(err))
// })

const getlevel = () => {
    const levelList= document.getElementById("level-list")
    const programList= document.getElementById("program-list")
    const courseList= document.getElementById("course-list")
    const programDataList= document.getElementById("programs-data")
    const levelDataList= document.getElementById("level-data")
    levelList.innerHTML= ''
    fetch(`${address}${getupdate}`,{
        method: 'GET'
    }).then(response => response.json())
    .then(response => {
        const level= response.level
        const program= response.program
        const course= response.course
        for(const x of level){
            levelList.innerHTML += `<li>${x}</li>`
            levelDataList.innerHTML += `<option value="${x}"></option>`
        }
        for(const x of program){
            programList.innerHTML += `<li>${x}</li>`
            programDataList.innerHTML += `<option value="${x}"></option>`
        }
        for(const x of course){
            courseList.innerHTML += `<li>${x}</li>`
        }
    })
    .catch(err => console.error(err))
}

getlevel()