var BASE_URL = "59.151.30.38:5567/chart/fakemonth/";

var currentDate;
var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right:60};

$( document ).ready( function() {
    BASE_URL = window.location.host + BASE_URL;
    currentDate = new Date();
    $("#prev_date").bind("click", prevDateFunc);
    $("#next_date").bind("click", nextDateFunc);

    initDailyChart()
    ajaxLoadDaily(currentDate)

});

// #initDailyChart
var initDailyChart = function(){
  //init daily transaction amount chart
  dailyTxAmountLineChart = dc.lineChart("#daily-tx-amount-chart", "daily");
  dailyTxAmountLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Amount")
    .renderHorizontalGridLines(true)
    .elasticY(true)
    .brushOn(false)
    .renderArea(true)

  dailyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%H"));
  dailyTxAmountLineChart.xAxis().ticks(d3.time.hour, 1);

  //init daily transaction num line chart
  dailyTxNumLineChart = dc.lineChart("#daily-tx-num-chart", "daily");
  dailyTxNumLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Num")
    .renderHorizontalGridLines(true)
    .mouseZoomable(true)
    .elasticY(true)
    .brushOn(false)
    .renderArea(true)

  dailyTxNumLineChart.xAxis().tickFormat(d3.time.format("%H"));
  dailyTxNumLineChart.xAxis().ticks(d3.time.hour, 1);

  //init daily miner pie chart
  dailyMinerPieChart = dc.pieChart("#daily-miner-chart", "daily");
  dailyMinerPieChart
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });

  //init daily color pie chart
  dailyColorPieChart = dc.pieChart("#daily-color-chart", "daily");
  dailyColorPieChart
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });

}

// #drawDailyChart
var drawDailyChart = function(date, data){
  var since = d3.time.day(date);
  var until = d3.time.day(new Date(date.getTime() + 24*60*60*1000));

  var crossfilter_data = crossfilter(data);
  var dailyDimension = crossfilter_data.dimension(function(b) { return b.hour });
  var amountGroup = dailyDimension.group().reduceSum(function(b) { return b.total_out; });

  dailyTxAmountLineChart.dimension(dailyDimension)
                        .group(amountGroup)
                        .x(d3.time.scale().domain([since, until]))

  dailyTxAmountLineChart.render();

  var numGroup = dailyDimension.group().reduceSum(function(b) { return b.tx_num });
  dailyTxNumLineChart.dimension(dailyDimension)
                     .group(numGroup)
                     .x(d3.time.scale().domain([since, until]))

  dailyTxNumLineChart.render();

  var minerDimension = crossfilter_data.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  dailyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  dailyMinerPieChart.render();

  var colorDimension = crossfilter_data.dimension(function(b) { return b.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.tx_num;});
  dailyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  dailyColorPieChart.render();

}


// #updateDailyDate
var updateDailyDate = function(){
  var nextDate = new Date(currentDate.getTime() + (24*60*60*1000));
  $("#date_date")[0].innerHTML = (currentDate.getMonth() + 1) + "/" + currentDate.getDate();
}

// #prevDateFunc
var prevDateFunc = function(){
  currentDate.setTime(currentDate.getTime() - (24*60*60*1000));
  ajaxLoadDaily(currentDate);
  updateDailyDate();
}

// #nextDateFunc
var nextDateFunc = function(){
  currentDate.setTime(currentDate.getTime() + (24*60*60*1000));
  ajaxLoadDaily(currentDate);
  updateDailyDate();
}

var ajaxLoadDaily = function(date) {
  $("#ajax_loader").show();
  var since = d3.time.day(date);
  var until = new Date(date.getTime()+ 24*60*60*1000);
  var url = BASE_URL;
  console.log("url = " + url);
  $.ajax({
    url: url,
    type: "GET",
    success: function(response){
      console.log("success");
      console.log(response.data);
      data = response.data;
      preprocessDaily(data)
      drawDailyChart(date, data);
      updateDailyDate();
      $("#ajax_loader").hide();
    },
    error: function(response){
      alert("Loading fail");
      console.log(url);
      console.log("load daily data error");
    }
  });
}

var preprocessDaily = function(data) {
  for (var i = 0; i < data.length; ++i){
    hour = d3.time.day(currentDate)
    data[i].hour = hour.setHours(data[i].hour)
  }
}
