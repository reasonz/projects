/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
   
	
	var totalpage= $('#total').val();
	var domain = $('#domain').val();
	var startpage = $('#startpage').val();
	
	$('#allcheck').click(function(){

		if($(this).attr('checked')){
			$('.videoid').each(function(){
				$(this).attr('checked',true);
			});
		}else{
			$('.videoid').each(function(){
				$(this).attr('checked',false);
			});
		}
	});


    $("#ttpage").paginate({
				count 		: totalpage,
				start		: startpage,
				display		:10,
				border					: false,
				text_color  			: '#888',
				background_color    	: '#EEE',	
				text_hover_color  		: 'black',
				background_hover_color	: '#CFCFCF',
				onChange     			: function(page){
											$('._current','#paginationdemo').removeClass('_current').hide();
											$('#p'+page).addClass('_current').show();
											window.location.href=domain + '/video/getitems?page='+page;

										  }

			});
    $('#chenagechannel').button();

    $('#chenagechannel').click(function(e){

    	ids="";
    	$('.videoid').each(function(){
    		if($(this).attr('checked')){
    			ids+=$(this).val()+"_";
    		}
    	});

    	if(ids==""){
    		newAlert("alert-error","请选择要分发的视频!");
    	}
    	else{
    		if ($('#channel').val()=='-1'){
    			newAlert("alert-error","请选择要分发的频道!");
    		}
    		else{
    			$.ajax({
				  url: domain + '/video/ishaveitem?ids='+ids +'&channelid='+$('#channel').val(),
				  type: 'GET',
				  timeout: 2000,
				  success: function(data) {

				  	if(data=='exist'){

				  		e.preventDefault();
						$('#myModal').modal('show');
				  	} else{
				  		$.changechannel('0');
				  	}
				  }
				});

    		}
    		
    	}
    });

    $.changechannel = function(ignore){
    	url = domain + '/video/changechannel?ids='+ids +'&channelid='+$('#channel').val() +'&ignore='+ignore;
    	
    	$.ajax({
			  url: url,
			  type: 'GET',
			  timeout: 2000,
			  success: function(data) {
			  	if(data=='ok'){
			  		newAlert('alert-success','成功分发到频道!');
			  	}else{
			  		newAlert('alert-error','分发失败!');
			  	}
			  }
		});
    }

    function newAlert (type, message) {
	    $("#alert-area").append($("<div id='alert-message' class='alert '"+ type+" style='margin-top:8px;'><p> " + message + " </p></div>"));
	    $("#alert-message").delay(5000).fadeOut("slow", function () { $(this).remove(); });
	}


	$('#ignore').button();
	$('#update').button();
	$('#ignore').click(function(e){
		$.changechannel('1');
		$('#myModal').modal('hide');

	});
	$('#update').click(function(e){
		$.changechannel('0');
		$('#myModal').modal('hide');
		
	});
});