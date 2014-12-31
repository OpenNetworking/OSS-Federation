var BASE_URL;
var currentMonth;
var monthlyTxAmountLineChart;
var monthlyTxNumLineChart;
var monthlyMinerPieChart;
var monthlyColorPieChart;

var monthlyTimeDimension;

var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right:60};

$( document ).ready(function() {
    BASE_URL = $("#chart_api_url")[0].value;
    currentMonth = d3.time.month(new Date());
    initMonthlyChart()
    ajaxLoadMonthly(currentMonth);
    updateMonthIndicator(currentMonth);
    $("#prev_month").bind("click", prevMonthFunc);
    $("#next_month").bind("click", nextMonthFunc);
});

// #initMonthlyChart
var initMonthlyChart = function(){
  //init monthly transaction amount chart
  monthlyTxAmountLineChart = dc.lineChart("#monthly-tx-amount-chart", "monthly");
  monthlyTxAmountLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .elasticY(true)
    .yAxisLabel("Transactions Amount")
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  monthlyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%d"));
  monthlyTxAmountLineChart.xAxis().ticks(d3.time.day, 1);


  //init monthly transaction num line chart
  monthlyTxNumLineChart = dc.lineChart("#monthly-tx-num-chart", "monthly");
  monthlyTxNumLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .elasticY(true)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Num")
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  monthlyTxNumLineChart.xAxis().tickFormat(d3.time.format("%d"));
  monthlyTxNumLineChart.xAxis().ticks(d3.time.day, 1);

  //init monthly miner pie chart
  monthlyMinerPieChart = dc.pieChart("#monthly-miner-chart", "monthly");
  monthlyMinerPieChart
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });


  //init monthly color pie chart
  monthlyColorPieChart = dc.pieChart("#monthly-color-chart", "monthly");
  monthlyColorPieChart
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });

}

// #drawMonthlyChart
var drawMonthlyChart = function(data){
  var since = currentMonth;
  var until = nextMonth(currentMonth);
  until = new Date(until.getTime() - 24*60*60*1000);
  var crossfilter_data = crossfilter(data);
  var monthlyDimension = crossfilter_data.dimension(function(b) { return b.day });

  var amountGroup = monthlyDimension.group().reduceSum(function(b) { return b.total_out; });

  monthlyTxAmountLineChart.dimension(monthlyDimension)
                        .group(amountGroup)
                        .x(d3.time.scale().domain([since, until]))

  monthlyTxAmountLineChart.render();

  var numGroup = monthlyDimension.group().reduceSum(function(b) { return b.tx_num });
  monthlyTxNumLineChart.dimension(monthlyDimension)
                     .group(numGroup)
                     .x(d3.time.scale().domain([since, until]))

  monthlyTxNumLineChart.render();


  var minerDimension = crossfilter_data.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  monthlyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  monthlyMinerPieChart.render();


  var colorDimension = crossfilter_data.dimension(function(b) { return b.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.tx_num;});
  monthlyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  monthlyColorPieChart.render();

}


var prevMonth = function(now){
  var year = now.getFullYear();
  var month = now.getMonth();
  if( month === 0){
    year = year - 1;
    month = 11
  } else {
    month = month - 1;
  }
  return d3.time.month(new Date(year, month, 1));
}

var nextMonth = function(now){
  var year = now.getFullYear();
  var month = now.getMonth();
  if( month === 11){
    year = year + 1;
    month = 0
  } else {
    month = month + 1;
  }
  return d3.time.month(new Date(year, month, 1));
}

var updateMonthIndicator = function(now){
  $("#month-indicator")[0].innerHTML = now.getFullYear() + "/" + (now.getMonth()+1);
}

var prevMonthFunc = function(){
  currentMonth = prevMonth(currentMonth);
  ajaxLoadMonthly(currentMonth);
  updateMonthIndicator(currentMonth);
}

var nextMonthFunc = function(){
  currentMonth = nextMonth(currentMonth);
  ajaxLoadMonthly(currentMonth);
  updateMonthIndicator(currentMonth);
}

var initData = [
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 1},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 2},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 3},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 4},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 5},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 6},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 7},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 10},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 11},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 12},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 13},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 14},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 15},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 16},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 17},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 18},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 19},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 20},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 21},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 22},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 23},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 24},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 25},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 26},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 27},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 28},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 29},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 30},
    {"color": 0, "miner":"", "total_out": 0, "tx_num": 0, "day": 31},
];
var ajaxLoadMonthly = function(now) {
  $("#ajax_loader").show();
  var since = now;
  var until = nextMonth(now);
  var url = BASE_URL +
            "/year/" + currentMonth.getFullYear() +
            "/month/" + (currentMonth.getMonth() + 1) + "/";
  $.ajax({
    url: url,
    type: "GET",
    success: function(response){
      console.log("success");
      console.log(response.data)
      /*
      for(var i = 0; i < initData.length; ++i){
         response.data.push(initData[i]);
      }
      */
      preprocessData(response.data);
      drawMonthlyChart(response.data);
      $("#ajax_loader").hide();
    },
    error: function(response){
      console.log(url);
      console.log("load daily data error");
    }
  });
}

var preprocessData = function(data) {
    var month = currentMonth.getMonth();
    var year = currentMonth.getFullYear();
    for (var i = 0; i < data.length; ++i){
        data[i].day = d3.time.day(new Date(year, month, data[i].day))
    }
}
