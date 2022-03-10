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
    let userId  = $.cookie();
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
                if(response['result']=='success'){
                    window.location.reload();
                }else{
                    if(confirm(response['msg']+'\n로그인페이지로 이동하시겠습니까?')){
                    window.location.href='/login/login';
                    }else{

                    }
                }
                console.log(response)

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
                if(response['result']=='success'){
                    alert(response['msg']);
                }else{
                    alert(response['msg']);
                }
            },error: function (error){
                console.log(error)
           }
        })

}










