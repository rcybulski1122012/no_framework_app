const editToDoListForm = document.querySelector("#edit-todolist-form");

editToDoListForm.addEventListener("submit", editToDoList);

function editToDoList(e) {
    e.preventDefault();
    const data = getToDoListData()
    const id_ = Number(document.querySelector("#content").dataset.id)
    // ajdust get*Data to return object instead of json
    sendPostRequest(`/update_todolist/${id_}`, data);
}

function getToDoListData() {
    const data = {
        name: editToDoListForm.querySelector("#todolist-name").value,
        description: editToDoListForm.querySelector("#todolist-description").value,
        id_: Number(document.querySelector("#content").dataset.id),
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