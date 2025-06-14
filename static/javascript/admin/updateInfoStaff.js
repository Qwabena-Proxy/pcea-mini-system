const staffSurname = document.getElementById("staff-surname");
const otherName = document.getElementById("staff-otherName");
const staffDepartment = document.getElementById("staff-department");
const infoSubmitBtn = document.getElementById("info-submit-btn");

const existingToken = JSON.parse(window.localStorage.getItem("token"));
const userID = existingToken.studentID;

infoSubmitBtn.addEventListener("click", () => {
  const apiUrl = `/apis/v1/auth/update-staff-info/`;
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  let formData = new FormData();

  formData.append("staffSurname", staffSurname.value);
  formData.append("otherName", otherName.value);
  formData.append("department", staffDepartment.value);
  formData.append("staffID", userID);
  formData.append("csrfmiddlewaretoken", csrfToken);

  fetch(apiUrl, {
    method: "POST",
    body: formData,
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, data]) => {
      if (status == 200) {
        window.location.href = "/account-office/";
      } else {
        alert(data.message);
      }
    });
});
