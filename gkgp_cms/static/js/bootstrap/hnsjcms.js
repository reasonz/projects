//tree click event
$(document).ready(function(){
	
	$('.nav-header').click(function(e){
		if ($(this).find('div').is(':hidden')){
			 e.stopPropagation();
			$(this).find('div').show();
		}
		else{
			e.stopPropagation();
			$(this).find('div').hide();
		}
	});

	//animating menus on hover
	$('ul.main-menu li:not(.nav-header)').hover(function(){
		$(this).animate({'margin-left':'+=5'},300);
	},
	function(){
		$(this).animate({'margin-left':'-=5'},300);
	});
});