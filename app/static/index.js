import { sendRequest, getDataFromForm, clearInnerText } from "./utils.js";

const toDoListsList = document.querySelector("#todolists-list");
const createToDoListForm = document.querySelector("#create-todolist-form");
const todolistTemplate = document.querySelector("#todolist-template").content.cloneNode(true);

createToDoListForm.addEventListener("submit", createToDoList);

buildList();


async function buildList() {
    const listsData = await getToDoLists();
    createToDoListHtmlElements(listsData);
}


async function getToDoLists() {
    const options = {"Cookie": document.cookie};
    const response = await fetch("/todolists", options);
    const result = await response.json();
    return result["todolists"];
}


function createToDoListHtmlElements(data) {
    data.forEach(createToDoListHtmlElement);
}


function createToDoListHtmlElement(el) {
    const todolist = todolistTemplate.querySelector(".todolist").cloneNode(true);
    todolist.dataset.id = el["id_"];
    todolist.querySelector(".edit-todolist").setAttribute("href", `/edit_todolist/${el["id_"]}`);
    todolist.querySelector(".todolist-name").innerText = el["name"];
    todolist.querySelector(".todolist-description").innerText = el["description"];
    todolist.querySelector(".delete-todolist").addEventListener("click", deleteToDoList);

    toDoListsList.append(todolist);
}


function createToDoList(e) {
    e.preventDefault();
    clearInnerText("#create-errors");
    const data = getDataFromForm(createToDoListForm, {"name": "#todolist-name", "description": "#todolist-description"})
    let statusCode = null;

    sendRequest("POST", "/create_todolist", data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if (statusCode == 201) {
            successfulToDoListCreation(res);
        }
        else {
            failedToDoListCreation(res);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulToDoListCreation(res) {
    createToDoListHtmlElement(res);
    createToDoListForm.reset();
    clearInnerText("#create-errors");
}


function failedToDoListCreation(res) {
    createToDoListForm.querySelector("#create-errors").innerText = res["error"];
}


function deleteToDoList(e) {
    const todolist = e.target.closest(".todolist");
    const id_ = Number(todolist.dataset.id);
    sendRequest("POST", `/delete_todolist/${id_}`, {})
    .then(res => {
        if(res.status == 200) {
            successfulToDoListDeletion(todolist);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulToDoListDeletion(todolist) {
    todolist.remove();
}
