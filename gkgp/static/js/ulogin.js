
domain = $("#domainval").val();
//alert(domain);
$(function(){
	$.ajax({
	    url: domain+'/user/curuser?timestamp='+new Date(),
	    type: 'GET',
	    cache:false,
	    dataType:"json",
	    timeout: 10000,
	    error: function(XMLHttpRequest, textStatus, errorThrown){
	        alert('登录出问题，请重新登录！');
	        alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
	    },
	    success: function(data){
	    	//alert(data);
	    	if(null!=data){
	    		$("#first_li").html("<a href=\"#\" onclick=\"userlogout()\" id=\"reg\">退出</a>");
	        	$("#second_li").html("<a href=\"#\" >"+data[3]+"</a>");
	    	}
	    	
	      	
	    }
	});
	//取得cookie中视频
	findPlayVideo();
	initNav();
});

function initNav(){
	$.ajax({
	    url: domain+'/main/navi',
	    type: 'GET',
	    cache:false,
	    dataType:"json",
	    timeout: 1000,
	    error: function(XMLHttpRequest, textStatus, errorThrown){
	        alert('系统出问题！');
	        alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
	    },
	    success: function(data){
	      if(null!=data){
	      		$("#master").html("");
	      		$.each(data, function(k, v) {
            		$("#master").append("<li><a href=\""+v[6]+"\">"+v[1]+"</a></li>");
        		})
	      } 
	    }
	});
}

function userlogout(){
	$.ajax({
	    url: domain+'/user/logout?timestamp='+new Date(),
	    type: 'GET',
	    cache:false,
	    dataType:"text",
	    timeout: 1000,
	    error: function(){
	        alert('系统出问题！');
	    },
	    success: function(data){
	    	//alert(data);
	      window.location.reload(); 
	    }
	});
}

function userlogin(){
	ref = window.location.href;
	username = document.getElementById("userName").value;
	passwd = document.getElementById("userPWD").value;
	userck = document.getElementById("userCk");

	var uk = 0;
	if(isBlank(username)||username=="邮箱名"){
		alert("用户名不能为空！");
		return false;
	}

	if(isBlank(passwd)||passwd=="密码"){
		alert("密码不能为空！");
		return false;
	}

	if(userck.checked){
		uk=1;
	}

	$.ajax({
	    url: domain+'/user/login',
	    type: 'POST',
	    cache:false,
	    data: { "username": username, "password": passwd,"userck":uk,"ref":ref},
	    dataType:"json",
	    timeout: 1000,
	    error: function(){
	        alert('登录出问题，请重新登录！');
	    },
	    success: function(data){
	    	if(data.status!=1){
	    		alert(data.msg);
	    	}else{
	    		if(ref.indexOf("/user/toreg")>0){
	    			window.location.href=domain+"/main/index";
	    		}else{
	    			window.location.reload(); 
	    		}
	    	}
	    }
	});

}


function isBlank(exp){
	if (!exp || typeof(exp)=="undefined" || srtLength(exp)==0)
	{
	    return true;
	}else{
		return false;
	}
}

function srtLength(str){
	var realLength = 0, len = str.length, charCode = -1;
    for (var i = 0; i < len; i++) {
        charCode = str.charCodeAt(i);
        if (charCode >= 0 && charCode <= 128) realLength += 1;
        else realLength += 2;
    }
    return realLength;
}

function delPlsyVideo(videocode){
	$.ajax({
	    url: domain+'/programs/delplaylist',
	    type: 'GET',
	    cache:false,
	    data: { "itemcode": videocode},
	    dataType:"text",
	    timeout: 10000,
	    error: function(XMLHttpRequest, textStatus, errorThrown){
	    	alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
	        alert('删除出问题，请稍后再操作！');
	    },
	    success: function(data){
	    	if(data=='ok'){
	    		findPlayVideo();
	    	}else{
	    		alert('删除出问题，请稍后再操作！');
	    	}
	    }
	});
}

function findPlayVideo(){
	$.ajax({
	    url: domain+'/programs/playlist',
	    type: 'GET',
	    cache:false,
	    dataType:"json",
	    timeout: 10000,
	    error: function(){
	        alert('获取历史数据出问题！');
	    },
	    success: function(data){
	    	if(data!=null){
	    		$("#viewRecordContainer").html("");
	    		$.each(data,function(i,n){
	    			$("#viewRecordContainer").append("<div class=\"viewRecord_item\" id=\"id"+i+"\">");
	    			$("#viewRecordContainer").append("</div>");
	    			$("#id"+i).append("<div class=\"vr_row\" id=\"iid"+i+"\">");
	    			$("#id"+i).append("</div>");
	    			
	    			$("#iid"+i).append("<h6 class=\"vr_title\" id=\"iiid"+i+"\"></h6>");
					$("#iid"+i).append("<a class=\"close\" href=\"javascript:delPlsyVideo('"+n[6]+"');\" title=\"删除\">×</a>");

					$("#iiid"+i).append("<a href=\""+domain+"/programs/view/"+n[6]+"/"+"\" title=\""+n[2]+"\" id=\"videocode"+n[6]+"\">"+n[2]+" </a>");
	    		});
	    	}else{
	    		$("#viewRecordContainer").html("您最近没有观看视频。");
	    	}
	    }
	});
}