import { getToken, storeToken, removeTokens } from "../general.js";

const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const logoutBtn = document.getElementById("logout");
const btnWithDebt = document.getElementById("btnWD");
const btnWithoutDebt = document.getElementById("btnWOD");
const contents = document.querySelectorAll("main > div");
const sliderSwitchers = document.querySelectorAll(".slider.dept > p");
const deptList = document.querySelectorAll(".student-container.debt");
const sliderWSwitchers = document.querySelectorAll(".slider.w-dept > p");
const deptWList = document.querySelectorAll(".student-container.w-debt");
const cards = document.querySelectorAll(".card");
const staffName = document.getElementById("staff-name");
const staffEmail = document.getElementById("staff-email");
const staffDepartment = document.getElementById("staff-department");
const switcherBtnList = [btnWithDebt, btnWithoutDebt];

const address = "http://127.0.0.1:8000";

btnWithDebt.addEventListener("click", () => {
  contents.forEach((x, i) => {
    x.classList.remove("active");
    switcherBtnList[i].classList.remove("active");
  });
  contents[0].classList.add("active");
  switcherBtnList[0].classList.add("active");
});

btnWithoutDebt.addEventListener("click", () => {
  contents.forEach((x, i) => {
    x.classList.remove("active");
    switcherBtnList[i].classList.remove("active");
  });
  contents[1].classList.add("active");
  switcherBtnList[1].classList.add("active");
});

sliderWSwitchers.forEach((x, index) => {
  x.addEventListener("click", (e) => {
    sliderWSwitchers.forEach((y, yIndex) => {
      y.classList.remove("selected");
      deptWList[yIndex].classList.remove("active");
    });
    e.target.classList.add("selected");
    deptWList[index].classList.add("active");
  });
});

sliderSwitchers.forEach((x, index) => {
  x.addEventListener("click", (e) => {
    sliderSwitchers.forEach((y, yIndex) => {
      y.classList.remove("selected");
      deptList[yIndex].classList.remove("active");
    });
    e.target.classList.add("selected");
    deptList[index].classList.add("active");
  });
});

cards.forEach((element, index) => {
  const btn = element.querySelector("input");
  const stdIndexNumber = element.querySelector("p:first-of-type");

  let formData = new FormData();
  formData.append("indexNumber", stdIndexNumber.textContent);

  btn.addEventListener("click", (e) => {
    const url =
      e.target.value == "Clear student"
        ? "/apis/v1/clear-student/"
        : "/apis/v1/debt-student/";
    fetch(`${address}${url}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data); // Handle response
        window.location.reload();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});

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
