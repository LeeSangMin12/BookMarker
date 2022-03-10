/********************************************
* comm.js
*********************************************/
$(function(){
    chkLoginCookies();
});

/* chk login user */
function chkLoginCookies() {
    let mytoken = $.cookie('mytoken');
    if (mytoken != null) {
        $('#tokenChk').text(parseJwt(mytoken)['userName'] + '님 환영합니다');
        showLogoutBtn();
    } else {
        showLoginBtn();
    }

}

/* jwt token decoding */
function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
};

/* to show  logoutBtn */
function showLogoutBtn(){
    $('#loginChkDiv').empty();
    let logOutBtn = `<button class="btn btn-outline-dark" id="userLogOut"  onclick="logout()" >
                                     로그아웃
                                 </button>`;
    $('#loginChkDiv').append(logOutBtn);
}

/* to show  logInBtn */
function showLoginBtn(){
        $('#loginChkDiv').empty();
    let loginBtn = `<button class="btn btn-outline-dark" id="toLoginPage" onclick="window.location.href='/login/login'" >
                                 로그인 / 회원가입
                                 </button>`
    $('#loginChkDiv').append(loginBtn);
}

/* logout */
 function logout(){
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href='/'

  }