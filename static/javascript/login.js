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
  if (selectors[0].classList.contains("active")) {
    var apiUrl = `/apis/v1/auth/login/`;
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
        const token = {
          accessToken: data.access,
          refreshToken: data.refresh,
          email: data.email,
          studentID: data.studentID,
        };
        storeToken(token.accessToken, token.refreshToken, token.studentID);
        if (data.updateRequired) {
          window.location.href = `/students/update-info/`;
        } else {
          window.location.href = `/students/dashboard/`;
        }
      } else {
        console.log(data);
        alert("Failed to login, please check your email and password.");
      }
    })
    .catch((err) => console.error(err));
});
