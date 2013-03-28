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
				  	} else if(data=='exist'){
				  		newAlert('alert-error','添加成功,忽略已存在菜单添加!');
				  	}
				  	else{
				  		newAlert('alert-error','添加失败!');
				  	}
				  }
				});

	});

	//edit 
	$('#edit_channel').button();
	$('#edit_channel').click(function(){
		ids="";
		num=0;
    	$('.channelid').each(function(){
    		if($(this).attr('checked')){
    			ids+=$(this).val();
    			num=num+1;
    		}
    	});
    	if (num>1){
    		newAlert('alert-error','只能选择一个频道!');
    		return;
    	}
 	   	if(num ==0){
 	   		newAlert('alert-error','请选择频道!');
 	   		return;
    	}
		window.location.href=domain+'/channel/toupdate?id='+ids
	});

	//sub_channel -> edit_video
	$('#add_product').button();
	$('#add_product').click(function(){
		var text = $('#product').find("option:selected").text();
		var value = $('#product').val();
		var flag=0;
		$('.tp').each(function(){
			if ($(this).html()==value){
				flag=1;
			}
		});
		if (flag==0){
			var tr = $('<tr>').attr("class","ptr_"+value);
			var td_a = $('<td>');
			var td_b = $('<td>').attr('class','tp').html(value);
			var td_c = $('<td>').html(text);
			var a_del = $('<a>').attr('href','javascript:void(0)').attr('class','removeproduct').html('删除');
			$(a_del).bind("click",function(){
				$(this).parent().parent().remove();
			});
			$('#current_product').append(tr.append(td_a.append(a_del)).append(td_b).append(td_c));	
		}
		else{
			newAlert('alert-error','此产品已经添加!');
		}

	});

	
	$('#edit_video_form').submit(function(){
		pids=""
		$('.tp').each(function(){
			pids+=$(this).html()+'_';
		});
		
		$('#productids').val(pids);
		
	});

	function newAlert (type, message) {
	    $("#alert-area").append($("<div id='alert-message' class='alert '"+ type+" style='margin-top:8px;'><p> " + message + " </p></div>"));
	    $("#alert-message").delay(5000).fadeOut("slow", function () { $(this).remove(); });
	}

	



});