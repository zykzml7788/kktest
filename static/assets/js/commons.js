/*
    登入方法
*/
function login(){

    var username=$("input[name='username']").val();
    var password=$("input[name='password']").val();

    console.log(username);
    console.log(password);
    $.ajax(
        {
            type:"POST",
            DataType:"json",
            contentType:"application/json;charset=utf-8",
            url:"/login/",
            data:JSON.stringify({"username":username,"password":password}),
            success:function(result){
                console.log(result);
                console.log(result.code)
                if(result.code=="100000"){
                    window.location.href="/index";
                }else if(result.code=="100001"){
                    $("#login_msg").text("账号或密码不能为空");
                }else if(result.code=="100002"){
                    $("#login_msg").text("账号不存在，请确认");
                }else if(result.code=="100003"){
                    $("#login_msg").text("密码错误，请确认");
                }else{
                    $("#login_msg").text("操作失败");
                }
            }
        }
    );
}


/*

    用户注册方法
*/
function regist(){

    var username=$("#username").val();
    var password=$("#password").val();
    var mail=$("#email").val();

    $.ajax(
        {
            type:"POST",
            DataType:"json",
            contentType:"application/json;charset=utf-8",
            url:"/register/",
            data:JSON.stringify({"username":username,"password":password,"mail":mail}),
            success:function(result){
                console.log(result);
                console.log(result.code)
                if(result.code=="100000"){
                    alert("恭喜你，注册成功，返回登入界面");
                    setTimeout(function(){},1000);
                    window.location.href="/login";
                }else if(result.code=="100001"){
                    $("#regist_msg").text("账号、密码或邮箱不能为空");
                }else if(result.code=="100002"){
                    $("#regist_msg").text("该账号昵称已存在,请更换");
                }else{
                    $("#regist_msg").text("注册失败,数据库炸炸炸啦！！！");
                }
            }
        }
    );
}






