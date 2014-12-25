var BASE_URL = "http://128.199.176.196:9000/chart/fake/";

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
    currentMonth = d3.time.
    initMonthlyChart()
    ajaxLoadMontly(currentMonth)
});

// #initMonthlyChart
var initMonthlyChart = function(){
  //init monthly transaction amount chart
  monthlyTxAmountLineChart = dc.lineChart("#monthly-tx-amount-chart", "monthly");
  monthlyTxAmountLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Amount")
    .renderHorizontalGridLines(true)
    .elasticY(true)
    .brushOn(false)
    .renderArea(true)

  monthlyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%b"));
  monthlyTxAmountLineChart.xAxis().ticks(d3.time.month, 1);


  //init monthly transaction num line chart
  monthlyTxNumLineChart = dc.lineChart("#monthly-tx-num-chart", "monthly");
  monthlyTxNumLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Num")
    .elasticY(true)
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  monthlyTxNumLineChart.xAxis().tickFormat(d3.time.format("%b"));
  monthlyTxNumLineChart.xAxis().ticks(d3.time.month, 1);

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
var drawMonthlyChart = function(date, data){
  var since = d3.time.month(date);
  var until = nextMonth(date);
  var crossfilter_data = crossfilter(data);
  var monthlyDimension = crossfilter_data.dimension(function(b) { return b.month; });
  console.log(monthlyDimension);
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


var nextMonth(date){
    date = d3.time.month(date)
    year = date.getFullYear()
    month = date.getMonth()
    if(m === 11){
        year = year + 1
        month = 0
    } else {
        month = month + 1
    }
    return d3.time.month(new Date(year, month, 1))
}

var prevMonth(date){
    date = d3.time.month(date)
    year = date.getFullYear()
    month = date.getMonth()
    if(m === 0){
        year = year - 1
        month = 11
    } else {
        month = month - 1
    }
    return d3.time.month(new Date(year, month, 1))
}

var updateMonthDate = function(){
  next_month = nextMonth(currentMonth);
  $("#month_date")[0].innerHTML = (currentMonth.getMonth() + 1) + " ~ " + (next_month.getMonth() + 1);
}

var prevMonthFunc = function(){
  console.log("prevWeek");
  currentMonth = prevMonth(currentMonth);
  ajaxLoadMonthly(currentMonth);
  updateMonthDate();
}

var nextMonthFunc = function(){
  currentMonth = nextMonth(currentMonth);
  ajaxLoadMonthly(currentMonth);
  updateMonthDate();
}

// #ajaxLoadMonthly
var ajaxLoadMonthly = function(date) {
  $("#ajax_loader").show();
  var since = d3.time.week(date);
  var until = d3.time.week(new Date(date.getTime() + 7*24*60*60*1000));
  var url = BASE_URL + "?since=" + since.getTime()/1000 + "&until=" + until.getTime()/1000;
  //url = "http://127.0.0.1:8000/blocks.json";
  console.log("url=" + url);
  $.ajax({
    url: url,
    type: "GET",
    success: function(response){
      console.log("success");
      blocks = preprocessBlocks(response.blocks);
      console.log("ajaxLoadMonthly blocks");
      drawMonthlyChart(date);
      updateWeekDate();
      $("#ajax_loader").hide();
    },
    error: function(response){
      console.log("load daily data error");
    }
  });
}

var preprocessMonthly = function(data) {
    for (var i = 0; i < data.length; ++i){
        var month = d3.time.Month(currentMonth)
        data[i].month = month.setMonth(data[i].month)
    }
}


