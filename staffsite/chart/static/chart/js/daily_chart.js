var BASE_URL;

var currentDate;
var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right:60};

$( document ).ready( function() {
    BASE_URL = $("#chart_api_url")[0].value;
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
  var tmp1 = new Date(date.getTime());
  var tmp2 = new Date(date.getTime());
  tmp1.setHours(0);
  tmp2.setHours(23);
  var since = d3.time.hour(tmp1);
  var until = d3.time.hour(tmp2);

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
  var nextDate = new Date(currentDate.getTime() + (23*60*60*1000));
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

var initData = [
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 0},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 1},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 2},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 3},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 4},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 5},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 6},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 7},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 8},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 9},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 10},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 11},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 12},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 13},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 14},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 15},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 16},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 17},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 18},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 19},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 20},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 21},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 22},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "hour": 23},
];
var ajaxLoadDaily = function(date) {
  $("#ajax_loader").show();
  var since = d3.time.day(date);
  var until = new Date(date.getTime()+ 24*60*60*1000);
  var url = BASE_URL + '/statistics/blocks' +
            "/year/" + currentDate.getFullYear() +
            "/month/" + (currentDate.getMonth() + 1) +
            "/day/" + currentDate.getDate() + "/";
  $.ajax({
    url: url,
    type: "GET",
    success: function(response){
      console.log("success");
      console.log(response.data);
      for(var i = 0; i < initData.length; ++i){
         response.data.push(initData[i]);
      }
      preprocessDaily(response.data)
      drawDailyChart(date, response.data);
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
