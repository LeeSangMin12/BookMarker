$(function(){



});
// 현재 날짜 가져오기
function todayDate(){
    let today = new Date();
    let year = today.getFullYear();     // 년도
    let month = today.getMonth() + 1;   // 월
    let date = today.getDate();         // 날짜

    return year + '-' + month + '-' + date;

}

function paraShare(){
    let bookNum = $('#bookNum').val();
    let userId  = "testUser";
    let paraContent = $('#paraContent').val();
    let writeDate = todayDate();
       $.ajax({
            type: 'POST',
            url: '/detail/write_paragraph',
            data: {
                'bookNum': bookNum,
                'userId': userId,
                'paraContent': paraContent,
                'writeDate': writeDate
            },
            success: function (response) {
                console.log(response)
                window.location.reload();

            },error: function (error){
                console.log(error)
           }
        })
    }
function paraShow(num){

}
function paraDelete(num){

     $.ajax({
            type: 'POST',
            url: '/detail/delete_paragraph',
            data: {
                'paraNum': num
            },
            success: function (response) {
                console.log(response)
                window.location.reload();

            },error: function (error){
                console.log(error)
           }
        })

}










