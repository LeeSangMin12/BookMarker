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
    let bookNum = "b"+1;
    let paraNum = "p"+1;
    let userId  = "testUser01";
    let paraContent = "책설명 입니당";
    let writeDate = todayDate();
    console.log("ASd");
       $.ajax({
            type: 'POST',
            url: '/detail/write_paragraph',
            data: {
                'bookNum': bookNum,
                'paraNum': paraNum,
                'userId': userId,
                'paraContent': paraContent,
                'writeDate': writeDate
            },
            success: function (response) {
                console.log(response)

            },error: function (error){
                console.log(error)
           }
        })
    }





