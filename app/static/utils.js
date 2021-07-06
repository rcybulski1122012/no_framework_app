function sendRequestWithData(method, path, data) {
    const stringified = JSON.stringify(data);
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "Content-Length": stringified.length
        },
       body: stringified
    };
    return fetch(path, options);
}

function getDataFromForm(form, nameSelectorObj) {
    const result = {}
    for(const property in nameSelectorObj) {
        if (nameSelectorObj.hasOwnProperty(property)) {
            result[property] = form.querySelector(nameSelectorObj[property]).value;
        }
    }
    return result
}

export {sendRequestWithData, getDataFromForm}