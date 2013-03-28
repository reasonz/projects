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
                        text :'PV'
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
                        text :'CV'
                        ,
                        style: {
                            color: '#AA4643'
                            ,fontWeight: 'bold'
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
                name: '播放量(CV)',
                type:'spline',
                yAxis: 1,

                data: chartsarray[2]
            })
        var chart = new Highcharts.Chart(options);
    }
    $.getcountdata = function(msg) {
        var chartsarray = $.processJson(msg);
        $.initCharts('<b>访问量/播放量</b>', '', '日期()', '次数', chartsarray);

    }
    $.processJson = function(json) {
        var keys = new Array();
        var pvlist = new Array();
        var cvlist = new Array();
        
        var data = eval('(' + json + ')');

        for (var i = 0; i < data.length; i++) {
            var one = data[i];
            var td=one.day.split("-")
            keys.push(td[1] + '-' + td[2]);
            pvlist.push(one.pv);
            cvlist.push(one.cv);
            
        }
        var res = new Array();
        res.push(keys);
        res.push(pvlist);
        res.push(cvlist);
      

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
        window.location.href = domain + '/tdwap/allcount/' + start + '/' + end + '/' + area + '/' +ver + '/' + wap
    });
});
