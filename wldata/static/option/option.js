/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
    
    var domain = $('#domain').val();
    $("#savebutton").button();
    var userid=0;
    $("#savebutton").click(function(){
        var v="";
        $('input:checked').each(function(){
             v += $(this).attr('lang') + ",";
        });
        $.ajax({
            type : "GET",
            url : domain+'/option/setpower/'+userid+'/'+v ,
             cache:false,
            data : {} ,
            success : function(msg) {
                $( "<div>设置成功</div>" ).dialog({
                    height: 100,
                    modal: true
                });
            }
        });
    });

    $('#userlist').change(function(){
         $('.power').attr('checked',false);
         userid = this.value;
         $.ajax({
            type : "GET",
            url : domain+'/option/getpower/'+this.value ,
             cache:false,
            data : {} ,
            success : function(msg) {
                 var data = eval('(' + msg + ')');
                 for (var i = 0; i <data.length; i++){
                    $('.power[lang='+data[i]+']' ).attr("checked",true);
                 }
            }
        });
    });
    ///----------------------user----------------
    $("#adduser").button();
     $("#deluser").button();
    $("#adduser").click(function(){
                $('#adduserdiv').css('display','block');

    });
    $('#commitbtn').click(function(){
        $('#adduserform').submit();
    });

    $('#deluser').click(function(){
         var v = ""
         $('input:checked').each(function(){
             v += $(this).attr('lang') + ",";
        });
         $.ajax({
            type : "GET",
            url : domain+'/option/deluser/'+v ,
             cache:false,
            data : {} ,
            success : function(msg) {
                $( "<div>删除成功</div>" ).dialog({
                    height: 100,
                    modal: true
                });
            }
        });
    });

   //----------------menu----------------
     $("#addmenu").button();
     $("#delmenu").button();
       $("#addmenu").click(function(){
                $('#addmenudiv').css('display','block');

    });
      $('#menucommitbtn').click(function(){
        $('#addmenuform').submit();
    });

    $('#delmenu').click(function(){
         var v = ""
         $('input:checked').each(function(){
             v += $(this).attr('lang') + ",";
        });
         $.ajax({
            type : "GET",
            url : domain + '/option/delmenu/'+v ,
             cache:false,
            data : {} ,
            success : function(msg) {
                $( "<div>删除成功</div>" ).dialog({
                    height: 100,
                    modal: true
                });
            }
        });
    });
    //-----------------project-----------------
     $("#addproject").button();
     $("#delproject").button();
    $("#addproject").click(function(){
                $('#addprojectdiv').css('display','block');

    });
    $('#commitbtn').click(function(){
        $('#addprojectform').submit();
    });

    $('#delproject').click(function(){
         var v = ""
         $('input:checked').each(function(){
             v += $(this).attr('lang') + ",";
         });
         alert(v);
         $.ajax({
            type : "GET",
            url : domain+'/option/delproject/'+v ,
             cache:false,
            data : {} ,
            success : function(msg) {
                $( "<div>删除成功</div>" ).dialog({
                    height: 100,
                    modal: true
                });
            }
        });
    });
});