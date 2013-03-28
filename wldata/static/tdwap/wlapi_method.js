/**
 * Created by IntelliJ IDEA.
 * User: reason
 * Date: 12-7-2
 * Time: 下午3:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
    $("#start").datepicker({dateFormat: "yy-mm-dd"});

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

            },
            //y轴
            yAxis : [
                {
                    title : {
                        text :'times'
                        ,
                        style: {
                            color: '#4572A7' ,
                            fontWeight: 'bold'
                        }
                    },
                    labels: {
                        formatter: function() {
                            return parseInt(this.value / 10000) + 'w';
                        }
                        ,
                        style: {
                            color: '#4572A7'
                        }
                    }
                }
            ],
            tooltip : {
                formatter : function() {
                    return '<b>' + this.series.name + '</b><br/>' + this.x
                        + ': ' + this.y + '次';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',

                verticalAlign: 'top',
                y: 40,
                floating: true,
                backgroundColor: '#FFFFFF'
            },
            series :[]
        }

        options.xAxis.categories = chartsarray[0];
        options.series.push({
                name: '调用次数',
                type:'bar',
                data: chartsarray[1]
            }
        )
        var chart = new Highcharts.Chart(options);
    }
    $.getcountdata = function(msg) {

        var chartsarray = $.processJson(msg);
        $.initCharts('<b>接口调用次数</b>', '', '', '次数', chartsarray);

    }
    $.processJson = function(json) {
        var keys = new Array();
        var count = new Array();
        var usetime = new Array();
        var data = eval('(' + json + ')');
        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            keys.push(one.apiname);
            count.push(one.count);
            usetime.push(one.usetime);
        }
        var res = new Array();
        res.push(keys);
        res.push(count);
        res.push(usetime);
        return res;

    }
    var jsonvalue = $('#ajaxvalue').val();
    $.getcountdata(jsonvalue);
    $('#searchbtn').click(function() {
        var start = ($('#start').val().length == 0) ? 'start' : $('#start').val();
        var domain = $('#domain').val();
        window.location.href = domain + '/wlapi/method/' + start
    });
});
