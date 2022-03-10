function getBookInfor() {
    $('#show_box').show()
    let url = $('#url').val()
    $.ajax({
        type: 'POST',
        url: '/getBookInfor',
        data: {url_give: url},
        success: function (response) {
            let bookTitle = response['showBook']['bookTitle']
            let bookAuthor = response['showBook']['bookAuthor']
            let bookUrl = response['showBook']['bookUrl']
            let temp_html = `<div class="col mb-5">
                                            <div class="card h-100">
                                                <!-- Product image-->
                                                <img class="card-img-top" src="${bookUrl}" alt="..." />
                                                <!-- Product details-->
                                                <div class="card-body p-4">
                        
                        
                                                    <div class="text-center">
                                                        <!-- Product name-->
                                                        <h5 class="fw-bolder">${bookTitle}</h5>
                                                        <!-- Product price-->
                                                        ${bookAuthor}
                                                    </div>
                                                </div>
                                                <!-- Product actions-->
                                                <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                                                    <div class="text-center">
                                                        
                                                    </div>

                                                </div>
                                            </div>
                                        </div>`
            $("#show_box").append(temp_html)
            console.log(bookTitle)
        }
    });
}

function uploading() {
    let url = $('#url').val()
    $.ajax({
        type: 'POST',
        url: '/upload',
        data: {url_give: url},
        success: function (response) {
            alert(response['msg'])
            window.location.href = '/';
        }
    });
}

