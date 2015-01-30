var BASE_URL;


// some global variable
var gRes;
var gAPIClient;
var gTimeObj;
var bandwidthData;
var rttData;
var computingPowerData;
var loaderImg;

$( document ).ready(function() {
    init();
    $("#ajax_loader").hide();
    $("#prev-btn").bind("click", time_prev);
    $("#next-btn").bind("click", time_next);
    gAPIClient = new Statistics();
    loadComputingPowerData();
    loadBandwidthData();
    //ajaxLoadComputingPowerData();
});

var init = function(){
    initDatePickerBtn();
    gTimeObj = new TimeObj();
    update_time_indicator();
    BASE_URL = $("#chart_api_url")[0].value;
    loaderImg = $("#loader-img").css("background-image");
    initComputingPowerChart();
    initRTTChart();
    initBandwidthChart();
    initDateTimePicker();
    initDatePickerBtn();
}

var initDatePickerBtn = function() {
    console.log("init");
    $("#day-btn").bind("click", function(){
        $("#day-picker").show();
        $("#day-picker").data("DateTimePicker").date(moment());
        $("#month-picker").hide();
        $("#year-picker").hide();
        console.log("day-btn");
    });
    $("#month-btn").bind("click", function(){
        $("#day-picker").hide();
        $("#month-picker").show();
        $("#month-picker").data("DateTimePicker").date(moment());
        $("#year-picker").hide();
        console.log("month-btn");
    });
    $("#year-btn").bind("click", function(){
        $("#day-picker").hide();
        $("#month-picker").hide();
        $("#year-picker").show();
        $("#year-picker").data("DateTimePicker").date(moment());
        console.log("year-btn");
    });
}

var initDateTimePicker = function() {
    $("#day-picker").show();
    $("#month-picker").hide();
    $("#year-picker").hide();
    $("#day-picker").datetimepicker({
        viewMode: "days",
        format: "YYYY-MM-DD",
    });
    $("#month-picker").datetimepicker({
        viewMode: "months",
        format: "YYYY-MM",
    });
    $("#year-picker").datetimepicker({
        viewMode: "years",
        format: "YYYY",
    });
}



var computingPowerChart;

var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right: 60};

var success = function(response) {
    console.log("success");
    data = response.data
    drawComputingPowerChart(data);
    $("#computing-power-panel").css("background-image", "");
    $("#computing-power-chart").show();
}

var error = function(response) {
    console.log("Ajax Load Error");
    alert("Ajax load error");
}

var initComputingPowerChart = function() {
    computingPowerChart = dc.pieChart("#computing-power-chart", "computing_power");
    computingPowerChart
        .width(pieChartWidth).height(pieChartHeight)
        .label(function(b) {
            return b.key + "(" + b.value + ")";
        });
}


var initRTTChart = function() {
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
}

var initBandwidthChart = function() {
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

var loadComputingPowerData = function() {
    $("#computing-power-panel").css("background-image", loaderImg);
    $("#computing-power-chart").hide();
    gAPIClient.getAEInfo({}, error, success);
    console.log("load computing power data");
}

var loadRTTData = function() {
    $("#rtt-panel").css("background-img", "");
    $("#rtt-chart").hide();
    gAPIClient.getAEInfo({}, error, success);
    console.log("load computing power data");
}

var bandwidthSuccess = function(response) {
    console.log("bandwith success");
    bandwidthData = response.data
    //drawBandwidthChart(bandwidthData);
    $("#bandwidth-panel").css("background-image", "");
    $("#bandwidth-chart").show();
}

var bandwidthError = function(response) {
    console.log("bandwith error");
}

var loadBandwidthData = function() {
    $("#bandwidth-panel").css("background-img", "");
    $("#bandwidth-chart").hide();
    tmp = gTimeObj.getSinceUntil();
    gAPIClient.getBandwidth({"since": tmp[0], "until": tmp[1], "unit": 1000}, bandwidthError, bandwidthSuccess);
    console.log("load bandwidth data");
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

var drawBandWidthChart = function(data) {
  console.log(data);
  console.log("Draw bandwith chart");
  var crossfilter_data = crossfilter(data);
  var dimension = crossfilter_data.dimension(function(d) {
  })
}

var update_time_indicator = function() {
    //$("#time-indicator")[0].innerHTML = gTimeObj.getTimeIndicator();
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
