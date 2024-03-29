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