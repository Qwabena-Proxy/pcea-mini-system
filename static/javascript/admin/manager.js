const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");
const levelInputElement = document.getElementById("level-input");
const programInputElement = document.getElementById("program-input");

//Btns
const singleAccountSendBtn = document.getElementById("send");
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

const address = "http://127.0.0.1:8000";
const singleStudentCreateApiUrl = `/apis/v1/create-student/`;
const levelCreateApiUrl = `/apis/v1/create-level/`;
const programCreateApiUrl = `/apis/v1/create-program/`;
const courseCreateApiUrl = `/apis/v1/create-course/`;
const getupdate = `/apis/v1/get-update`;
const settingsApiUrl = `/apis/v1/create-settigns/`;

const clearBtns = [levelClear, progamClear];
const clearInputs = [levelInputElement, programInputElement];

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
  disableSemesterSettingsHandler(e);
});

addAcademicYear.addEventListener("click", (e) => {
  addAcademicYearHandler(e);
});

saveAcademicYear.addEventListener("click", (e) => {
  saveAcademicYearHandler(e);
});

const clearElement = (e) => {
  e.value = "";
  e.focus();
};

// Handlers

const levelSubmitHandler = (e) => {
  let formData = new FormData();
  formData.append("name", levelInputElement.value);
  fetch(`${address}${levelCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Handle response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const programSubmitHandler = (e) => {
  let formData = new FormData();
  formData.append("name", programInputElement.value);
  fetch(`${address}${programCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Handle response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

const courseProgramInput = document.getElementById("course-program");
const upgDiv = document.getElementById("upg");

courseProgramInput.addEventListener("input", function () {
  if (this.value.trim() === "General Course") {
    upgDiv.style.display = "block";
  } else {
    upgDiv.style.display = "none";
  }
});

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
  alert(!upCCheckbox.checked);

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
  fetch(`${address}${courseCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Handle response
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
  fetch(`${address}${settingsApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Handle response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  console.log(
    academicYear.value,
    academicYearStart.value,
    academicYearEnd.value
  );
  levelTutions.forEach((element) => {
    console.log(element.value);
  });

  showAcademicSettings.style.display = "none";
};
singleAccountSendBtn.addEventListener("click", () => {
  const email = document.getElementById("email");
  let formData = new FormData();

  formData.append("email", email.value);
  fetch(`${address}${singleStudentCreateApiUrl}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      console.log(response);
    })
    .catch((err) => console.error(err));
});

const getlevel = () => {
  const levelList = document.getElementById("level-list");
  const programList = document.getElementById("program-list");
  const courseList = document.getElementById("course-list");
  const programDataList = document.getElementById("programs-data");
  const levelDataList = document.getElementById("level-data");
  const tutionContainer = document.querySelector(".tution");
  levelList.innerHTML = "";
  programList.innerHTML = "";
  courseList.innerHTML = "";
  tutionContainer.innerHTML = "";

  fetch(`${address}${getupdate}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((response) => {
      const level = response.level;
      const program = response.program;
      const course = response.course;
      for (const x of level) {
        levelList.innerHTML += `<li>${x}</li>`;
        levelDataList.innerHTML += `<option value="${x}"></option>`;
        tutionContainer.innerHTML += `<label for=academic-year-level-${x}">Fees for level ${x}</label>
                    <input type="text" name="" placeholder="level ${x} fees" id="academic-year-level-${x}"><br>`;
      }
      for (const x of program) {
        programList.innerHTML += `<li>${x}</li>`;
        programDataList.innerHTML += `<option value="${x}"></option>`;
      }
      programDataList.innerHTML += `<option value="General Course"></option>`;
      for (const x of course) {
        courseList.innerHTML += `<li>${x}</li>`;
      }
    })
    .catch((err) => console.error(err));
};

getlevel();
