var BASE_URL = "59.151.30.38:5567/chart/fakeyear/";

var currentYear;

var yearlyTxAmountLineChart;
var yearlyTxNumLineChart;
var yearlyMinerPieChart;
var yearlyColorPieChart;

var yearlyTimeDimension;

var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right:60};

$( document ).ready(function() {
    currentYear = d3.time.year(new Date());
    initYearlyChart()
    ajaxLoadYearly(currentYear);
    updateYearIndicator(currentYear);
    $("#prev_year").bind("click", prevYearFunc);
    $("#next_year").bind("click", nextYearFunc);
});

// #initYearlyChart
var initYearlyChart = function(){
  //init yearly transaction amount chart
  yearlyTxAmountLineChart = dc.lineChart("#yearly-tx-amount-chart", "yearly");
  yearlyTxAmountLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .elasticY(true)
    .yAxisLabel("Transactions Amount")
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  yearlyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%b"));
  yearlyTxAmountLineChart.xAxis().ticks(d3.time.month, 1);


  //init yearly transaction num line chart
  yearlyTxNumLineChart = dc.lineChart("#yearly-tx-num-chart", "yearly");
  yearlyTxNumLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .elasticY(true)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Num")
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  yearlyTxNumLineChart.xAxis().tickFormat(d3.time.format("%b"));
  yearlyTxNumLineChart.xAxis().ticks(d3.time.month, 1);

  //init yearly miner pie chart
  yearlyMinerPieChart = dc.pieChart("#yearly-miner-chart", "yearly");
  yearlyMinerPieChart
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });


  //init yearly color pie chart
  yearlyColorPieChart = dc.pieChart("#yearly-color-chart", "yearly");
  yearlyColorPieChart
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });

}

// #drawYearlyChart
var drawYearlyChart = function(data){
  var since = currentYear;
  var until = nextYear(currentYear);
  var crossfilter_data = crossfilter(data);
  var yearlyDimension = crossfilter_data.dimension(function(b) { return b.month });

  var amountGroup = yearlyDimension.group().reduceSum(function(b) { return b.total_out; });

  yearlyTxAmountLineChart.dimension(yearlyDimension)
                        .group(amountGroup)
                        .x(d3.time.scale().domain([since, until]))

  yearlyTxAmountLineChart.render();

  var numGroup = yearlyDimension.group().reduceSum(function(b) { return b.tx_num });
  yearlyTxNumLineChart.dimension(yearlyDimension)
                     .group(numGroup)
                     .x(d3.time.scale().domain([since, until]))

  yearlyTxNumLineChart.render();


  var minerDimension = crossfilter_data.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  yearlyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  yearlyMinerPieChart.render();


  var colorDimension = crossfilter_data.dimension(function(b) { return b.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.tx_num;});
  yearlyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  yearlyColorPieChart.render();

}


var prevYear = function(now){
  return d3.time.year(new Date(now.getFullYear()-1, 1, 1));
}

var nextYear = function(now){
  return d3.time.year(new Date(now.getFullYear()+1, 1, 1));
}

var updateYearIndicator = function(now){
  console.log(now.getFullYear());
  $("#year-indicator")[0].innerHTML = "" + now.getFullYear();
}

var prevYearFunc = function(){
  currentYear = prevYear(currentYear);
  ajaxLoadYearly(currentYear);
  updateYearIndicator(currentYear);
}

var nextYearFunc = function(){
  currentYear = nextYear(currentYear);
  ajaxLoadYearly(currentYear);
  updateYearIndicator(currentYear);
}

var ajaxLoadYearly = function(now) {
  $("#ajax_loader").show();
  var since = now;
  var until = nextYear(now);
  url = BASE_URL;
  $.ajax({
    url: url,
    type: "GET",
    success: function(response){
      console.log("success");
      console.log(response.data)
      preprocessData(response.data);
      drawYearlyChart(response.data);
      $("#ajax_loader").hide();
    },
    error: function(response){
        console.log(url);
      console.log("load daily data error");
    }
  });
}

var preprocessData = function(data) {
    var year = currentYear.getFullYear();
    for (var i = 0; i < data.length; ++i){
        data[i].month = d3.time.month(new Date(year, data[i].month-1, 1))
    }
}
