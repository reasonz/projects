$(function() {
	
	var domain = $('#domain').val();

	$('#add').button();
	$('#update').button();
	
	$('#del').button();
	$('#reset').button();
	var option = $("#module option[value='"+$('#selectmodule').val()+ "']" );
	
	option.attr('selected',true);


	var option_edit = $("#item_type option[value='"+$('#selecttype').val()+ "']" );
	
	option_edit.attr('selected',true);

	$('#add').click(function(){
		window.location.href=domain + '/main/gotoadd?moduleid='+$('#module').val()
	});

	$('#module').change(function(){
		window.location.href=domain + '/main/gotoindexsetting?moduleid='+$('#module').val()
	})
	
	$('#del').click(function(){
		var chk = false;
		$('.op').each(function(){
			if($(this).attr('checked')){
				chk = true;
			}
		});
		
		if(!chk){
		  alert("请选择需要删除的记录!");
		  return
		}
		
		var ids="";
		$('.op').each(function(){
			if($(this).attr('checked')){
				ids+=$(this).val()+',';	
			}
		});
		window.location.href=domain + '/main/delete?id='+ids + '&moduleid='+$('#module').val()
	});
	
	$('#op').click(function(){
		if($(this).attr('checked')){
			$('.op').each(function(){
				$(this).attr('checked',true)
			});
		}else{
			$('.op').each(function(){
				$(this).attr('checked',false)
			});
		}
	});

	$('#update').click(function(){
		var chk = false;
		var count = 0;
		$('.op').each(function(){
			if($(this).attr('checked')){
				chk = true;
				count++;
			}
		});
		
		if(!chk || count>1){
		  alert("请选择一条需要修改的记录!");
		  return
		}
		
		var ids="";
		$('.op').each(function(){
			if($(this).attr('checked')){
				ids+=$(this).val()+'_';	
			}
		});
		if(ids==""){
			alert('请勾选修改项');
			return;
		}
		window.location.href=domain + '/main/gotoedit?id='+ids + '&moduleid='+$('#module').val()
	});


	$('#reset').click(function(){

		window.location.href=domain + '/main/gotoindexsetting?moduleid='+$('#module').val()

	});
});