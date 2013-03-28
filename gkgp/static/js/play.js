$(function(){
	var domain = $('#domainval').val();
	$('#btnDig').click(function(){
	   var itemcode = $('#itemcode').val();
	   var dig = $('#btnDig > em');
	   	/*alert(domain+'/programs/dig/'+itemcode+'/');*/
	   $.get(domain+'/programs/dig/'+itemcode+'/',{},function(data){
		   if(data == 'noLogin'){
		   	  $('#loginDo').click();
		   }else{
		   	  dig.text(data)
		   }
		 });
	});
	
	$('#btnBury').click(function(){
	   var itemcode = $('#itemcode').val();
	   var bury = $('#btnBury > em');
	   		/*alert(domain+'/programs/dig/'+itemcode+'/');*/
	   $.get(domain+'/programs/bury/'+itemcode+'/',{},function(data){
		   	if(data == 'noLogin'){
		   	  $('#loginDo').click();
		   }else{
		   	  bury.text(data);
		   }
		 });
	});
});