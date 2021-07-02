const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");

loginForm.addEventListener("submit", login);
registerForm.addEventListener("submit", register);


function login(e) {
    e.preventDefault();
    const data = getLoginData();
    let statusCode = null;

    const res = sendPostRequest("/login", data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if(statusCode === 201)
            successLogin(res);
        else
            failedLogin(res)
    })
    .catch(error => console.log("Error", error));
}


function getLoginData() {
    const data = {
        username: loginForm.querySelector("#username-login").value,
        password: loginForm.querySelector("#password-login").value
    };

    return JSON.stringify(data);
}


function sendPostRequest(path, data) {
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Content-Length": data.length
        },
       body: data
    };
    return fetch(path, options);
}


function successLogin(res) {
    document.cookie = "session_id=" + res["session_id"] + ";";
    window.location.reload("/");
}


function failedLogin(res){
    loginForm.querySelector("#login-errors").innerText = res["error"];
}


function register(e) {
    e.preventDefault()
    clearRegisterMessagesDivs();
    const data = getRegisterData();
    let statusCode = null;


    sendPostRequest("/register", data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if(statusCode == 201)
            successRegister(res);
        else
            failedRegister(res);
    })
    .catch(error => console.log("Error", error));
}


function clearRegisterMessagesDivs() {
    document.querySelector("#register-success").innerText = "";
    document.querySelector("#register-errors").innerText = "";
}


function getRegisterData() {
    const data = {
        username: registerForm.querySelector("#username-register").value,
        password1: registerForm.querySelector("#password1-register").value,
        password2: registerForm.querySelector("#password2-register").value,
        email: registerForm.querySelector("#email-register").value,
    };

    return JSON.stringify(data);
}


function successRegister(res) {
    registerForm.reset();
    document.querySelector("#register-success").innerText = "Your account has been created successfully.";
}


function failedRegister(res) {
    document.querySelector("#register-errors").innerText = res["error"];
}
