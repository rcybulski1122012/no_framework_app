import { sendRequest, getDataFromForm } from "./utils.js";

const editToDoListForm = document.querySelector("#edit-todolist-form");

editToDoListForm.addEventListener("submit", editToDoList);

function editToDoList(e) {
    e.preventDefault();
    const data = getDataFromForm(editToDoListForm, {"name": "#todolist-name", "description": "#todolist-description"})
    const id_ = document.querySelector("#content").dataset.id
    let statusCode = null;
    sendRequest("POST", `/update_todolist/${id_}`, data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if(statusCode != 200) {
            editToDoListForm.querySelector("#update-errors").innerText = res["error"];
        }
    });
}