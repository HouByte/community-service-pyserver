;
var index_ops = {
    init: function () {
        this.orderEChart();
        this.serviceNatureEChart();
        this.serviceTypeEChart();
        this.orderStatusEChart();

    },
    orderEChart: function () {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('order'));

        // 指定图表的配置项和数据
        var option = {
            xAxis: {
                type: 'category',
                data: []
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [],
                    type: 'line',
                    smooth: true
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        $.ajax({
            url: common_ops.buildUrl("/charts/order/trading"),
            type: "GET",
            dataType: "json",
            success: function (map) {
                 var xData = []
                 var yData = []
                 for (var key in map) {
                     xData.push(key)
                     yData.push(map[key])
                }
                option.xAxis.data = xData
                option.series[0].data = yData
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            },
            error: common_ops.errorHandle
        });


    },
    serviceTypeEChart: function () {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('service-type'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '服务类型分布图',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [
                {
                    name: '类型',
                    type: 'pie',
                    radius: '50%',
                    data: [
                        {value: 1048, name: '提供服务'},
                        {value: 735, name: '寻找服务'}
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        $.ajax({
            url: common_ops.buildUrl("/charts/service/type"),
            type: "GET",
            dataType: "json",
            success: function (data) {
                option.series[0].data = data
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            },
            error: common_ops.errorHandle
        });
    },
    serviceNatureEChart: function () {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('service-nature'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '服务性质分布图',
                left: 'center'
            },
            tooltip: {
                trigger: 'item'
            },
            legend: {
                orient: 'vertical',
                left: 'left'
            },
            series: [
                {
                    name: '性质',
                    type: 'pie',
                    radius: '50%',
                    data: [
                        {value: 1048, name: '互助'},
                        {value: 735, name: '服务'},
                        {value: 580, name: '公益'}
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        $.ajax({
            url: common_ops.buildUrl("/charts/service/nature"),
            type: "GET",
            dataType: "json",
            success: function (data) {
                option.series[0].data = data
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            },
            error: common_ops.errorHandle
        });
    },
    orderStatusEChart: function () {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('order-status'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: '近30日订单状态'
            },
            tooltip: {},
            legend: {
                data: ['订单状态']
            },
            xAxis: {
                data: ['未同意', '未支付', '未确认', '未评价', '完成', '已取消', '被拒绝']
            },
            yAxis: {},
            series: [
                {
                    name: '订单状态',
                    type: 'bar',
                    data: [0, 0, 0, 0, 0, 0]
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        $.ajax({
            url: common_ops.buildUrl("/charts/order/trading/status"),
            type: "GET",
            dataType: "json",
            success: function (data) {
                console.log(data)
                option.series[0].data = data
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
            },
            error: common_ops.errorHandle
        });
    }
};

$(document).ready(function () {
    index_ops.init();
});