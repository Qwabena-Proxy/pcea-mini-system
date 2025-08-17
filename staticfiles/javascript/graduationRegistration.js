const submitIndexNumber = document.getElementById("submit-id-btn");
const indexNumberInput = document.getElementById("index-number");
const submitDetails = document.getElementById("submit-details-btn");
const fullName = document.getElementById("name");
const indexNumber = document.getElementById("index-number-f");
const program = document.getElementById("program");
const gpa = document.getElementById("gpa");
const gpaClass = document.getElementById("class");

let currentIndex;

submitIndexNumber.addEventListener("click", (e) => {
  if (indexNumberInput.value) {
    currentIndex = indexNumberInput.value;
    changeVerificationStatus();
    let formData = new FormData();
    formData.append("indexNumber", indexNumberInput.value.trim());
    fetch("/graduation-registration/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        changeVerificationStatus();
        if (response.code == 200) {
          const sections = document.querySelectorAll("section");
          sections.forEach((x, i) => {
            if (x.classList.contains("active")) {
              x.classList.remove("active");
            }
            if (i == 1) {
              document.getElementById("server-response").textContent = "";
              x.classList.add("active");
            }
          });
        } else {
          document.getElementById("server-response").textContent =
            response.message;
        }
      });
  } else {
    alert("Please enter your index number");
  }
});

submitDetails.addEventListener("click", (e) => {
  if (
    fullName.value &&
    indexNumber.value &&
    program.value &&
    gpa.value &&
    gpaClass.value
  ) {
    if (indexNumber.value == currentIndex) {
      changeRegistrationStatus();
      let formData = new FormData();
      formData.append("name", fullName.value);
      formData.append("indexNumber", indexNumber.value);
      formData.append("program", program.value);
      formData.append("gpa", gpa.value);
      formData.append("gpaClass", gpaClass.value);
      fetch("/graduation-registration/register", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((response) => {
          changeRegistrationStatus();
          if (response.code == 200) {
            alert(response.message);
            const sections = document.querySelectorAll("section");
            sections.forEach((x, i) => {
              if (x.classList.contains("active")) {
                x.classList.remove("active");
              }
              if (i == 0) {
                document.getElementById("server-response-final").textContent =
                  "";
                x.classList.add("active");
              }
            });
          } else {
            document.getElementById("server-response-final").textContent =
              response.message;
          }
        });
    } else {
      alert("Please the right index number");
    }
  } else {
    alert("Please provide all the details");
  }
});

function changeVerificationStatus() {
  const icon = submitIndexNumber.querySelector("span > i");
  const iconContainer = submitIndexNumber.querySelector("span.icon");
  const textContainer = submitIndexNumber.querySelector("span.text");
  if (icon.classList.contains("ri-send-plane-line")) {
    icon.classList.replace("ri-send-plane-line", "ri-loader-4-line");
    iconContainer.style.animationName = "loader";
    textContainer.textContent = "Verifying";
  } else {
    indexNumberInput.value = "";
    icon.classList.replace("ri-loader-4-line", "ri-send-plane-line");
    iconContainer.style.animationName = "submit";
    textContainer.textContent = "Submit";
  }
}

function changeRegistrationStatus() {
  const icon = submitDetails.querySelector("span > i");
  const iconContainer = submitDetails.querySelector("span.icon");
  const textContainer = submitDetails.querySelector("span.text");
  if (icon.classList.contains("ri-send-plane-line")) {
    icon.classList.replace("ri-send-plane-line", "ri-loader-4-line");
    iconContainer.style.animationName = "loader";
    textContainer.textContent = "Processing";
  } else {
    fullName.value = "";
    indexNumber.value = "";
    program.value = "";
    gpa.value = "";
    gpaClass.value = "";
    document.getElementById("server-response-final").textContent = "";
    icon.classList.replace("ri-loader-4-line", "ri-send-plane-line");
    iconContainer.style.animationName = "submit";
    textContainer.textContent = "Submit";
  }
}
