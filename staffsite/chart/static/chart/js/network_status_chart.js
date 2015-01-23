var BASE_URL;


// some global variable
var gRes;
var gAPIClient;
var gTimeObj;

$( document ).ready(function() {
    init();
    $("#ajax_loader").hide();
    $("#prev-btn").bind("click", time_prev);
    $("#next-btn").bind("click", time_next);
    gAPIClient = new Statistics();
    ajaxLoadComputingPowerData();
});

var init = function(){
    gTimeObj = new TimeObj();
    update_time_indicator();
    BASE_URL = $("#chart_api_url")[0].value;
    initCharts();
}

var computingPowerChart;

var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right: 60};

var initCharts = function(){

    computingPowerChart = dc.pieChart("#computing-power-chart", "computing_power");
    computingPowerChart
        .width(pieChartWidth).height(pieChartHeight)
        .label(function(b) {
            return b.key + "(" + b.value + ")";
        });

    rttLineChart = dc.lineChart("rtt-chart");
    rttLineChart
        .width(lineChartWidth).height(lineChartHeight)
        .margins(lineChartMargins)
        .elasticY(true)
        .xAxisLabel("Time")
        .yAxisLabel("Rtt time")
        .renderHorizontalGridLines(true)
        .brushOn(false)
        .renderArea(true);

    rttLineChart.xAxis().ticks(d3.time.hour, 1);

    bandwidthChart = dc.lineChart("bandwidth-chart");
    bandwidthChart
        .width(lineChartWidth).height(lineChartHeight)
        .margins(lineChartMargins)
        .elasticY(true)
        .xAxisLabel("Time")
        .yAxisLabel("Bandwidth")
        .renderHorizontalGridLines(true)
        .brushOn(false)
        .renderArea(true);

    bandwidthChart.xAxis().ticks(d3.time.hour, 1);

}


var success = function(response) {
    console.log("success");
    data = response.data
    drawComputingPowerChart(data);
    $("#ajax_loader").hide();
}

var error = function(response) {
    console.log("Ajax Load Error");
    alert("Ajax load error");
}

var ajaxLoadComputingPowerData = function(){
    $("#ajax_loader").show();
    gAPIClient.getAEInfo({}, error, success);
    console.log("load");
}

var drawComputingPowerChart = function(data){
    console.log(data);
    console.log("Draw Computing Power Chart");
    var crossfilter_data = crossfilter(data);
    dimension = crossfilter_data.dimension(function(d) {return d.AE_addr;});
    group = dimension.group()
                         .reduceSum(function(d) {return d.block_count;});

    computingPowerChart.dimension(dimension)
                       .group(group)
                       .label(function(d) {
                           return d.key + "(" + d.value + ")";
                       });

    console.log("Render Computing Power Chart");
    computingPowerChart.render();
}

var update_time_indicator = function() {
    $("#time-indicator")[0].innerHTML = gTimeObj.getTimeIndicator();
}

var time_prev = function() {
    gTimeObj.prev();
    update_time_indicator();
    ajaxLoadComputingPowerData();
}

var time_next = function() {
    gTimeObj.next();
    update_time_indicator();
    ajaxLoadComputingPowerData();
}
