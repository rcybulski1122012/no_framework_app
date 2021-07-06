import { sendRequestWithData, getDataFromForm } from "./utils.js";

const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");

loginForm.addEventListener("submit", login);
registerForm.addEventListener("submit", register);


function login(e) {
    e.preventDefault();
    const data = getDataFromForm(loginForm, {"username": "#username-login", "password": "#password-login"});
    let statusCode = null;

    const res = sendRequestWithData("POST", "/login", data)
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
    const data = getDataFromForm(registerForm, {
        "username": "#username-register",
        "password1": "#password1-register",
        "password2": "#password2-register",
        "email": "#email-register"
    });
    let statusCode = null;


    sendRequestWithData("POST", "/register", data)
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


function successRegister(res) {
    registerForm.reset();
    document.querySelector("#register-success").innerText = "Your account has been created successfully.";
}


function failedRegister(res) {
    document.querySelector("#register-errors").innerText = res["error"];
}
