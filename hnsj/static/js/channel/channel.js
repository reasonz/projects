/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
	
	var domain = $('#domain').val();
	$("#add_channel").button();
	$('#add_channel').click(function(){
		var url = domain+'/channel/add';
		window.location.href=url;
	});

	$('#del_channel').click(function(){
		var ids="";
		$('.channelid').each(function(){
			if($(this).attr('checked')){
				ids+=$(this).val()+'_';	
			}
		});
		window.location.href=domain+'/channel/delete?ids='+ids

	});

	$('#reset').click(function(){
		window.location.href=domain+'/channel/getitems';

	});
	
	$('#to_menu').button();
	$('#to_menu').click(function(){
		var menuid = $('#menuid').val();

		ids="";
    	$('.channelid').each(function(){
    		if($(this).attr('checked')){
    			ids+=$(this).val()+"_";
    		}
    	});

		$.ajax({
				  url: domain + '/channel/tomenu?menuid='+ menuid +'&channelids='+ids,
				  type: 'GET',
				  timeout: 2000,
				  success: function(data) {
				  	if(data=='ok'){
				  		newAlert('alert-success','添加成功!');
				  	} else{
				  		newAlert('alert-error','添加失败!');
				  	}
				  }
				});

	});

	function newAlert (type, message) {
	    $("#alert-area").append($("<div id='alert-message' class='alert '"+ type+" style='margin-top:8px;'><p> " + message + " </p></div>"));
	    $("#alert-message").delay(5000).fadeOut("slow", function () { $(this).remove(); });
	}

});