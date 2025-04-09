const authEmail = document.getElementById("auth-email");
const authPassword = document.getElementById("auth-password");
const authButton = document.getElementById("auth-btn");


authButton.addEventListener("click", () => {
    const address= 'http://127.0.0.1:8000'
    const apiUrl= `/apis/v1/auth/login/`;
    const email = authEmail.value.trim();
    const password = authPassword.value.trim();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let formData= new FormData();

    formData.append("password", password)
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append("email", email)

    fetch(apiUrl,{
        method: 'POST',
        body: formData,
    }).then(response => Promise.all([response.status, response.json()])).
    then(([status, data]) => {
        if (status == 200) {
            console.log(data)
            if(data.updateRequired){
                const token= {
                    'accessToken': data.access,
                    'refreshToken': data.refresh,
                    'email': data.email,
                    'studentID': data.studentID
                }
                window.localStorage.setItem('token', JSON.stringify(token))
                window.location.href= `${address}/students/update-info/`
            }else{
                window.location.href= `${address}/students/dashboard/`
            }
        }
        else{
            console.log(data)
            alert("Failed to login, please check your email and password.");
        }
    }).catch(err => console.error(err))

})