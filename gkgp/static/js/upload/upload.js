$(document).ready(function() {
			var domain=$('#domain').val();
			
			$('.shangc_but').click(function(){
				$.fn.submitUP();
			});

			$.fn.submitUP=function(){

				var fileType=".rm.rmvb.wmv.asf.asx.wav.mpg.mpeg.mpe.mp4.m4v.3gp.mp4.amr.mp3.wma.m4a.aac.ac3.mov.avi.dat.mkv.flv.hlv.swf.vob.f4v.ogg.dv.dif.ts.lavf";
				var filePath=$("#fileUpload").val();
				var fileName=null;
				var suffix=null;
				if(filePath!=null&&filePath!=''){
					if(filePath.indexOf('\\')!=-1){
						var indexStart=filePath.lastIndexOf('\\')+1;
						var indexEnd=filePath.lastIndexOf('.');
						fileName=filePath.substring(indexStart,indexEnd); 
						suffix=filePath.substring(indexEnd,filePath.length);
					}else{
						var indexEnd=filePath.lastIndexOf('.');
						fileName=filePath.substring(0,indexEnd); 
						suffix=filePath.substring(indexEnd,filePath.length);
					}

					if(fileType.indexOf(suffix)==-1){
						$("#err_type").show();
						return;
					}else{
						$("#err_type").hide();
					}
				}else{
					alert("请先选择上传的文件");
					return;
				}
				
			
			 	$.post(domain+"/upload/upload",{title:fileName},function(res){
			 		
				 	if(res=='1'){
					 	alert("准备上传时出错！");
					 	return;
					 }
					var data=eval('('+ res +')');
					if(data.result&&data.url!=''){
						$("#uploadInfo").hide();
						$("#videoInfo").show();
						//设置数据
						$("#itemId").val(data.itemId);
						$("#title").val(fileName);
						$("#description").val(fileName);
						$("#tag1").val(fileName);

						$("#uploadForm").attr("action",data.url);
						$("#uploadForm").submit();
						$.fn.showUpload(data.url,res,fileName);
					}else{
						alert("上传时出错！请稍后再试！");
					}
				 });
			}
			
			////////////////////////
			$.fn.showUpload=function(url,res,fileName) {
				var data=eval('('+ res +')');
				var t;
				$.getJSON(url+'&callback=?',{},function(response){
					if (!response)return;
					if(data.token!=response.token)return;
					if (!response.status)return;
					var percent;
					
					if(response.status=='uploading'){
						percent=response.percent;
						$("#filePath").val(percent);
					}else if(response.status=='finish'){
						clearTimeout(t); 
						$("#filePath").val(percent);
						$("#filePath").val("上传成功！");
						//document.location.href="videoInfo.html?itemId="+data.itemId+"&title="+encodeURIComponent(fileName);
					}else if(response.status=='failed'){
						clearTimeout(t);
						alert("上传出错！请稍后再试！");
					}
				});
				t=setTimeout("$.fn.showUpload('"+url+"','"+res+"','"+fileName+"')", 1000);
			}
			//////////////
		});