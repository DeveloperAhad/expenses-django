const passwordHandler = document.querySelector('#password-handler');
passwordHandler.addEventListener('click',() => {

});




const usernameField = document.querySelector('#username');
const usernameMsg = document.querySelector('#username-check-msg');
usernameField.addEventListener('keyup', e => {
    let usernameVal = e.target.value;
    console.log(e);

    if(usernameVal.length > 0){
        fetch("http://127.0.0.1:8000/accounts/username-check", {
            method: "POST",
            body: JSON.stringify({
                'username': usernameVal
            })
        }).then(res => res.json()).then(data => {
            if(data.username_error) {
                e.target.classList.remove('is-valid');
                e.target.classList.add('is-invalid');
                console.log(data.username_error);
                usernameMsg.innerText = data.username_error;
            } else {
                e.target.classList.remove('is-invalid');
                e.target.classList.add('is-valid');
            }
        })
    }
})
