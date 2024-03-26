function Form(e): {
    e.preventDefault();
    $.ajax(
    {
        url: '/api/v1/cases',
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: Json.stringify(
        {
            title: this.title.value,
            slug: this.slug.value,
            body: this.body.value
            }),
        success: function {
            console.log(data)
        }
        })
    }

$("#CaseForm").on("submit", Form)