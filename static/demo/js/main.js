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
                "access_token", data.access_token
            );
            localStorage.setItem(
                "refresh_token", data.refresh_token
            );
            localStorage.setItem(
                "token_type", data.token_type
            );
//            Cookie.setItem(
//                "refresh_token", data.refresh_token
//            );
//            cookies.set({
//                name: "access_token",
//                value: data.access_token
//            })
//            document.cookie="test cookie";
            document.cookie="access_token=Bearer " + data.access_token + "; SameSite=None";
            alert("this is document.cookie: " + document.cookie);
            window.location.assign('/cases')
//            setCookies: "lkfh89asdhjahska7al446dfg5kgfbfgdhfdbfgcvbcbc dfskljvdfhpl"
//            document.cookie="mySite=localhost; expires=Thu, 18 Dec 2015 12:00:00 UTC; path=/ SameSite=None;"
//            const cookie = require('cookie');
//            const token = data.access_token;
//            const secureCookie = true;
//            const httpOnlyCookie = true;
//            const cookieOptions = {
//            secure: secureCookie,
//            httpOnly: httpOnlyCookie,
//            };
//            const cookieString = cookie.serialize(data.access_token, token, cookieOptions);
//            res.setHeader('Set-Cookie', cookieString);
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