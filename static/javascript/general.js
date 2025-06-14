import config from "./config.js";

// const alertEl= document.querySelector(".alert");
// const alertContent= document.getElementById("alert-content");
// const closeAlert= document.getElementById("closeAlert");

export const showAlert = (color, info) => {
  alertEl.style.backgroundColor = color;
  alertContent.textContent = info;

  alertEl.style.transform = "translateY(5%)";
};

const hideAlert = () => {
  alertEl.style.transform = "translateY(-110%)";
};

// closeAlert.addEventListener("click", () => {hideAlert()});

export function storeToken(accessToken, refreshToken, userID) {
  const newToken = {
    accessToken: accessToken,
    refreshToken: refreshToken,
    studentID: userID,
  };
  window.localStorage.setItem("token", JSON.stringify(newToken));
}

export function removeTokens() {
  window.localStorage.removeItem("token");
}

export function getToken() {
  const token = window.localStorage.getItem("token");
  const parsedToken = JSON.parse(token);
  const accessToken = parsedToken.accessToken;
  const refreshToken = parsedToken.refreshToken;
  const userID = parsedToken.studentID;
  return [accessToken, refreshToken, userID];
}
