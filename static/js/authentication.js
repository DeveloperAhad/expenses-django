const passwordHandler = document.querySelector('#password-handler');
if(passwordHandler !== null) {
    passwordHandler.addEventListener('click',(e) => {
        const password = document.getElementById('password');
        const password2 = document.getElementById('password2');
        if (password.type === "password") {
            password.type = "text";
            if (password2 !== null) { 
                password2.type = "text";
            }
            e.target.innerText = 'Hide';
        } else {
            password.type = "password";
            if (password2 !== null) { 
                password2.type = "password";
            }
            e.target.innerText = 'Show';
        }
    });
}


const usernameField = document.querySelector('#username');
const usernameMsg = document.querySelector('#username-check-msg');
if(usernameField !== null && usernameMsg !== null) {
    usernameField.addEventListener('keyup', e => {
        let usernameVal = e.target.value;
        e.target.classList.add('is-invalid');
        emailMsg.innerText = 'checking!';

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
}


const emailField = document.querySelector('#email');
const emailMsg = document.querySelector('#email-check-msg');

if(emailField !== null) {
    emailField.addEventListener('keyup', e => {
        let emailVal = e.target.value;
        e.target.classList.add('is-invalid');
        emailMsg.innerText = 'checking!';

        if(emailVal.length > 0){
            fetch("http://127.0.0.1:8000/accounts/email-check", {
                method: "POST",
                body: JSON.stringify({
                    'email': emailVal
                })
            }).then(res => res.json()).then(data => {
                if(data.email_error) {
                    e.target.classList.remove('is-valid');
                    e.target.classList.add('is-invalid');
                    console.log(data.email_error);
                    emailMsg.innerText = data.email_error;
                } else {
                    e.target.classList.remove('is-invalid');
                    e.target.classList.add('is-valid');
                }
            })
        }
    })
}