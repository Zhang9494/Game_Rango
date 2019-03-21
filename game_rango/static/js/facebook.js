(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; }
    js = d.createElement(s);
    js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js"
    fjs.parentNode.insertBefore(js, fjs)
}(document, 'script', 'facebook-jssdk'))

window.fbAsyncInit = function () {
    FB.init({
        appId: '2095185734106677',
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v3.2'
    })
}



function login(){
    FB.login(function (response) {
        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            FB.api('/me', function (response) {
                console.log('Good to see you, ' + response.name + '.');
                checkLoginState()
            });
        } else {
            console.log('User cancelled login or did not fully authorize.');
        }
    }, {
        scope: 'public_profile,email'
    });
}

var fbId, fbToken;
function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}

function statusChangeCallback(response) {
    if (response.status === 'connected') {
        fbId = response.authResponse.userID;
        fbToken = response.authResponse.accessToken;
        getUserInfo();
    } else if (response.status === 'not_authorized') {
        console.log('facebook unauthorized');
    } else {
        console.log('unknown');
    }
}

function getUserInfo() {
    FB.api('/me', function (response) {
        console.log('Successful login for: ' + response.name);
        var data = {
            nickName: response.name,
            avatar: 'http://graph.facebook.com/' + fbId + '/picture?type=large',
            openId: fbId,
            loginType: 'FACEBOOK'
        }
        console.log(data)
        POST('/app/user/loginByOther.v2', data, function (res) {
            if (res.code == 0) {
                console.log(res.data)
                localStorage.userInfo = JSON.stringify(res.data)
                localStorage.token = res.data.token
                localStorage.avatar = res.data.avatar
                localStorage.userName = res.data.nickName
            } else {
                alert(JSON.parse(res.msg)[language])
            }
        })

    });
}
// <script type="text/javascript" src="{% static 'facebook.js' %}">
//<a onclick="login()"> <img src="{% static 'facebook.png' %}" alt="" height="30" width="30"> </a><a onclick="login()">Log in with Facebook</a>