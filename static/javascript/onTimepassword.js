const newPass= document.getElementById("new-password");
const confirmPass= document.getElementById("confirm-new-password");
const userEmail= document.getElementById("email");
const submitBtn= document.getElementById("submit-btn");

const passwordValidation= (e) => {
    console.log(newPass.value, confirmPass.value)
    if (newPass.value === confirmPass.value) {
        return true;
    }
}

submitBtn.addEventListener("click", (e) => {
    if (passwordValidation(e)) {
        
        const address= 'http://127.0.0.1:8000'
        const apiUrl= `/apis/v1/create-student-password/`;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let formData= new FormData();

        formData.append("password", newPass.value)
        formData.append("csrfmiddlewaretoken", csrfToken);
        formData.append("email", userEmail.value)
        console.log(formData.get("password"))

        fetch(apiUrl,{
            method: 'POST',
            body: formData,
        }).then(response => response.json()).
        then(response => {
            if (response.message === "Success") {
                alert("Password changed successfully!");
                window.location.href = `/login/`;
            }
            else{
                alert("Password change failed!");
            }
        }).catch(err => console.error(err))

    }
    else {
        alert("Passwords do not match!");
    }
});