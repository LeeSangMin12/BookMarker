$(document).ready(function () {
    listing();

});

function listing() {
    $.ajax({
        type: 'GET',
        url: '/listBook',
        data: {},
        success: function (response) {

            $("#books").empty()
            let rows = response['books']
            for (let i = 0; i < rows.length; i++) {
                let bookNum   = rows[i]['bookNum']
                let bookTitle = rows[i]['bookTitle']
                let bookUrl = rows[i]['bookUrl']
                let bookAuthor = rows[i]['bookAuthor']
                let bookPublisher = rows[i]['bookPublisher']
                let html_temp = ` <div class="col mb-5" id="${bookNum}">
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
                                                        <a class="btn btn-outline-dark mt-auto" href="/detail/detail/${bookNum}">명언 달기</a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>`
                $("#books").append(html_temp)
            }
        }
    })
}
function find_word(){
    $('div').removeClass("highlight")
    // window.location.reload()
    let hiChk = false
     $.ajax({
        type: 'GET',
        url: '/listBook',
        data: {},
        success: function (response) {
             // console.log(response['books'])
            let rows = response['books']
             for (let i = 0; i < rows.length; i++) {
                 let bookTitle = rows[i]['bookTitle']
                 let bookNum   = rows[i]['bookNum']
                   console.log(bookTitle)
                let book = $("#input-word").val()
                 console.log(book)
                  if(bookTitle.includes(book)){
                      $(`#`+bookNum).addClass("highlight")
                      $(`#`+bookNum)[0].scrollIntoView()
                      hiChk = true
                  }
             }
            if (hiChk === false){
                alert('해당하는 책이 없습니다 추가해주세요!')
                window.location.href ='/upload'
            }
         }
    })
}
