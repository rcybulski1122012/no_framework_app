import { sendRequest, getDataFromForm } from "./utils.js";

const editToDoListForm = document.querySelector("#edit-todolist-form");
const createTaskForm = document.querySelector("#creat-task-form");
const tasksList = document.querySelector("#tasks-list");
const taskTemplate = document.querySelector("#task-template").content.cloneNode(true);

const id_ = document.querySelector("#content").dataset.id;

editToDoListForm.addEventListener("submit", editToDoList);

buildTasks();


function editToDoList(e) {
    e.preventDefault();
    const data = getDataFromForm(editToDoListForm, {"name": "#todolist-name", "description": "#todolist-description"})
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
        else {
            editToDoListForm.querySelector("#update-errors").innerText = "";
        }
    });
}


async function buildTasks() {
    const tasksData = await getTasksData();
    console.log(tasksData);
    createTasksHtmlElements(tasksData);
}


async function getTasksData() {
    const options = {"Cookie": document.cookie};
    const response = await fetch(`/tasks/${id_}`, options);
    const result = await response.json();
    return result["tasks"];
}

function createTasksHtmlElements(data) {
    data.forEach(createTaskHtmlElement);
}

function createTaskHtmlElement(el) {
  const task = taskTemplate.querySelector(".task").cloneNode(true);
  task.dataset.id = id_;
  task.querySelector(".task-content").innerText = el["content"];
  tasksList.append(task);
}