import { getToken, storeToken, removeTokens } from "./general.js";

const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const studentName = document.getElementById("student-name");
const studentProgramLevel = document.getElementById("student-program-level");
const studentProgram = document.getElementById("student-program");
const logoutBtn = document.getElementById("log-out-btn");
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
        status == 400 ||
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
      } else {
        console.log(response);
      }
    })
    .catch((err) => console.error(err));
};

logoutBtn.addEventListener("click", () => {
  const confirmation = confirm(
    "Are you sure you want to logout? You will be redirected to the login page."
  );
  if (confirmation) {
    logoutHandler();
  }
});

const logoutHandler = () => {
  removeTokens();
  window.location.href = "/login/";
};

getStudentRegisterInfo();
