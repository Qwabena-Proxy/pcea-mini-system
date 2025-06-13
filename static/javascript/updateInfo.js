const studentSurname = document.getElementById("student-surname");
const otherName = document.getElementById("student-otherName");
const indexNumber = document.getElementById("student-indexNumber");
const studentTelephone = document.getElementById("student-telephone");
const studentProgram = document.getElementById("student-program");
const studentLevel = document.getElementById("student-level");
const infoSubmitBtn = document.getElementById("info-submit-btn");
const studentProgramLevel = document.getElementById("student-program-level");

const existingToken = JSON.parse(window.localStorage.getItem("token"));
const userID = existingToken.studentID;

infoSubmitBtn.addEventListener("click", () => {
  const apiUrl = `/apis/v1/auth/update-student-info/`;
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let formData = new FormData();

  formData.append("studentSurname", studentSurname.value);
  formData.append("otherName", otherName.value);
  formData.append("indexNumber", indexNumber.value);
  formData.append("studentTelephone", studentTelephone.value);
  formData.append("studentProgram", studentProgram.value);
  formData.append("studentProgramLevel", studentProgramLevel.value);
  formData.append("studentLevel", studentLevel.value);
  formData.append("studentID", userID);
  formData.append("csrfmiddlewaretoken", csrfToken);

  fetch(apiUrl, {
    method: "POST",
    body: formData,
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, data]) => {
      if (status == 200) {
        window.location.href = "/students/dashboard/";
      } else {
        alert(data.message);
      }
    });
});
