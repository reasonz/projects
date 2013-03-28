$(document).ready(function() {
	var domain = $('#domain').val();
	var vitemid='';
	var vqueryurl='';
	var vmpsurl='';
	var swfpath = domain+"/static/js/swfupload.swf";
	var swfuOption = {
	    flash_url :  swfpath,
	    button_placeholder_id : "swfu-placeholder",
	    file_size_limit : "2GB",
	    button_width: 80, 
	    button_height: 25, 
	    button_image_url:domain +'/static/image/button.png',
	    button_text:'<span class="button">Select Images <span class="buttonSmall">(2 MB Max)</span></span>',
	    button_text_style: ".button { font-family: Helvetica, Arial, sans-serif; font-size: 12pt; } .buttonSmall { font-size: 10pt; }",
	    file_types:"*.rm;*.rmvb;*.wmv;*.asf;*.asx;*.wav;*.mpg;*.mpeg;*.mpe;*.mp4;*.m4v;*.3gp;*.mp4;*.amr;*.mp3;*.wma;*.m4a;*.aac;*.ac3;*.mov;*.avi;*.dat;*.mkv;*.flv;*.hlv;*.swf;*.vob;*.f4v;*.ogg;*.dv;*.dif;*.ts;*.lavf",
	    debug:true,
	    upload_progress_handler : upload_progress_function,
	    // file_dialog_complete_handler:file_dialog_complete_funciton,
	    file_queued_handler:file_queued_function
	}


	var swfu = new SWFUpload(swfuOption);
	$('#viewinfo').hide();
	function upload_progress_function(file, complete, total){
		$('#progressbar').progressbar({
			value: (complete / total)*100,
			progressLabel:(complete / total)*100
		});
	}


	function file_queued_function(file){
		alert(file.name);
		//get real upload url 
		$.post(domain+"/upload/upload",{title:file.name},function(res){
		 	if(res=='1'){
			 	alert("准备上传时出错！");
			 	return;
			 }

			var data=eval('('+ res +')');
			if(data.result&&data.url!=''){

				vitemid=data.itemId;
				vqueryurl=data.url;
				vmpsurl = data.mpsUrl;
				swfu.setUploadURL(data.url);
				swfu.startUpload();
			}else{
				alert("上传时出错！请稍后再试！");
			}
		});
		// show view info form
		$('#viewinfo').show();
	}

	$( "#progressbar" ).progressbar({
      value: 0
    });
	
	

	$('#uploadbtn').click(function(){
		var vtitle = $('#title').val();
		var vtags = $('#tags').val();
		var vcontent = $('#comments').val();
		var vchannel = $("input[name='channel']:checked").val();
		alert(vchannel);
		
		$.post(domain+"/upload/addvideoinfo",
		{
			title:vtitle,
			tags:vtags,
			comments:vcontent,
			itemid:vitemid,
			queryurl:vqueryurl,
			mpsurl:vmpsurl,
			channel : vchannel
		},
		function(res){
			var data=eval('('+ res +')');
			// url= data.itemUploadInfo.uploadUrl;
			if(data.status==0){
				alert(data.msg);
			}
		});

	});
	
	

	$.fn.showlog=function(url){
		$.getJSON(url+'&callback=?',{},function(response){
			$('#title').val(response.percent);
		});
		t=setTimeout("$.fn.showlog("+ url + ")", 3000);
	}
				
});