import { sendRequest, getDataFromForm, clearInnerText } from "./utils.js";

const editToDoListForm = document.querySelector("#edit-todolist-form");
const createTaskForm = document.querySelector("#create-task-form");
const tasksList = document.querySelector("#tasks-list");
const taskTemplate = document.querySelector("#task-template").content.cloneNode(true);

const id_ = document.querySelector("#content").dataset.id;

editToDoListForm.addEventListener("submit", editToDoList);
createTaskForm.addEventListener("submit", createTask);

buildTasks();


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
    if(el["is_done"]) {
        task.classList.add("task-done");
    }
    task.querySelector(".delete-task-button").addEventListener("click", deleteTask);
    task.querySelector(".task-content").innerText = el["content"];
    task.querySelector(".done-task-button").addEventListener("click", markAsDone);
    tasksList.append(task);
}


function editToDoList(e) {
    e.preventDefault();
    const data = getDataFromForm(editToDoListForm, {"name": "#todolist-name", "description": "#todolist-description"});
    let statusCode = null;

    sendRequest("POST", `/update_todolist/${id_}`, data)
    .then(res => {
        statusCode = res.status;
        return res;
    })
    .then(res => res.json())
    .then(res => {
        if(statusCode == 200) {
            successfulUpdate()
        }
        else {
            failedUpdate(res);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulUpdate() {
    clearInnerText("#update-errors");
}


function failedUpdate(res) {
    editToDoListForm.querySelector("#update-errors").innerText = res["error"];
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
            successfulTaskCreation(res);
        }
        else {
            failedTaskCreation(res);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulTaskCreation(res) {
    createTaskHtmlElement(res);
    createTaskForm.reset();
    clearInnerText("#create-task-errors");
}


function failedTaskCreation(res) {
    createTaskForm.querySelector("#create-task-errors").innerText = res["error"];
}


function deleteTask(e) {
    const task = e.target.closest(".task");
    const taskId = task.dataset.id;

    sendRequest("POST", `/delete_task/${taskId}`)
    .then(res => {
        if(res.status == 200) {
            successfulTaskDeletion(task);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulTaskDeletion(task) {
    task.remove();
}


function markAsDone(e) {
    const task = e.target.closest(".task");
    const taskId = task.dataset.id;

    sendRequest("POST", `/mark_task_as_done/${taskId}`)
    .then(res => {
        if(res.status == 200) {
            successfulTaskMarking(task);
        }
    })
    .catch(error => console.log("Error", error));
}


function successfulTaskMarking(task) {
     task.classList.add("task-done");
}
