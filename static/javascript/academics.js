import { getToken, storeToken } from "./general.js";

const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const studentName = document.getElementById("student-name");
const studentProgramLevel = document.getElementById("student-program-level");
const studentProgram = document.getElementById("student-program");

const SelectDropdown = document.querySelector(".select-drop .title");
const dropIcon = document.querySelector(".select-drop .title > i");
const contentDisplay = document.querySelector(".select-drop .content");

var isOpen = false;
SelectDropdown.addEventListener("click", () => {
  if (!isOpen) {
    dropIcon.style.transform = "rotate(180deg)";
    contentDisplay.style.display = "none";
  } else {
    dropIcon.style.transform = "rotate(0deg)";
    contentDisplay.style.display = "flex";
  }
  isOpen = !isOpen;
});

const getStudentRegisterInfo = () => {
  const token = getToken();
  fetch("/apis/v1/student-info/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token[0]}`,
    },
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        const userInfo = response.data;
        studentName.textContent = `${userInfo.fullName}`;
        studentProgram.textContent = `${userInfo.program}`;
        studentProgramLevel.textContent =
          userInfo.pogram_level == "False"
            ? "Bachelor of Education (Upper Primary)"
            : "Bachelor of Education (J.H.S)";
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
      }
    })
    .catch((err) => console.error(err));
};

getStudentRegisterInfo();
