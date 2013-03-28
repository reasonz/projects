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
	


});