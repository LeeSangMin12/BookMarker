$(document).ready(function () {
    listing();
});

function listing() {
    $.ajax({
        type: 'GET',
        url: '/movie',
        data: {},
        success: function (response) {
            let rows = response['movies']
            for (let i = 0; i < rows.length; i++) {
                let comment = rows[i]['comment']
                let title = rows[i]['title']
                let desc = rows[i]['desc']
                let image = rows[i]['image']
                let star = rows[i]['star']

                let star_image = '⭐'.repeat(star)

                let temp_html = ` <div class="col">
                                            <div class="card h-100">
                                                <img src="${image}"
                                                     class="card-img-top">
                                                <div class="card-body">
                                                    <h5 class="card-title">${title}</h5>
                                                    <p class="card-text">${desc}</p>
                                                    <p>${star_image}</p>
                                                    <p class="mycomment">${comment}</p>
                                                </div>
                                            </div>
                                        </div>`
                $('#cards-box').append(temp_html)
            }
            console.log(response['movies'])
        }
    })
}

function uploading() {
    let url = $('#url').val()
    let author = $('#author').val()
    let sum = $('#sum').val()
    let title = $('#title').val()
    let publisher = $('#publisher').val()


    $.ajax({
        type: 'POST',
        url: '/movie',
        data: {url_give: url, comment_give: comment, author_give: author, sum_give : sum, title_give : title, publisher_give : publisher},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}
