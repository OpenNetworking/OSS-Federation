
// some global variable
var BASE_URL;
var gTimeObj;
var txData;
var loaderImg;

$( document ).ready(function() {
    initDatePickerBtn();
    initDateTimePicker();
    gTimeObj = new TimeObj();
    BASE_URL = $("#chart_api_url")[0].value;
    loaderImg = $("#loader-img").css("background-image");
    initTxAmountChart();
    loadData();
});

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



var issuerChart;
var colorChart;
var txAmountChart;
var txNumChart;

var lineChartHeight = 150;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 40, bottom: 40, left: 60, right: 60};

var initIssuerChart = function() {
    issuerChart = dc.pieChart("#issuer-chart", "issuer-chart");
    issuerChart.width(pieChartWidth).height(pieChartHeight)
}

var initColorChart = function() {
    colorChart = dc.pieChart("#color-chart", "color-chart");
    colorChart.width(pieChartWidth).height(pieChartHeight)
}

var initTxAmountChart = function() {
    var width = $("#tx-amount-panel").css("width");
    lineChartWidth = parseInt(width, 10);
    var height = $("#tx-amount-panel").css("height");
    lineChartHeight = parseInt(height, 10);
    var h = $("#tx-amount-heading").css("height");
    lineChartHeight = lineChartHeight - parseInt(h, 10) - 10;
    txAmountChart = dc.lineChart("#tx-amount-chart");
    txAmountChart
        .width(lineChartWidth).height(lineChartHeight)
        .margins(lineChartMargins)
        .elasticY(true)
        .xAxisLabel("Time")
        .renderHorizontalGridLines(true)
        .brushOn(false)
        .renderArea(true);

    txAmountChart.xAxis().tickFormat(d3.time.format("%H"));
    txAmountChart.xAxis().ticks(d3.time.hour, 1);
}

var initTxNumChart = function() {
    txNumChart = dc.lineChart("#tx-num-chart");
    txNumChart
        .width(lineChartWidth).height(lineChartHeight)
        .margins(lineChartMargins)
        .elasticY(true)
        .xAxisLabel("Time")
        .renderHorizontalGridLines(true)
        .brushOn(false)
        .renderArea(true);

    txNumChart.xAxis().ticks(d3.time.hour, 1);
}

var draw = function(data) {
    var date = new Date();
    var tmp1 = new Date(date.getTime());
    var tmp2 = new Date(date.getTime());
    tmp1.setHours(0);
    tmp2.setHours(23);
    var since = d3.time.hour(tmp1);
    var until = d3.time.hour(tmp2);
    console.log(since);
    console.log(until);

    var crossfilter_data = crossfilter(data);
    var dim = crossfilter_data.dimension(function(t) { return t.hour; });
    var g = dim.group().reduceSum(function(t) { return t.total_out; });
    txAmountChart.dimension(dim)
                 .group(g)
                 .x(d3.time.scale().domain([since, until]));
    txAmountChart.render();


}

var loadData = function() {
    $.ajax({
        url: "http://128.199.176.196:9000/chart/day/",
        method: "GET",
        success: function(response){
            console.log("success");
            console.log(response);
            data = response.data
            //data.sort(function(a, b) { return a.hour - b.hour; });
            console.log(data);
            for(var i = 0; i < data.length; ++i){
                hour = d3.time.day(new Date());
                data[i].hour = hour.setHours(data[i].hour);
            }
            draw(data)
        },
        error: function(response) {
            console.log("error");
        }
    });
}
