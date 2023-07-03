function prototype() {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = "";
    const hiddenField = document.createElement('input')
    hiddenField.type = 'hidden'
    hiddenField.name = "csrfmiddlewaretoken"
    hiddenField.value = document.getElementsByName('csrfmiddlewaretoken')[0].value
    form.appendChild(hiddenField)
    document.body.appendChild(form);
    form.submit();
}