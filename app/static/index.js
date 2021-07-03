const toDoListsList = document.querySelector("#todolists-list");

async function buildList() {
    const listsData = await getToDoLists();
    console.log(listsData);
    const htmlElements = createToDoListHtmlElements(listsData);
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
    return data.forEach(el => {
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
    });
}

buildList();