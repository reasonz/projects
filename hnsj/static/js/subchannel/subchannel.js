
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
	// var optInit = getOptionsFromForm();
	// $("#ttpage").pagination(totalpage,optInit);

	// $('.edit_video').dblclick(function(){
	// 	window.location.href = $(this).attr('href');
	// });
	
});