/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
    $("#startdate").datepicker();
    $("#enddate").datepicker();
    $("#button").button();

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
            },
            //y轴
            yAxis : {
                title : {
                    text :ytitle
                },
                labels: {
                    formatter: function() {
                        return this.value;
                    }
                }    ,
                //y=0
                plotLines : [
                    {
                        value : 0,
                        width : 2,
                        color : '#000000'
                    }
                ]
            },
            tooltip : {
                formatter : function() {
                    return '<b>' + this.series.name + '</b><br/>' + this.x
                        + ': ' + this.y;
                }
            },
            //右边的提示
            legend : {
                layout : 'vertical',
                align : 'right',
                verticalAlign : 'top',
                x : -10,
                y : 100,
                borderWidth : 1
            } ,
            series :[]
        }
        return options;


    }

    $.getchart = function(type, chartsarray) {
        if (type == 'fee') {
              var op = $.initCharts('<b>收入</b>', '', '日期', '元', chartsarray);
            op.xAxis.categories = chartsarray[0];
            op.series.push({
                    name: 'index pv',
                    data: chartsarray[1]}
            )
            var chart = new Highcharts.Chart(op);
        }
        if (type == 'indexpv') {
            var op = $.initCharts('<b>推荐页PV</b>', '30天内推荐页访问量', '日期', '次数', chartsarray);
            op.xAxis.categories = chartsarray[0];
            op.series.push({
                    name: 'index pv',
                    data: chartsarray[1]}
            )
            var chart = new Highcharts.Chart(op);
        }
    }

    $.indexpv = function(start, end, coll, querytype, qkey, qvalue) {
        var url = "/ssx/indexpv"
        $.ajax({
            type : "GET",
            url : url ,
            data : {},
            beforeSend:function() {
                $('#container').html('正在分析,请稍后....');
            }      ,
            success : function(msg) {
                var chartsarray = $.processindexpv(msg);
                $.getchart('indexpv', chartsarray);
            }
        });
    }
    $.getfee = function(start, end, coll, querytype, qkey, qvalue) {
        var url = "/ssx/fee"
        $.ajax({
            type : "GET",
            url : url ,
            data : {},
            beforeSend:function() {
                $('#container').html('正在分析,请稍后....');
            }      ,
            success : function(msg) {
                var chartsarray = $.processfee(msg);
                $.getchart('fee', chartsarray);
            }
        });
    }
    $.processindexpv = function(json) {
        var keys = new Array();
        var value1 = new Array();
        var data = eval('(' + json + ')');
        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            keys.push(one.date);
            value1.push(parseInt(one.indexpv));
        }

        var res = new Array();
        res.push(keys);
        res.push(value1);
        return res;
    }
    $.processfee = function(json) {
        var keys = new Array();
        var value1 = new Array();
        var data = eval('(' + json + ')');
        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            keys.push(one.date);
            value1.push(parseInt(one.fee));
        }

        var res = new Array();
        res.push(keys);
        res.push(value1);
        return res;
    }
    $.getfee();
});