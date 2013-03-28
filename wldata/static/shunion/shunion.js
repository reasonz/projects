/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
    $("#start").datepicker({dateFormat: "yy-mm-dd"});
    $("#end").datepicker( {dateFormat: "yy-mm-dd"});

    $("#searchbtn").button();

    $.initCharts = function(title, subtitle, xtitle, ytitle, chartsarray) {
        var options = {
            chart : {
                renderTo : 'container',
                defaultSeriesType : 'line',
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
                   , labels: {rotation: -25,    align: 'right',    style: { font: 'normal 13px Verdana, sans-serif'}}
               , gridLineWidth :1

            },
            //y轴
            yAxis : [{
                title : {
                    text :'PV/UV'
                },
                labels: {
                    formatter: function() {
                        return this.value ;
                    }
                }    ,
                
            },{
                title : {
                    text :'订购/退订'
                },
                labels: {
                    formatter: function() {
                        return this.value ;
                    }
                } 
                , opposite: true
             
            }

            ],
            tooltip : {
                formatter : function() {
                    return '<b>' + this.series.name + '</b><br/>' + this.x
                        + ': ' + this.y + '次';
                }
            }
            ,
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
                name: '订购量',
                 yAxis: 1,
                data: chartsarray[1]
            },
            {
                name: '退订量',
                 yAxis: 1,
                data: chartsarray[2]
            },{

                name: 'PV',
              
                data: chartsarray[3]
            },
            {
                name: 'UV',
              
                data: chartsarray[4]
            })
        var chart = new Highcharts.Chart(options);
    }
    $.getcountdata = function(msg) {
        var chartsarray = $.processJson(msg);
        $.initCharts('<b>订购退订量</b>', '', '日期()', '次数', chartsarray);

    }
    $.processJson = function(json) {
        var keys = new Array();
        var value1 = new Array();
        var value2 = new Array();
        var value3 = new Array();
        var value4 = new Array();

        var data = eval('(' + json + ')');
        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            keys.push(one.date);
            value1.push(one.dinggou);
            value2.push(one.tuiding);
            value3.push(one.pv);
            value4.push(one.uv);

        }
        var res = new Array();
        res.push(keys);
        res.push(value1);
        res.push(value2);
        res.push(value3);
        res.push(value4);

        return res;
    }
    var startend = $('#ajaxvalue').val();
    $.getcountdata(startend.split('|')[2]);

    $('#searchbtn').click(function(){
        var start = ($('#start').val().length==0)?'start': $('#start').val();
        var end = ($('#end').val().length==0)?'end': $('#end').val();
        var domain = $('#domain').val();
        window.location.href=domain + '/shunion/order/'+start   + '/' + end
    });
});
