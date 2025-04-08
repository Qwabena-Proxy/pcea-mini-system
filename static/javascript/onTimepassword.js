const newPass= document.getElementById("new-password");
const confirmPass= document.getElementById("confirm-new-password");
const userEmail= document.getElementById("email");
const submitBtn= document.getElementById("submit-btn");

const passwordValidation= (e) => {
    if (newPass.value !== confirmPass.value) {
        return false;
    }
}

submitBtn.addEventListener("click", (e) => {
    if (passwordValidation(e)) {
        const newPassword= newPass.value;
        const address= 'http://172.20.10.3:8000/'
        const apiUrl= `${address}/apis/v1/create-student-password`;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let formData= new FormData();

        formData.append("password", newPassword.value)
        formData.append("csrfmiddlewaretoken", csrfToken);
        formData.append("email", userEmail.value)
        fetch(apiUrl,{
            method: 'POST',
            body: formData,
        }).then(response => response.json()).
        then(response => {
            console.log(response)
        }).catch(err => console.error(err))

    }
    else {
        alert("Passwords do not match!");
    }
});