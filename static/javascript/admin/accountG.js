import { getToken, removeTokens } from "../general.js";

const logoutBtn = document.getElementById("logout");
const staffName = document.getElementById("staff-name");
const staffEmail = document.getElementById("staff-email");
const staffDepartment = document.getElementById("staff-department");

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

const getStaffInfo = () => {
  const token = getToken();
  if (token[0] == null || token[1] == null) {
    alert("Session has expired. Please login again to continue");
    window.location.href = "/login/";
    return;
  }
  fetch("/apis/v1/staff-info/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token[0]}`,
    },
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        const userInfo = response.data;
        staffName.textContent = `${userInfo.fullName}`;
        staffEmail.textContent = `${userInfo.email}`;
        staffDepartment.textContent = `${userInfo.department}`;
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
                studentID: response.token.staffID,
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

getStaffInfo();
