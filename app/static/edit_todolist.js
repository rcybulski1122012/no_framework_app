import { sendRequestWithData, getDataFromForm } from "./utils.js";

const editToDoListForm = document.querySelector("#edit-todolist-form");

editToDoListForm.addEventListener("submit", editToDoList);

function editToDoList(e) {
    e.preventDefault();
    const data = getDataFromForm(editToDoListForm, {"name": "#todolist-name", "description": "#todolist-description"})
    const id_ = document.querySelector("#content").dataset.id
    sendRequestWithData("POST", `/update_todolist/${id_}`, data);   // Should be post?
}