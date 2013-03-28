$(document).ready(function() {
    var domain = $('#domainval').val();
    var vitemid='';
    var vqueryurl='';
    var vmpsurl='';

    var swfpath = domain + "/static/js/swfupload.swf";
    var swfuOption = {
        flash_url :  swfpath,
        button_placeholder_id : "swfu-placeholder",
        file_size_limit : "2GB",
        button_width: 80, 
        button_height: 40, 
        button_image_url:domain+'/static/css/swfu.png',
        file_types:"*.rm;*.rmvb;*.wmv;*.asf;*.asx;*.wav;*.mpg;*.mpeg;*.mpe;*.mp4;*.m4v;*.3gp;*.mp4;*.amr;*.mp3;*.wma;*.m4a;*.aac;*.ac3;*.mov;*.avi;*.dat;*.mkv;*.flv;*.hlv;*.swf;*.vob;*.f4v;*.ogg;*.dv;*.dif;*.ts;*.lavf",
        debug:false,
        upload_progress_handler : upload_progress_function,
        upload_complete_handler : upload_complete_function,
        //file_dialog_complete_handler:file_dialog_complete_funciton,
        file_queue_error_handler: fileQueueError,
        file_queued_handler:file_queued_function
    }


    var swfu = new SWFUpload(swfuOption);
    
    function upload_complete_function(file, t,v){
        // show view info form
        $('#setp-1').hide();
        $('#setp-2').show();
    }
    
    function upload_progress_function(file, complete, total){        
        $('#progressbar').show().progressbar({
            value: (complete / total)*100
            
        });
        progressLabel = $( ".progress-label" );
        progressLabel.text( (complete / total)*100 + "%" );
    }
   
   function fileQueueError(fileobject, errorcode, message){
         
         if(errorcode =='-130'){
            alert('文件格式不支持, ' + message);
         }
   }

    function file_queued_function(file){
        //alert(file.name);
        $.ajax({
            url : domain + '/upload/upload',
            data : {
                title : file.name
            },
            dataType : 'jsonp',
            success : function(res) {
                if (res == '1') {
                    alert("准备上传时出错！");
                    return;
                }

                var data = res;
                if (data.result && data.url != '') {
                    vitemid = data.itemId;
                    vqueryurl = data.url;
                    vmpsurl = data.mpsUrl;
                    swfu.setUploadURL(data.url);
                    swfu.startUpload();

                } else {
                    alert("上传时出错！请稍后再试！");
                }
            }
        }); 

    }

    $('#uploadbtn').click(function(){
        var vtitle = $('#title').val();
        var vtags = $('#tags').val();
        var vcontent = $('#comments').val();
        var vchannel = $("input[name='videotype']:checked").val();
        
        if(!vchannel || !vcontent || !vtitle || !vtags){
            alert('该表单都是必填信息！');
            return;
        }
        if(!vitemid || !vqueryurl || !vmpsurl){
            alert('视频信息不完整！');
            return;
        }

        $.ajax({
            url : domain + "/upload/addvideoinfo",
            dataType: 'jsonp',
            data : {
                title : vtitle,
                tags : vtags,
                comments : vcontent,
                itemid : vitemid,
                queryurl : vqueryurl,
                mpsurl : vmpsurl,
                videotype : vchannel
            },
            success : function(res) {
                if(res.status == 0){
                    alert('提交表单成功');
                    location.reload();
                }
                if(res.status == 1){
                    alert('提交表单失败');
                }
            }
        });
    });
                


});