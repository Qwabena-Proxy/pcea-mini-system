import { getToken, storeToken } from "./general.js";

const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const tableContent = document.querySelector(".course-table > table > tbody");
// const modal= document.querySelector("body .modal");
// const noBtn= document.getElementById("btnNo");
// const yesBtn= document.getElementById("btnYes");
// const courseContainer= document.querySelector(".courses-container");

const getStudentRegisteredCourses = () => {
  const token = getToken();
  fetch("/apis/v1/register-course/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token[0]}`,
    },
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        tableContent.innerHTML = "";
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
      } else if (
        status == 400 &&
        response.message ==
          "Access token has expired use your refresh token to generate new tokens and try again."
      ) {
        let tokenForm = new FormData();
        tokenForm.append("refToken", token[1]);
        fetch("/apis/v1/token-regenerate/", {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
          },
          body: tokenForm,
        })
          .then((response) => Promise.all([response.status, response.json()]))
          .then(([status, response]) => {
            if (status == 201) {
              const token = {
                accessToken: response.token.access,
                refreshToken: response.token.refresh,
                email: response.token.email,
                studentID: response.token.studentID,
              };
              storeToken(
                token.accessToken,
                token.refreshToken,
                token.studentID
              );
              window.location.reload();
            } else if (status >= 400) {
              alert("Sesssion has expired. Please login again to continue");
              window.location.href = "/login/";
            }
          });
      } //
    });
};

const getStudentRegisterInfo = () => {
  const token = getToken();
  fetch("/apis/v1/student-register-course/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token[0]}`,
    },
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        const userInfo = response.data;
        console.log(userInfo.indexNumber);
        document.getElementById(
          "index-number"
        ).textContent = `Index Number: ${userInfo.indexNumber}`;
        document.getElementById(
          "name"
        ).textContent = `Full Name: ${userInfo.fullName}`;
        document.getElementById(
          "program"
        ).textContent = `Program: ${userInfo.program}`;
        document.getElementById(
          "level"
        ).textContent = `Level: ${userInfo.level}`;
        document.getElementById(
          "semester"
        ).textContent = `Semester: ${userInfo.current_semester}`;
      } else if (status == 400) {
        displayModal(response);
      }
    })
    .catch((err) => console.error(err));
};

const displayModal = (response) => {
  const modal = document.querySelector(".modal-authorization");
  const modalTitle = document.querySelector(".modal-authorization .card > h2");
  const modalMessage = document.querySelector(".modal-authorization .card > p");
  const modalAction = document.querySelector(
    ".modal-authorization .card .action > input"
  );
  modal.style.display = "flex";
  modal.style.visibility = "visible";
  modalTitle.textContent = "Error";
  modalMessage.textContent = `${
    response.message || "Bad request. Please try again."
  }`;
  modalAction.addEventListener("click", () => {
    window.history.back();
  });
  modalAction.value = "Go Back";
};

getStudentRegisterInfo();
getStudentRegisteredCourses();
