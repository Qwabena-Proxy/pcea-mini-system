import { storeToken, removeTokens } from "./general.js";
removeTokens();
const selectors = document.querySelectorAll(".selectors > h2");
const authEmail = document.getElementById("auth-email");
const authPassword = document.getElementById("auth-password");
const authButton = document.getElementById("auth-btn");

selectors.forEach((e) => {
  e.addEventListener("click", () => {
    selectors.forEach((x) => {
      x.classList.remove("active");
    });
    e.classList.add("active");
  });
});

authButton.addEventListener("click", () => {
  const studentActive = selectors[0].classList.contains("active")
    ? true
    : false;
  if (studentActive) {
    var apiUrl = `/apis/v1/auth/login/`;
  } else {
    var apiUrl = `/apis/v1/auth/staff-login/`;
  }
  const email = authEmail.value.trim();
  const password = authPassword.value.trim();
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let formData = new FormData();

  formData.append("password", password);
  formData.append("csrfmiddlewaretoken", csrfToken);
  formData.append("email", email);

  fetch(apiUrl, {
    method: "POST",
    body: formData,
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, data]) => {
      if (status == 200) {
        console.log(data);
        const token = {
          accessToken: data.access,
          refreshToken: data.refresh,
          email: data.email,
          studentID: data.studentID,
        };
        if (!studentActive) {
          token.studentID = data.staffID;
        }
        storeToken(token.accessToken, token.refreshToken, token.studentID);
        if (data.updateRequired) {
          if (studentActive) {
            window.location.href = `/students/update-info/`;
          } else {
            window.location.href = `/staff/update-info/`;
          }
        } else {
          if (studentActive) {
            window.location.href = `/students/dashboard/`;
          } else {
            window.location.href = `/account-office/`;
          }
        }
      } else {
        console.log(data);
        alert("Failed to login, please check your email and password.");
      }
    })
    .catch((err) => console.error(err));
});
