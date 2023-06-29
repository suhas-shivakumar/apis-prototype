function prototype() {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = "";
    let params = { "client_id": localStorage.client_id, "client_secret": localStorage.client_secret };
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];
            form.appendChild(hiddenField);
        }
    }
    document.body.appendChild(form);
    form.submit();
}