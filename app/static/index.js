const toDoListsList = document.querySelector("#todolists-list");
const createToDoListForm = document.querySelector("#create-todolist-form")

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
    const h3 = document.createElement("h3");
    const p = document.createElement("p");
    const hr = document.createElement("hr");

    toDoList.classList.add("todolist");
    toDoList.dataset.id = el["id_"];
    h3.innerText = el["name"];
    p.innerText = el["description"];

    toDoList.append(h3);
    toDoList.append(p);
    toDoList.append(hr);
    toDoListsList.append(toDoList);
}


function createToDoList(e) {
    e.preventDefault();
    const data = getToDoListData()
    let statusCode = null;

    sendPostRequest("/create_todolist", data)
    .then(res => {
        statusCode = res.status;
        return res
    })
    .then(res => res.json())
    .then(createToDoListHtmlElement);

    createToDoListForm.reset();
}

function getToDoListData() {
    const data = {
        name: createToDoListForm.querySelector("#todolist-name").value,
        description: createToDoListForm.querySelector("#todolist-description").value
    }

    return JSON.stringify(data)
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