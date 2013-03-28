
$(function() {

	var totalpage= $('#total').val();
	var domain = $('#domain').val();
	var startpage = $('#startpage').val();
	var cid  = $('#channelid').val();
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
											query(page);

										  }

	});
	// var optInit = getOptionsFromForm();
	// $("#ttpage").pagination(totalpage,optInit);

	// $('.edit_video').dblclick(function(){
	// 	window.location.href = $(this).attr('href');
	// });
	

	$('#search').button();

	$('#search').click(function(){
		
		query(1);
	});

	function query(page){
		var start= $('#start').val();
		var end= $('#end').val();
		var title= $('#title').val();
		var id= $('#id').val();
		var cid=$('#channelid').val();
		var url=domain+'/channel/gotochannel?page='+page+'&start='+start +'&end='+end+'&title='+title +'&id='+id + '&cid='+cid;
		
		window.location.href=url;
	}

	function newAlert (type, message) {
	    $("#alert-area").append($("<div id='alert-message' class='alert '"+ type+" style='margin-top:8px;'><p> " + message + " </p></div>"));
	    $("#alert-message").delay(10000).fadeOut("slow", function () { $(this).remove(); });
	}

	$('#publish').button()
	$('#unpublish').button()
	$('#publish').click(function(){
		
		var ids='';
		$('.videoid').each(function(){
			if ($(this).attr('checked')){
				ids+=$(this).val()+'_';
			}
		});
		
		if(ids.length<=0){
			newAlert('alert-error','发布失败!请选择需要发布的视频!');
		}
		else{
			//validate item is have product
			$.ajax({
				  url: domain + '/channel/publish?ids='+ids+ '&channelid='+cid,
				  type: 'GET',
				  timeout: 2000,
				  async:false,
				  success: function(data) {

				  	var res = eval('(' + data + ')')
				  	if(res.stat=='ok'){
				  		newAlert('alert-success','发布成功!');
				  		window.location.reload();
				  	}
				  	if(res.stat=='exist'){
				  		newAlert('alert-error','发布失败,存在没有绑定产品的视频 :' + res.data);
				  	}
				  	if(res.stat=='error'){
				  		newAlert('alert-error','添加失败!');
				  	}
				  }
			});	
		}

	});
	
	$('#unpublish').click(function(){
			var ids='';
			$('.videoid').each(function(){
				if ($(this).attr('checked')){
					ids+=$(this).val()+'_';
				}
			});
			
			if(ids.length<=0){
				newAlert('alert-error','取消发布失败!请选择需要取消发布的视频!');
			}
			else{
				//validate item is have product
				$.ajax({
					  url: domain + '/channel/unpublish?ids='+ids+ '&channelid='+cid,
					  type: 'GET',
					  timeout: 2000,
					  async:false,
					  success: function(data) {
					  	var res = eval('(' + data + ')')
					  	if(res.stat=='ok'){
					  		newAlert('alert-success','取消发布成功!');
					  		window.location.reload();
					  	} 
					  	else{
					  		newAlert('alert-error','取消发布失败!');
					  	}
					  }
				});	
			}

		});
	


});