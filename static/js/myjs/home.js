var disks = [];
var cpu = [];
var cpuchart = {};
var memory = [];
var memoryChart = echarts.init(document.getElementById("memory"));
var cpuChart = echarts.init(document.getElementById("cpu"));
var diskChart = echarts.init(document.getElementById("disk"));

option = null;

function getdata() {
    $.ajax({
        url: 'home.html',
        data: {action: 'getsysteminfo'},
        success: function (result) {
            if (result.code === 200) {
                disks = result.disks;
                var cpucount = result.cpu.logicalcount;
                for (i = 0; i < cpucount; i++) {
                    if (cpu[i] === undefined) {
                        var cpui = [];
                    }
                    else {
                        var cpui = cpu[i];
                        if (cpui.length > 100) {
                            cpui.shift();
                        }
                    }
                    var data = {value: result.cpu.percent[i], name: result.cpu.time};
                    cpui.push(data);
                    cpu[i] = cpui;
                }
                var series = [];
                for (i = 0; i < cpu.length; i++) {
                    var serie = {};
                    serie.name = 'CPU' + i.toString();//
                    serie.type = 'line';
                    serie.data = cpu[i];
                    serie.smooth = true;
                    serie.xAxisIndex = i;
                    serie.yAxisIndex = i;
                    series.push(serie);
                }
                cpuchart.series = series;
                var axies = [];
                for (i = 0; i < cpu.length; i++) {
                    var axie = {};
                    axie.data = [];
                    for (j = 0; j < cpu[i].length; j++) {
                        axie.data.push(cpu[i][j].name);
                    }
                    axie.gridIndex = i;
                    axie.type = 'category';
                    axies.push(axie);
                }
                cpuchart.xAxis = axies;
                var axies = [];
                for (i = 0; i < cpu.length; i++)
                    axies.push({gridIndex: i});
                cpuchart.yAxis = axies;
                memory = [];
                memory.push({
                    name: '已使用',
                    value: (result.memory.used / 1024 / 1024).toFixed(2),
                    itemStyle: {
                        color: '#FF6666'
                    }
                });
                memory.push({
                    name: 'Buffer',
                    value: (result.memory.buffers / 1024 / 1024).toFixed(2),
                    itemStyle: {
                        color: '#CCCC00'
                    }
                });
                memory.push({
                    name: 'Cache',
                    value: (result.memory.cached / 1024 / 1024).toFixed(2),
                    itemStyle: {
                        color: '#0066CC'
                    }
                });
                memory.push({
                    name: '空闲',
                    value: (result.memory.free / 1024 / 1024).toFixed(2),
                    itemStyle: {
                        color: '#009966'
                    }
                });
            }
        }
    });
}

function makechart() {
    option = {
        title: {
            show: true,
            text: '内存使用情况',
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}{c}M',
            position: 'inside'
        },
        series: [
            {
                name: '内存使用情况',
                type: 'pie',
                avoidLabelOverlap: true,
                label: {
                    normal: {
                        show: true,
                        position: 'inside',
                        formatter: '{b}: {d}%'
                    }
                },
                labelLine: {
                    normal: {
                        show: true
                    }
                },
                data: memory
            }
        ],
    };
    memoryChart.setOption(option, true);
    option = {
        title: {
            show: true,
            text: 'CPU运行情况',
        },
        grid: [
            {x: '7%', y: '7%', width: '38%', height: '38%',},
            {x2: '7%', y: '7%', width: '38%', height: '38%',},
            {x: '7%', y2: '7%', width: '38%', height: '38%',},
            {x2: '7%', y2: '7%', width: '38%', height: '38%',}
        ],
        series: cpuchart.series,
        xAxis: cpuchart.xAxis,
        yAxis: cpuchart.yAxis,
    };
    cpuChart.setOption(option, true);
}

function refresh() {
    getdata();
    makechart();
    setTimeout(refresh, 1500);
}

layui.use(['form', 'layer'], function () {
    var form = layui.form;
    var layer = layui.layer;
});

$(function () {
    refresh();
});