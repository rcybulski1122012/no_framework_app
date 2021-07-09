import { sendRequest, getDataFromForm } from "./utils.js";

const editToDoListForm = document.querySelector("#edit-todolist-form");
const createTaskForm = document.querySelector("#create-task-form");
const tasksList = document.querySelector("#tasks-list");
const taskTemplate = document.querySelector("#task-template").content.cloneNode(true);

const id_ = document.querySelector("#content").dataset.id;

editToDoListForm.addEventListener("submit", editToDoList);
createTaskForm.addEventListener("submit", createTask);

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
    task.dataset.todolist_id = id_;
    task.dataset.id = el["id_"];
    task.querySelector(".delete-task-button").addEventListener("click", deleteTask)
    task.querySelector(".task-content").innerText = el["content"];
    tasksList.append(task);
}


function createTask(e) {
    e.preventDefault();
    const data = getDataFromForm(createTaskForm, {"content": "#task-content"});
    data.todolist_id = id_;
    let statusCode = null;

    sendRequest("POST", "/create_task", data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if (statusCode == 201) {
            createTaskHtmlElement(res);
            createTaskForm.reset();
        }
        else {
            createTaskForm.querySelector("#create-task-errors").innerText = res["error"];
        }
    })
    .catch(error => console.log("Error", error));
}


function deleteTask(e) {
    const task = e.target.closest(".task");
    const taskId = task.dataset.id

    sendRequest("POST", `/delete_task/${taskId}`)
    .then(res => {
        if(res.status == 200) {
            task.remove();
        }
    })
}