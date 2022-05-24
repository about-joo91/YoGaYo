const user_email = document.querySelector('#user_email');
const user_password = document.querySelector('#user_password');

// 자기 주소 작성할 것
const back_url = 'http://192.168.45.104:8080';

async function login() {
    let user_email_give = user_email.value;
    let user_password_give = user_password.value;

    if (user_email_give == "") {
        alert("이메일 주소를 입력하셔요")
        user_email.focus();
        return;
    }

    if (user_password_give == "") {
        alert("비밀번호를 입력하셔요")
        user_password.focus();
        return;
    }

    const request_body = {
        user_email_give: user_email_give,
        user_password_give: user_password_give
    }

    const response = await fetch(back_url + '/login', {
        method: 'POST',
        body: JSON.stringify(request_body),
    });

    const data = await response.json();
    alert(data['msg']);
    $.cookie('mytoken', data['token'], { path: '/' });
    console.log($.cookie);
}

const login_button = document.querySelector('#login_button');

login_button.addEventListener('click', login)