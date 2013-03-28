
/*
 * @public 主站登录API
 * @param {object} op 用户名/密码对象
 * @param {function} cb 登录事件回调
 */
// TUI.ns('TUI.api.login', function(op, cb){
// 
    // var opt = TUI.mix({ loginname: '', password: '' }, op || {});
    // var msg = {
        // '1': '登录成功',
        // '0': 'Email不存在或密码错误，请重试',
        // '-1': '帐号因反复上传侵权视频，已被封',
        // '-2': '你注册的邮箱还没有验证！',
        // '-3': '请填写完整的E-mail和密码！'
    // };
// 
    // if (checkInput()) {
        // $.ajax({
          // url: "http://login.tudou.com/login.do?act=ajaxLogin",
          // dataType: 'jsonp',
          // data: opt,
          // success: function(res){
            // cb && cb(res, msg[res]);
          // }
        // });
    // } 
// 
    // function checkInput(){
        // var flag = true;
        // if (opt.loginname == '' || opt.password == '') {
            // cb && cb(-3, msg['-3']);
            // flag = false;
        // }
        // return flag;
    // }
// 
// }); // TUI.api.login

var GK = {};
GK.login= function (){
    var user, pwd, loginbox, winW = $(window).width(), regbox;
    var html = ['<div class="mask" id="mask"></div>',
                '<div class="reg-box" id="loginBox">',
                    '<div class="reg-logo"></div>',
                    '<span class="reg-close" ></span>',
                    '<a href="'+domain+'/user/toreg'+'" class="toreg">免费注册</a>',
                    '<div class="reg-tr"><input type="text" value ="邮箱名" class="txt" id="userName" /></div>',
                    '<div class="reg-tr"><input type="password" value="" class="txt" id="userPWD" /> <span class="tip-pwd">密码</span></div>',
                    '<div class="reg-tr"><input type="button" value="登录" id="loginBtn"  class="btn" onclick="userlogin();"/> <label><input id="userCk" type="checkbox" checked="checked" /> 记住我</label></div>',           
                '</div>'].join('');
    
    $('#loginDo').click(function(){
        // event.preventDefault();
         $(document.body).append(html);
         regbox = $('#loginBox'); 
         regbox.css({'left': winW/2 - 170});
         $('#mask').css({'height': $(document).height(), 'opacity': 0.5});
        return false;        
    });

    $('#upload_index_btn').click(function(){

        $.ajax({
            url: domain+'/user/curuser',
            type: 'GET',
            dataType:"json",
            async:false,
            timeout: 10000,
            success: function(data){
                
                if(null==data){
                    
                     event.preventDefault();
                     $(document.body).append(html);
                     regbox = $('#loginBox'); 
                     regbox.css({'left': winW/2 - 170});
                     $('#mask').css({'height': $(document).height(), 'opacity': 0.5});
                     return false;   
                }
                
                
            }
        });
             
    });
    
    function callBack(res, t){
        if(res == 1){
            setUserInfo();
            showLoginStatus();
            loginbox.close();
        }else{
            TUI.panel(t);
        }        
    }

    $(document.body).delegate('#loginBtn', 'click', function(){
        user = $('#userName').val();
        pwd = $('#userPWD').val();
        
       //TODO: 登录 接口
       
    }).delegate('.reg-close', 'click', function(){
        $('#mask').remove();
        regbox.remove();
    }).delegate('#userName', 'click', function(){
        $(this).val(''); 
    }).delegate('#userPWD', 'click', function(){
        $('.tip-pwd').hide(); 
    });
    
        
}
/*
 * 热点大图轮换
 */
GK.slideShow = function(){
    var items = window.hotBoardItems;
    var count = items && items.length || 0;

    if (!count) return;

    var panel = $('#slideshow');
    var $pic = panel.find('.scroll'), 
        $txt = panel.find('.txt'), 
        $btns = panel.find('.btns')
        pic = [], txt = [], btns = [];
    
    createHtml();
    
    var lazyImg = panel.find('.lazyImg');
    loadLazyImg();
    var content = TUI.switchTab({ box: panel, tab: '.btns a', panel: '.pic a', slide: true, loop: 3000 }); 
    var $cur = panel.find('.cur');   
    content.bind('before', function(prev, cur){
        loadLazyImg(cur);
        cur = cur > count - 1 ? 0 : cur;
        
        $cur.animate({'left': cur * 58}, 500);
    });
    
    content.bind('after', function(){
        var cur = content.current;        
        $txt.hide()
        .html('<div class="play"></div><h3>'+ txt[cur].title +'</h3><span>'+ txt[cur].subtitle +'</span><a href="'+ txt[cur].url +'" class="link" target="_blank"></a> ').fadeIn();
    });
    
    
    function createHtml(){
        for(var i = 0; i < count; i++){
           pic.push('<a target="_blank" rel= "'+ (i+1) +'" href="'+ items[i].url +'" style="display: ' + (i == 0 ? 'block': 'none')+ ';"><img width="980" height="375"  class="lazyImg" src="http://css.tudouui.com/skin/__g/img/sprite.gif" alt="'+ items[i].pic +'"></a>');
           btns.push('<a href="'+ items[i].url +'" target="_blank" rel="'+ (i+1)+'"><img width="48" height="48" src="'+ items[i].pic +'" /></a>');
           txt.push({title: items[i].title, subtitle : items[i].subtitle || '', url: items[i].url});
        }
        btns.push('<div class="cur"><b></b></div>');
        
        $pic.html(pic.join(''));
        $btns.html(btns.join('')); 
        $txt.html('<div class="play"></div><h3>'+ txt[0].title +'</h3><span>'+ txt[0].subtitle +'</span><a href="'+ txt[0].url +'" class="link" target="_blank"></a> ');       
    }
    
    function loadLazyImg(cur){
        cur = cur || 0;
        var img = lazyImg.eq(cur);
        var src = img.attr('alt');
        if (src) {
            img.attr('src', src);
            img.attr('alt', '');
        }
    }
};


GK.GKTX = function(){
    var box, tab, panel;
    $('#secGKTX .c').forEach(function(t){        
        box = $(t);
        tab = box.find('.btns').find('li');
        panel = box.find('.pic');
        TUI.switchTab({ box: box, tab: tab, panel: panel});        
    });    
};

GK.hover = function(){
    $('.mod_nrank').delegate('li.pack', 'mouseenter', function(){
        $(this).addClass('current');
    }).delegate('.pack', 'mouseleave', function(){
        $(this).removeClass('current');
    });
    
    $('.mod_picarea').delegate('.pic1, .pic2, .pic3', 'mouseenter', function(){
        $(this).find('.ext').show();
    }).delegate('.pic1, .pic2, .pic3', 'mouseleave', function(){
        $(this).find('.ext').hide();
    });
    
    
};

GK.reg = function(){
    var vcodeImg = $('#vcodeImg'),
        codeId = $('#codeId'),
        data = GK.regx;
    
    $('#regBtn').click(function(){
        event.preventDefault();
    
        if(!FrmValid.validata(data))  return false;        
        
    });
}
var FrmValid = function(){
    //验证表单  args {array} 
    function validata(args){
        for (var i = 0, l = args.length; i < l; i++) {            
            if (!toValid(args[i])){
                return false;
            } 
        }
        return true;
    }

    function toValid(ops) {
        var elm = ops.elm || '', def = $.trim(ops.def) || '', reg = ops.reg || '', tips = ops.tips || '', val;

        if (!elm)
            return false;

        val = $.trim(elm.val());
        
        if (val === def || !reg.test(val)) {
            elm.next('span.red').html(tips);
            elm.focus();
            return false;
        }else{
            elm.next('span.red').html('');
        }
        return true;
    }
    
    return {
        validata: validata
    }
}();

GK.regx = [{
        elm : $('#email'),
        def : ' ',
        reg : /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,
        tips : 'Email是必填的'

    }, {
        elm : $('#password'),
        def : '',
        reg : /^.{4,20}$/,
        tips : '密码是必填的 '

    }, {
        elm : $('#nickName'),
        def : '',
        reg : /^.{1,25}$/,
        tips : '昵称必填'

    }, {
        elm : $('#vCode'),
        def : '',
        reg : /^.{1,6}$/,
        tips : '验证码必填'

    }];

GK.viewRecord = function(){
    $('#viewRecordNav').mouseenter(function(){
        $(this).addClass('active');
    }).mouseleave(function(){
        $(this).removeClass('active');
    });
    
};

GK.uploadBtn = function(){
         var elm = $('.g-upload');
         setInterval(function(){
                   elm.hasClass('g-upload-y')? elm.removeClass('g-upload-y') : elm.addClass('g-upload-y');
         },1000);
};



$(function(){
    TUI.lazyImageLoader();
    GK.slideShow();
    
    TUI.switchTab({ box: '#secGKTX2', tab: '.t_dot li', panel: '.c',  loop: 5000  });
    TUI.switchTab({ box: '#secGKTX', tab: '.t_dot li', panel: '.c',  loop: 5000  });
	TUI.switchTab({ box: '.mod_vdlist_n1', tab: '.t-sub li', panel: '.c'});

    GK.uploadBtn();
    GK.GKTX();
    GK.hover();
    GK.viewRecord();
    
    GK.login();
    GK.reg();
});
