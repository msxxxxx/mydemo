function login(e) {
    e.preventDefault();
    $.ajax(
    {
        url: '/signin',
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            email: this.email.value,
            password: this.password.value
        }),
        success: function (data) {
            localStorage.setItem(
                "user_name", data.user_name
            );
            localStorage.setItem(
                "access_token", data.access_token
            );
            localStorage.setItem(
                "refresh_token", data.refresh_token
            );
            localStorage.setItem(
                "token_type", data.token_type
            );
//            document.cookie="access_token=Bearer " + data.access_token + ";";
            document.cookie="access_token=Bearer " + data.access_token + "; SameSite=Strict; Secure";
//            document.cookie = "name=oeschger; SameSite=None; Secure";
//            alert("this is document.cookie: " + document.cookie);
            window.location.assign('/cases')
        },
        error: function (data) {
            if (data.responseJSON.detail === "user not found") {
                let loginForm = document.getElementById("loginForm")
                let emailLabel = document.getElementById("emailLabel")
                emailLabel.innerHTML = "User Not Found";
                loginForm.email.className = "form-control border-warning"
            }
        }
    })
}

$("#loginForm").on("submit", login)

function register(e) {
    e.preventDefault();
    $.ajax(
    {
        url: '/signup',
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(
        {
            email: this.login.value,
            password: this.pass.value,
            confirm_password: this.conf_pass.value
        }),
        success: function (data) {
            window.location.assign('/login')
        },
        error: function (data) {
            alert("error")
            window.location.assign('/register')
        }
    })
}

$("#registerForm").on("submit", register)

function Form(e) {
    e.preventDefault();
    $.ajax(
    {
        url: '/api/v1/cases',
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(
        {
            title: this.title.value,
            body: this.body.value
            }),
        success: function(data) {
            console.log(data)
            alert("Case Added!");
            window.location = "/cases/list/";
        }
        })
    }

function FormC(e) {
    e.preventDefault();
    pathname = window.location.pathname;
    caseID = pathname.split('/')[3]
    $.ajax(
    {
        url: '/api/v1/cases/' + caseID + '/comment',
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(
        {
            text: this.text.value,
            }),
        success: function(data) {
            console.log(data)
            alert("Comment Added!");
            window.location = "/cases/list/" + caseID;
        }
        })
    }

$("#CommentForm").on("submit", FormC)
$("#CaseForm").on("submit", Form)