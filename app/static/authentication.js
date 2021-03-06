import { sendRequest, getDataFromForm, clearInnerText } from "./utils.js";

const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");

loginForm.addEventListener("submit", login);
registerForm.addEventListener("submit", register);


function login(e) {
    e.preventDefault();
    const data = getDataFromForm(loginForm, {"username": "#username-login", "password": "#password-login"});
    let statusCode = null;

    sendRequest("POST", "/login", data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        console.log(statusCode);
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
    clearInnerText("#register-success", "#register-errors");
    const data = getDataFromForm(registerForm, {
        "username": "#username-register",
        "password1": "#password1-register",
        "password2": "#password2-register",
        "email": "#email-register"
    });
    let statusCode = null;


    sendRequest("POST", "/register", data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if(statusCode == 201) {
            successfulRegistration(res);
        }
        else {
            failedRegistration(res);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulRegistration(res) {
    registerForm.reset();
    clearInnerText("#register-errors");
    document.querySelector("#register-success").innerText = "Your account has been created successfully.";
}


function failedRegistration(res) {
    document.querySelector("#register-errors").innerText = res["error"];
}
