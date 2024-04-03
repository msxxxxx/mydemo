//function loadCases() {
//    $.ajax({
//        url: "/cases/",
//        method: "GET",
//        dataType: "json",
//        headers: {
//            Authorization: `${localStorage.getItem("token_type")} ${localStorage.getItem("access_token")}`
//        },
//        success: function (data) {
//            console.log(data)
//            alert("Case Added!");
//            window.location = "/cases/list/";
//        },
//        error: function (data) {
//            refreshToken(loadFinanceList)
//        }
//    })
//}

function login(e) {
    e.preventDefault();
    $.ajax({
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
//            setRequestHeader('Authorization', data.access_token);
            window.location.assign('/cases');
//            alert("ok")
//            window.location = "/cases/list/";
//            loadCases()
//            document.location.replace()

        },
        error: function (data) {
            if (data.responseJSON.detail === "user not found") {
                let loginForm = document.getElementById("loginForm")
                let emailLabel = document.getElementById("emailLabel")
                emailLabel.innerHTML = "User Not Found";
                loginForm.email.className = "form-control border-warning"
            }
        }
    });
//    $.ajax({
//        url: "/cases/",
//        method: "GET",
//        dataType: "json",
//        headers: {
//            Authorization: `${localStorage.getItem("token_type")} ${localStorage.getItem("access_token")}`
//        },
//        success: function (data) {
//        },
//        error: function (data) {
//            refreshToken(loadFinanceList)
//        }
//    })
}

//$(document).ready(function () {
//    let accessToken = localStorage.getItem("access_token");
//    let tokenType = localStorage.getItem("token_type");
//    console.log(accessToken, tokenType)
//
//    if ((accessToken === null || tokenType == null) && document.location.pathname !== "/login") {
//        document.location.replace("/login")
//    } else if (document.location.pathname !== "/login") {
//        loadCases();
//        alert("test")
//    }
//})

$("#loginForm").on("submit", login)

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