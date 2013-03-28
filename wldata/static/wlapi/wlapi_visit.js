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
                , labels: {rotation: -25,    align: 'right',    style: { font: 'normal 13px Verdana, sans-serif'}}
                , gridLineWidth :1,
                minorTickInterval: 0.1
            },
            //y轴
            yAxis : [
                {
                    title : {
                        text :'PV'
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
                },
                {
                    title : {
                        text :'UV/IP'
                        ,
                        style: {
                            color: '#89A54E'
                            ,fontWeight: 'bold'
                        }
                    },
                    labels: {
                        formatter: function() {
                            return parseInt(this.value / 10000) + 'w';
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
                    return '<b>' + this.series.name + '</b><br/>' + this.x
                        + ': ' + this.y + '次';
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
                name: '访问量(PV)',
                type:'spline',

                data: chartsarray[1]
            },
            {
                name: '用户量(UV)',
                type:'spline',
                yAxis: 1,

                data: chartsarray[2]
            },
            {
                name: 'IP(IP)',
                type:'spline',
                yAxis: 1,

                data: chartsarray[3]
            })
        var chart = new Highcharts.Chart(options);
    }
    $.getcountdata = function(msg) {
        var chartsarray = $.processJson(msg);
        $.initCharts('<b>访问量/用户量</b>', '', '日期()', '次数', chartsarray);

    }
    $.processJson = function(json) {
        var keys = new Array();
        var pvlist = new Array();
        var uvlist = new Array();
        var iplist = new Array();
        var data = eval('(' + json + ')');

        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            keys.push(one.date);
            pvlist.push(one.pv);
            uvlist.push(one.uv);
            iplist.push(one.ip);
        }
        var res = new Array();
        res.push(keys);
        res.push(pvlist);
        res.push(uvlist);
        res.push(iplist);

        return res;

    }
    var startend = $('#ajaxvalue').val();
    $.getcountdata(startend.split('|')[2]);
    $('#searchbtn').click(function() {
        var start = ($('#start').val().length == 0) ? 'start' : $('#start').val();
        var end = ($('#end').val().length == 0) ? 'end' : $('#end').val();
        var domain = $('#domain').val();
        var visittype = $('#visittype').val();
        window.location.href = domain + '/wlapi/visit/' + start + '/' + end + '/' + visittype
    });
});
