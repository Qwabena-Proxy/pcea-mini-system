import { getToken } from "./general.js";

const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const registerbtn = document.querySelector("#btnRegister");
const modal = document.querySelector("body .modal");
const noBtn = document.getElementById("btnNo");
const yesBtn = document.getElementById("btnYes");
const courseContainer = document.querySelector(".courses-container");

registerbtn.addEventListener("click", () => {
  modal.style.display = "flex";
  modal.style.visibility = "visible";
});

noBtn.addEventListener("click", () => {
  modal.style.display = "none";
  modal.style.visibility = "hidden";
});

yesBtn.addEventListener("click", () => {
  modal.style.display = "none";
  modal.style.visibility = "hidden";
  const token = getToken();
  const totalCourseSelected = document.getElementById("couuse-select");
  const totalCreditHours = document.getElementById("tcrh");
  let formData = new FormData();
  formData.append("courses", selectedCourses);

  fetch("/apis/v1/register-course/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token[0]}`,
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        getStudentCourses();
        alert("Courses registered successfully!");
        window.location.href = "/students/academics/registered-courses/";
      } else {
        console.log(response);
        alert(
          "Error registering courses. Please try again if problem still exist try logging in again.."
        );
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while registering courses.");
    });
  selectedCourses = [];
  courseContainer
    .querySelectorAll(".courses-card > input")
    .forEach((element) => {
      element.checked = false;
    });
  totalCourseSelected.textContent = `Courses Selected: 0`;
  totalCreditHours.textContent = `Total Credit Hours: 0`;
  modal.style.display = "none";
  modal.style.visibility = "hidden";
});

const getStudentCourses = () => {
  const modal = document.querySelector(".modal-authorization");
  const modalTitle = document.querySelector(".modal-authorization .card > h2");
  const modalMessage = document.querySelector(".modal-authorization .card > p");
  const modalAction = document.querySelector(
    ".modal-authorization .card .action > input"
  );
  const token = getToken();
  fetch("/apis/v1/get-course/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token[0]}`,
    },
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        courseContainer.innerHTML = "";
        for (let element in response) {
          courseContainer.innerHTML += `
                        <div class="courses-card">
                    <div class="info">
                        <div class="upper">
                            <p>Code: ${response[element].CC}</p>
                            <p>CRH: ${response[element].CCHR}</p>
                        </div>
                        <p>${response[element].CT}</p>
                        <input type="hidden" id="ID" value="${response[element].ID}">
                        <input type="hidden" id="CCHR" value="${response[element].CCHR}">
                    </div>
                    <input type="checkbox" name="" id="">
                </div>
                    `;
        }
        addEvents();
      } else if (status == 401) {
        modal.style.display = "flex";
        modal.style.visibility = "visible";
        modalTitle.textContent = "Error";
        modalMessage.textContent =
          "You are not authorized to view this page. Please log in again.";
        modalAction.addEventListener("click", (e) => {
          window.location.href = "/login/";
        });
        modalAction.value = "Login";
      } else if (status == 400) {
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
      }
    });
};

let selectedCourses = [];
let totalCreditHoursCalculated = 0;
const addEvents = () => {
  const cardsChecks = courseContainer.querySelectorAll(".courses-card > input");
  const coursIDs = courseContainer.querySelectorAll(
    ".courses-card .info > input#ID"
  );
  const coursecrh = courseContainer.querySelectorAll(
    ".courses-card .info > input#CCHR"
  );
  const totalCourseSelected = document.getElementById("couuse-select");
  const totalCreditHours = document.getElementById("tcrh");
  cardsChecks.forEach((element, index) => {
    element.addEventListener("click", () => {
      let currentID = coursIDs[index].value;
      if (selectedCourses.includes(currentID)) {
        selectedCourses = selectedCourses.filter((IDs) => IDs !== currentID);
        totalCreditHoursCalculated -= parseInt(coursecrh[index].value);
      } else {
        selectedCourses.push(currentID);
        totalCreditHoursCalculated += parseInt(coursecrh[index].value);
      }
      totalCourseSelected.textContent = `Courses Selected: ${selectedCourses.length}`;
      totalCreditHours.textContent = `Total Credit Hours: ${totalCreditHoursCalculated}`;
    });
  });
};

getStudentCourses();
