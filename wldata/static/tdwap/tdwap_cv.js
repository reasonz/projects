/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
    $("#start").datepicker({dateFormat: "yy-mm-dd"});
    $("#end").datepicker({dateFormat: "yy-mm-dd"});

    $("#searchbtn").button();

    $.initCharts = function(title, subtitle, xtitle, ytitle, chartsarray) {
        var options = {
            chart : {
                renderTo : 'container',
                //defaultSeriesType : 'area',
                marginRight : 130,
                marginBottom : 50   ,
                borderWidth:1 ,
                borderColor:'#cccccc'
            },
            title : {
                text : title,
                x : -20
            },
            subtitle : {
                text : subtitle,
                x : -20
            },
            //X轴
            xAxis : {
                title : {
                    text : xtitle
                }
                , labels: {rotation: 0,    align: 'right',    style: { font: 'normal 13px Verdana, sans-serif'}}
                , gridLineWidth :1,
                minorTickInterval: 0.1
            },
            //y轴
            yAxis : [
                {
                    title : {
                        text :'CV'
                        ,
                        style: {
                            color: '#4572A7' ,
                            fontWeight: 'bold'
                        }
                    },
                    labels: {
                        formatter: function() {
                            if (this.value<=1000){
                                return parseInt(this.value ) ;
                            }

                            if (this.value>1000 && this.value<=10000){
                                return parseInt(this.value / 1000) + 'k';
                            }

                            if (this.value>10000 ){
                                return parseInt(this.value / 10000) + 'w';
                            }
                        }
                        ,
                        style: {
                            color: '#4572A7'
                        }
                    }
                },
                {
                    title : {
                        text :'转化率'
                        ,
                        style: {
                            color: '#AA4643'
                            ,fontWeight: 'bold'
                        }
                    },
                    labels: {
                        formatter: function() {
                           return this.value + '%' ;
                        }
                        ,
                        style: {
                            color: '#AA4643'
                        }
                    }
                    ,
                    opposite: true
                }
            ],
            tooltip : {
                formatter : function() {
                    if (this.series.name=='convert'){
                        return '<b>' + this.series.name + '</b><br/>' + this.x
                        + ': ' + this.y + '%';
                    }
                    else{
                        return '<b>' + this.series.name + '</b><br/>' + this.x
                        + ': ' + this.y + '次'; 
                    }
                   
                }
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 120,
                verticalAlign: 'top',
                y: 20,
                floating: true,
                backgroundColor: '#FFFFFF'
            },
            series :[]
        }

        options.xAxis.categories = chartsarray[0];
        options.series.push({
                name: '500',
                type:'spline',
                data: chartsarray[1]
            },
            {
                name: '51',
                type:'spline',
              
                data: chartsarray[2]
            },
            {
                name: '52',
                type:'spline',
               
                data: chartsarray[3]
            },
            {
                name: '53',
                type:'spline',
               
                data: chartsarray[4]
            },
            {
                name: '54',
                type:'spline',
              
                data: chartsarray[5]
            },
            {
                name: 'FLV',
                type:'spline',
               
                data: chartsarray[6]
            },
            {
                name: '其他',
                type:'spline',
               
                data: chartsarray[7]
            },
            {
                name: '总计',
                type:'spline',
               
                data: chartsarray[8]
            },
            {
                name: '转换率',
                type:'spline',
                yAxis: 1,
                data: chartsarray[9]
            }
            )
        var chart = new Highcharts.Chart(options);
    }
    $.getcountdata = function(msg) {
        var chartsarray = $.processJson(msg);
        $.initCharts('<b>访问量/播放量</b>', '', '日期()', '次数', chartsarray);

    }

    $.processJson = function(json) {
        var keys = new Array();
        var _500list = new Array();
        var _51list = new Array();
        var _52list = new Array();
        var _53list = new Array();
        var _54list = new Array();
        var _FLVlist = new Array();
        var _otherlist = new Array();
        var _countlist = new Array();
        var _convertlist = new Array();
      
        var data = eval('(' + json + ')');

        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            var td=one.day.split("-")
            keys.push(td[1] + '-' + td[2]);
            
            _500list.push(one._500);
            _51list.push(one._51);
            _52list.push(one._52);
            _53list.push(one._53);
            _54list.push(one._54);
            _FLVlist.push(one.FLV);
            _otherlist.push(one.other);
            _countlist.push(one.count);
            _convertlist.push(one.convert)

        }
        var res = new Array();
        res.push(keys);
        res.push(_500list);
        res.push(_51list);
        res.push(_52list);
        res.push(_53list);
        res.push(_54list);
        res.push(_FLVlist);
        res.push(_otherlist);
         res.push(_countlist);
          res.push(_convertlist);
        return res;

    }
    var startend = $('#ajaxvalue').val();
    $.getcountdata(startend.split('|')[2]);
    $('#searchbtn').click(function() {
        var start = ($('#start').val().length == 0) ? 'start' : $('#start').val();
        var end = ($('#end').val().length == 0) ? 'end' : $('#end').val();
        var domain = $('#domain').val();
        var ver = $('#ver').val() ;
        var area = $('#area').val() ;
        var wap = $('#wap').val() ;
        var api = $('#api').val() ;
        window.location.href = domain + '/tdwap/cv/' + start + '/' + end + '/' + area + '/' +ver + '/' + wap + '/' + api
    });
});
