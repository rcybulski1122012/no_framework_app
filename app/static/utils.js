function sendRequest(method, path, data=null) {
    const options = {
        method: method,
    };
    if(data) {
        const stringified = JSON.stringify(data);
        options.headers = {
            "Content-Type": "application/json",
            "Content-Length": stringified.length
        }
        options.body = stringified
    }
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


export {sendRequest, getDataFromForm}