const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const emailSingleAccount = document.getElementById("email");
const levelInputElement = document.getElementById("level-input");
const programInputElement = document.getElementById("program-input");
const programMinorInputElement = document.getElementById("program-input-mn");
const courseProgramInput = document.getElementById("course-program");
const departmentInputElement = document.getElementById("department-input");
const singleDepartmentUserCreate = document.getElementById("department-email");
const upgDiv = document.getElementById("upg");
const fileInputBulkAccountActivation = document.getElementById(
  "account-activation-b"
);
const bulkActivationBtn = document.getElementById("send-bulk");

//Btns
const singleAccountSendBtn = document.getElementById("send");
const singleAccountClearBtn = document.getElementById("clear");
const signleDepartmentSendBtn = document.getElementById("department-send");
const singleDepartmentClearBtn = document.getElementById("department-clear");
const departmentSubmit = document.getElementById("submit-department");
const departmentClear = document.getElementById("clear-department");
const levelSubmit = document.getElementById("submit-level");
const levelClear = document.getElementById("clear-level");
const programSubmit = document.getElementById("submit-program");
const progamClear = document.getElementById("clear-program");
const courseSubmit = document.getElementById("submit-course");
const courseClear = document.getElementById("clear-course");
const makeChanges = document.getElementById("settings-make-change");
const saveChanges = document.getElementById("settings-save-change");
const addAcademicYear = document.getElementById("add-academic-year");
const saveAcademicYear = document.getElementById("save-academic-year");

// const address = "http://127.0.0.1:8000";
const singleStudentCreateApiUrl = `/apis/v1/create-student/`;
const bulkAccountActivationApiUrl = `/apis/v1/bulk-account-activation/`;
const levelCreateApiUrl = `/apis/v1/create-level/`;
const programCreateApiUrl = `/apis/v1/create-program/`;
const courseCreateApiUrl = `/apis/v1/create-course/`;
const getupdate = `/apis/v1/get-update`;
const settingsApiUrl = `/apis/v1/create-settigns/`;
const singleDepartmentCreateApiUrl = `/apis/v1/create-department/`;
const singleDepartmentUserCreateApiUrl = `/apis/v1/create-staff/`;

const clearBtns = [
  levelClear,
  progamClear,
  singleAccountClearBtn,
  departmentClear,
  singleDepartmentClearBtn,
];
const clearInputs = [
  levelInputElement,
  programInputElement,
  emailSingleAccount,
  departmentInputElement,
  singleDepartmentUserCreate,
];

clearBtns.forEach((element, index) => {
  element.addEventListener("click", (e) => {
    clearElement(clearInputs[index]);
    clearInputs[index].focus();
  });
});

// Eventlisteners
levelSubmit.addEventListener("click", (e) => {
  e.preventDefault();
  if (levelInputElement.value === "") {
    alert("Please enter a level name.");
    return;
  }
  levelSubmitHandler(e);
  clearElement(levelInputElement);
});

programSubmit.addEventListener("click", (e) => {
  e.preventDefault();
  if (programInputElement.value === "") {
    alert("Please enter a program name.");
    return;
  }
  programSubmitHandler(e);
  clearElement(programInputElement);
});

courseSubmit.addEventListener("click", (e) => {
  courseSubmitHandler(e);
});

makeChanges.addEventListener("click", (e) => {
  enableSemesterSettingsHandler(e);
});

saveChanges.addEventListener("click", (e) => {
  const settingsID = document.getElementById("settingsID");
  const semester1Radio = document.getElementById("ss1");
  const semester2Radio = document.getElementById("ss2");
  let formData = new FormData();
  formData.append("settings_id", settingsID.value);
  formData.append("current_semester", semester1Radio.checked ? 1 : 2);
  fetch(`${settingsApiUrl}`, {
    method: "PUT",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => Promise.all([response.status, response.json()]))
    .then(([status, response]) => {
      if (status == 200) {
        alert("Semester changes was successful");
        reloadPage();
      }
      getSettings(); // Handle response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  disableSemesterSettingsHandler(e);
});

addAcademicYear.addEventListener("click", (e) => {
  addAcademicYearHandler(e);
});

saveAcademicYear.addEventListener("click", (e) => {
  saveAcademicYearHandler(e);
});

bulkActivationBtn.addEventListener("click", (e) => {
  bulkAccountHandler(e);
});

departmentSubmit.addEventListener("click", (e) => {
  departmentSubmitHandler(e);
  clearElement(departmentInputElement);
});

signleDepartmentSendBtn.addEventListener("click", (e) => {
  departmentUserCreateHandler(e);
  clearElement(singleDepartmentUserCreate);
});

const clearElement = (e) => {
  e.value = "";
  e.focus();
};

// Handlers

const levelSubmitHandler = (e) => {
  let formData = new FormData();
  formData.append("name", levelInputElement.value);
  fetch(`${levelCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message); // Handle response
      reloadPage();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const programSubmitHandler = (e) => {
  let formData = new FormData();
  formData.append("name", programInputElement.value);
  formData.append("minor", programMinorInputElement.value);
  fetch(`${programCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message); // Handle response
      reloadPage();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

// courseProgramInput.addEventListener("input", function () {
//   if (this.value.trim() === "General Course") {
//     upgDiv.style.display = "block";
//   } else {
//     upgDiv.style.display = "none";
//   }
// });

const courseSubmitHandler = (e) => {
  const courseCodeInputElement = document.getElementById("course-code");
  const courseTitleInputElement = document.getElementById("course-title");
  const courseCreditInputElement = document.getElementById("course-credit");
  const courseLevelInputElement = document.getElementById("course-level");
  const courseProgramInputElement = document.getElementById("course-program");
  const upCCheckbox = document.getElementById("upC");
  const semesterValue = document.querySelector(
    'input[name="semester"]:checked'
  )?.value;
  e.preventDefault();
  if (
    courseCodeInputElement.value === "" ||
    courseTitleInputElement.value === "" ||
    courseCreditInputElement.value === "" ||
    courseLevelInputElement.value === "" ||
    courseProgramInputElement.value === "" ||
    !semesterValue
  ) {
    alert("Please fill in all fields.");
    return;
  }

  let formData = new FormData();
  formData.append("code", courseCodeInputElement.value);
  formData.append("name", courseTitleInputElement.value);
  formData.append("crh", courseCreditInputElement.value);
  formData.append("level", courseLevelInputElement.value);
  formData.append("semester", semesterValue);
  if (courseProgramInputElement.value === "General Course") {
    formData.append("isGeneral", true);
    formData.append("isJHS", !upCCheckbox.checked);
    // Do NOT append program
  } else {
    formData.append("program", courseProgramInputElement.value);
    formData.append("isGeneral", false);
    formData.append("isJHS", false);
  }
  fetch(`${courseCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => Promise.all([response.json(), response.status]))
    .then(([data, status]) => {
      if (status != 400) {
        alert(data.message);
      } else {
        alert(
          "The course code or course title exist already. Please check you data again"
        );
      }
      reloadPage();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const enableSemesterSettingsHandler = (e) => {
  const semester1Radio = document.getElementById("ss1");
  const semester2Radio = document.getElementById("ss2");

  [semester1Radio, semester2Radio].forEach((element) => {
    element.disabled = false;
  });
};

const disableSemesterSettingsHandler = (e) => {
  const semester1Radio = document.getElementById("ss1");
  const semester2Radio = document.getElementById("ss2");

  [semester1Radio, semester2Radio].forEach((element) => {
    element.disabled = true;
  });
};

const addAcademicYearHandler = (e) => {
  const showAcademicSettings = document.querySelector(".academic-settings");

  showAcademicSettings.style.display = "block";
};

const saveAcademicYearHandler = (e) => {
  const showAcademicSettings = document.querySelector(".academic-settings");
  const academicYear = document.getElementById("academic-year");
  const academicYearStart = document.getElementById("academic-year-start");
  const academicYearEnd = document.getElementById("academic-year-end");
  const levelTutions = document.querySelectorAll(
    ".tution > input[type='text']"
  );
  let formData = new FormData();
  formData.append("current_semester", 1);
  formData.append("academic_year", academicYear.value);
  formData.append("academic_year_start", academicYearStart.value);
  formData.append("academic_year_end", academicYearEnd.value);
  formData.append(
    "academic_year_levels",
    Array.from(document.querySelectorAll("#level-data option"))
      .map((option) => option.value)
      .join(",")
  );
  formData.append(
    "academic_year_levels_tution",
    Array.from(levelTutions)
      .map((input) => input.value)
      .join(",")
  );
  formData.append("active", true);
  fetch(`${settingsApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message); // Handle response
      reloadPage();
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  showAcademicSettings.style.display = "none";
};
singleAccountSendBtn.addEventListener("click", () => {
  let formData = new FormData();

  formData.append("email", emailSingleAccount.value);
  fetch(`${singleStudentCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      alert(response.message);
      reloadPage();
    })
    .catch((err) => console.error(err));
});

const bulkAccountHandler = (e) => {
  alert("Bulk activation request sent successfully.");
  if (fileInputBulkAccountActivation.files.length === 0) {
    alert("Please select a file to upload.");
    return;
  }
  let formData = new FormData();
  formData.append("file", fileInputBulkAccountActivation.files[0]);
  fetch(`${bulkAccountActivationApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      alert(response.message);
      reloadPage();
    })
    .catch((err) => console.error(err));
};

const departmentSubmitHandler = (e) => {
  e.preventDefault();
  const departmentName = departmentInputElement.value.trim();
  if (departmentName === "") {
    alert("Please enter a department name.");
    return;
  }
  let formData = new FormData();
  formData.append("name", departmentName);
  fetch(`/apis/v1/create-department/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message); // Handle response
      clearElement(departmentInputElement);
      reloadPage();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const departmentUserCreateHandler = (e) => {
  e.preventDefault();
  const departmentEmail = singleDepartmentUserCreate.value.trim();
  if (departmentEmail === "") {
    alert("Please enter account email.");
    return;
  }
  let formData = new FormData();
  formData.append("email", departmentEmail);
  fetch(`${singleDepartmentUserCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message); // Handle response
      clearElement(singleDepartmentUserCreate);
      reloadPage();
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const getlevel = () => {
  const levelList = document.getElementById("level-list");
  const programList = document.getElementById("program-list");
  const courseList = document.getElementById("course-list");
  const programDataList = document.getElementById("programs-data");
  const programDataListMn = document.getElementById("programs-data-mn");
  const levelDataList = document.getElementById("level-data");
  const tutionContainer = document.querySelector(".tution");
  levelList.innerHTML = "";
  programList.innerHTML = "";
  courseList.innerHTML = "";
  tutionContainer.innerHTML = "";

  fetch(`${getupdate}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((response) => {
      const level = response.level;
      const program = response.program;
      const course = response.course;
      for (const x of level) {
        if (x != "TestLevel") {
          levelList.innerHTML += `<li>${x}</li>`;
          levelDataList.innerHTML += `<option value="${x}"></option>`;
          tutionContainer.innerHTML += `<label for=academic-year-level-${x}">Fees for level ${x}</label>
                      <input type="text" name="" placeholder="level ${x} fees" id="academic-year-level-${x}"><br>`;
        }
      }
      for (const x of program) {
        if (x != "TestProgram") {
          programList.innerHTML += `<li>${x}</li>`;
          programDataList.innerHTML += `<option value="${x}"></option>`;
          programDataListMn.innerHTML += `<option value="${x}"></option>`;
        }
      }
      programDataList.innerHTML += `<option value="General Course"></option>`;
      for (const x of course) {
        courseList.innerHTML += `<li>${x}</li>`;
      }
    })
    .catch((err) => console.error(err));
}; //create-staff/

const getSettings = () => {
  fetch(`${settingsApiUrl}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      const settingsID = document.getElementById("settingsID");
      const academicYear = document.querySelector(".academic-y > p");
      const semester1 = document.getElementById("ss1");
      const semester2 = document.getElementById("ss2");

      const settings = data[0];
      settings.current_semester === 1
        ? (semester1.checked = true)
        : (semester2.checked = true);
      settingsID.value = settings.settings_id;
      academicYear.textContent = `Academic Year: ${settings.academic_year}`;

      // console.log(data); // Handle response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const reloadPage = () => {
  window.location.reload();
};

getSettings();
getlevel();
