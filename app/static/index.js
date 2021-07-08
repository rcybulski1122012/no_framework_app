import { sendRequest, getDataFromForm } from "./utils.js";

const toDoListsList = document.querySelector("#todolists-list");
const createToDoListForm = document.querySelector("#create-todolist-form");

createToDoListForm.addEventListener("submit", createToDoList);

buildList();


async function buildList() {
    const listsData = await getToDoLists();
    createToDoListHtmlElements(listsData);
}


async function getToDoLists() {
    const options = getRequestHeaders();
    const response = await fetch("/todolists", options);
    const result = await response.json();
    return result["todolists"];
}


function getRequestHeaders() {
    return {
        "Cookie": document.cookie,
    }
}


function createToDoListHtmlElements(data) {
    return data.forEach(createToDoListHtmlElement);
}


function createToDoListHtmlElement(el) {
    const toDoList = document.createElement("div");
    const deleteButton = document.createElement("button");
    const editButton = document.createElement("a");
    const h3 = document.createElement("h3");
    const p = document.createElement("p");
    const hr = document.createElement("hr");

    toDoList.classList.add("todolist");
    toDoList.dataset.id = el["id_"];
    deleteButton.innerText = "Delete"
    deleteButton.classList.add("btn", "btn-danger");
    editButton.innerText = "Edit"
    editButton.classList.add("btn", "btn-info");
    editButton.setAttribute("href", `/edit_todolist/${el["id_"]}`)
    h3.innerText = el["name"];
    p.innerText = el["description"];

    deleteButton.addEventListener("click", deleteToDoList);

    toDoList.append(h3);
    toDoList.append(p);
    toDoList.append(deleteButton);
    toDoList.append(editButton);
    toDoList.append(hr);
    toDoListsList.append(toDoList);
}


function createToDoList(e) {
    e.preventDefault();
    clearMessagesDivs();
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
            createToDoListHtmlElement(res);
            createToDoListForm.reset();
        }
        else {
            createToDoListForm.querySelector("#create-errors").innerText = res["error"];
        }
    })
    .catch(error => console.log("Error", error));
}


function clearMessagesDivs() {
    createToDoListForm.querySelector("#create-errors").innerText = "";
}


function deleteToDoList(e) {
    const todolist = e.target.closest(".todolist");
    const id_ = Number(todolist.dataset.id);
    sendRequest("POST", `/delete_todolist/${id_}`, {})
    .then(res => {
        if(res.status == 200) {
            todolist.remove();
        }
    });
}