var BASE_URL = "http://128.199.176.196:9000/chart/fake/";
URL = "http://140.112.29.198/py/demo/blocks";
URL = "http://127.0.0.1:8000/l_blocks.json";
var currentWeek;
var currentDate = new Date();

var dailyTxAmountLineChart;
var dailyTxNumLineChart;
var dailyMinerPieChart;
var dailyColorPieChart;

var weeklyTxAmountLineChart;
var weeklyTxNumLineChart;

var monthlyTxAmountLineChart;
var monthlyTxNumLineChart;

var dailyTimeDimension;
var weeklyTimeDimension;
var monthlyTimeDimension;

var blocks;
var lineChartHeight = 300;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 20, left: 60, right:60};



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
  var blockCF = crossfilter(data);
  var dailyDimension = blockCF.dimension(function(b) { return b.hour });

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


  var minerDimension = blockCF.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  dailyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  dailyMinerPieChart.render();

  var colorDimension = blockCF.dimension(function(b) { return b.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.tx_num;});
  dailyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  dailyColorPieChart.render();

}

// #initWeeklyChart
var initWeeklyChart = function(){
  //init weekly transaction amount chart
  weeklyTxAmountLineChart = dc.lineChart("#weekly-tx-amount-chart", "weekly");
  weeklyTxAmountLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Amount")
    .renderHorizontalGridLines(true)
    .elasticY(true)
    .brushOn(false)
    .renderArea(true)

  weeklyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%b %d"));
  weeklyTxAmountLineChart.xAxis().ticks(d3.time.day, 1);
  var amountGroup = dailyDimension.group().reduceSum(function(b) { return b.transactions.total_out; });

  dailyTxAmountLineChart.dimension(dailyDimension)
                        .group(amountGroup)
                        .x(d3.time.scale().domain([since, until]))

  dailyTxAmountLineChart.render();

  //init weekly transaction num line chart
  weeklyTxNumLineChart = dc.lineChart("#weekly-tx-num-chart", "weekly");
  weeklyTxNumLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Num")
    .elasticY(true)
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  weeklyTxNumLineChart.xAxis().tickFormat(d3.time.format("%b %d"));
  weeklyTxNumLineChart.xAxis().ticks(d3.time.day, 1);

  var numGroup = dailyDimension.group().reduceSum(function(b) { return b.transactions.tx_num });
  dailyTxNumLineChart.dimension(dailyDimension)
                     .group(numGroup)
                     .x(d3.time.scale().domain([since, until]))

  dailyTxNumLineChart.render();


  var minerDimension = blockCF.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  dailyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  dailyMinerPieChart.render();


  var colorDimension = blockCF.dimension(function(b) { return b.transactions.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.transactions.tx_num;});
  dailyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  dailyColorPieChart.render();
  

}

// #initWeeklyChart
var initWeeklyChart = function(){
  //init weekly transaction amount chart
  weeklyTxAmountLineChart = dc.lineChart("#weekly-tx-amount-chart", "weekly");
  weeklyTxAmountLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Amount")
    .renderHorizontalGridLines(true)
    .elasticY(true)
    .brushOn(false)
    .renderArea(true)

  weeklyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%b %d"));
  weeklyTxAmountLineChart.xAxis().ticks(d3.time.day, 1);


  //init weekly transaction num line chart
  weeklyTxNumLineChart = dc.lineChart("#weekly-tx-num-chart", "weekly");
  weeklyTxNumLineChart
    .width(lineChartWidth).height(lineChartHeight)
    .margins(lineChartMargins)
    .xAxisLabel("Time")
    .yAxisLabel("Transactions Num")
    .elasticY(true)
    .renderHorizontalGridLines(true)
    .brushOn(false)
    .renderArea(true)

  weeklyTxNumLineChart.xAxis().tickFormat(d3.time.format("%b %d"));
  weeklyTxNumLineChart.xAxis().ticks(d3.time.day, 1);

  //init weekly miner pie chart
  weeklyMinerPieChart = dc.pieChart("#weekly-miner-chart", "weekly");
  weeklyMinerPieChart 
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });


  //init weekly color pie chart
  weeklyColorPieChart = dc.pieChart("#weekly-color-chart", "weekly");
  weeklyColorPieChart 
    .width(pieChartWidth).height(pieChartHeight)
    .label(function(b){
        return b.key + "(" + b.value + ")";
    });

}


// #drawWeeklyChart
var drawWeeklyChart = function(date){
  var since = d3.time.week(date);
  var until = d3.time.week(new Date(date.getTime() + 7*24*60*60*1000));
  var blockCF = crossfilter(blocks);
  
  var weeklyDimension = blockCF.dimension(function(b) { return b.day; });
  console.log(weeklyDimension);

  var amountGroup = weeklyDimension.group().reduceSum(function(b) { return b.transactions.total_out; });

  weeklyTxAmountLineChart.dimension(weeklyDimension)
                        .group(amountGroup)
                        .x(d3.time.scale().domain([since, until]))

  weeklyTxAmountLineChart.render();


  var numGroup = weeklyDimension.group().reduceSum(function(b) { return b.transactions.tx_num });
  weeklyTxNumLineChart.dimension(weeklyDimension)
                     .group(numGroup)
                     .x(d3.time.scale().domain([since, until]))

  weeklyTxNumLineChart.render();


  var minerDimension = blockCF.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  weeklyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  weeklyMinerPieChart.render();



  var colorDimension = blockCF.dimension(function(b) { return b.transactions.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.transactions.tx_num;});
  weeklyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  weeklyColorPieChart.render();

}

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

  monthlyTxAmountLineChart.xAxis().tickFormat(d3.time.format("%b"));
  monthlyTxAmountLineChart.xAxis().ticks(d3.time.month, 1);


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
var drawMonthlyChart = function(date){
  var since = d3.time.year(date);
  var until = d3.time.year(new Date(date.getTime() + 365*24*60*60*1000));
  var blockCF = crossfilter(blocks);
  console.log("hi");
  var monthlyDimension = blockCF.dimension(function(b) { return b.week });

  var amountGroup = monthlyDimension.group().reduceSum(function(b) { return b.transactions.total_out; });

  monthlyTxAmountLineChart.dimension(monthlyDimension)
                        .group(amountGroup)
                        .x(d3.time.scale().domain([since, until]))

  monthlyTxAmountLineChart.render();

  var numGroup = monthlyDimension.group().reduceSum(function(b) { return b.transactions.tx_num });
  monthlyTxNumLineChart.dimension(monthlyDimension)
                     .group(numGroup)
                     .x(d3.time.scale().domain([since, until]))

  monthlyTxNumLineChart.render();


  var minerDimension = blockCF.dimension(function(b) { return b.miner });
  var minerGroup = minerDimension.group().reduceCount();

  monthlyMinerPieChart.dimension(minerDimension)
                    .group(minerGroup)
                    .label(function(b){
                        return b.key + "(" + b.value + ")";
                    });

  monthlyMinerPieChart.render();


  var colorDimension = blockCF.dimension(function(b) { return b.transactions.color });
  var colorGroup = colorDimension.group().reduceSum(function(b) { return b.transactions.tx_num;});
  monthlyColorPieChart.dimension(colorDimension)
                    .group(colorGroup)
                    .label(function(b){
                      return b.key + "(" + b.value + ")";
                    });

  monthlyColorPieChart.render();

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

var updateWeekDate = function(){
  var nextWeek = new Date(currentWeek.getTime() + (7*24*60*60*1000));
  nextWeek = d3.time.week(nextWeek);
  $("#week_date")[0].innerHTML = (currentWeek.getMonth() + 1) + "/" + currentWeek.getDate() + " ~ " + (nextWeek.getMonth() + 1) + "/" + nextWeek.getDate();
}

var prevWeekFunc = function(){
  console.log("prevWeek");
  currentWeek.setTime(currentWeek.getTime() - (7*24*60*60*1000) );
  currentWeek = d3.time.week(currentWeek);
  ajaxLoadWeekly(currentWeek);
  updateWeekDate();
}

var nextWeekFunc = function(){
  console.log("next week");
  currentWeek.setTime(currentWeek.getTime() + (7*24*60*60*1000));
  currentWeek = d3.time.week(currentWeek);
  ajaxLoadWeekly(currentWeek);
  updateWeekDate();
}




var gdata;
var dailyBlocks;
// #ajaxLoadDaily
var ajaxLoadDaily = function(date) {
  $("#ajax_loader").show();
  var since = d3.time.day(date);
  var until = new Date(date.getTime()+ 24*60*60*1000);
  var url = BASE_URL + "?since=" + since.getTime()/1000 + "&until=" + until.getTime()/1000;
  //url = "http://127.0.0.1:8000/l_blocks.json";
  url = 'http://128.199.176.196:9000/chart/fake/'
  console.log("url = " + url);
  $.ajax({
    url: url,
    type: "GET",
    success: function(response){
      console.log("success");
      console.log(response.data);
      //blocks = preprocessBlocks(response.data);
      console.log(blocks);
      data = response.data;
      preprocessDaily(data)
      drawDailyChart(date, data);
      updateDailyDate();
      $("#ajax_loader").hide();
    },
    error: function(response){
      console.log("load daily data error");
    }
  });
}

// #ajaxLoadWeekly
var ajaxLoadWeekly = function(date) {
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
      console.log("ajaxLoadWeekly blocks");
      drawWeeklyChart(date);
      updateWeekDate();
      $("#ajax_loader").hide();
    },
    error: function(response){
      console.log("load daily data error");
    }
  });
}


// #ajaxLoadMonthly
var ajaxLoadMonthly = function(date) {
  $("#ajax_loader").show();
  var since = d3.time.year(date);
  var until = d3.time.year(new Date(date.getTime() + 356*7*24*60*60*1000));
  var url = BASE_URL + "?since=" + since.getTime()/1000 + "&until=" + until.getTime()/1000;

  //url = "http://127.0.0.1:8000/blocks.json";
  console.log("url=" + url);
  $.ajax({
    url: url, 
    type: "GET",
    success: function(response){
      console.log("success");
      blocks = preprocessBlocks(response.blocks);
      console.log(blocks);
      drawMonthlyChart(date);
      $("#ajax_loader").hide();
    },
    error: function(response){
      console.log("load daily data error");
    }
  });
}


var preprocessDaily = function(data) {
    for (var i = 0; i < data.length; ++i){
        hour = d3.time.day(new Date())
        data[i].hour = hour.setHours(data[i].hour)
    }
}

// #preprocessBlocks
var preprocessBlocks = function(oldBlks) {
  var blks = new Array();
  for(var i = 0; i < oldBlks.length; ++i){
    for(var j = 0; j < oldBlks[i].transactions.length; ++j){
      var newBlk = new Object();
      for(var attr in oldBlks[i]){
        newBlk[attr] = oldBlks[i][attr];
      }
      newBlk.transactions = oldBlks[i].transactions[j];
      newBlk.time = new Date(newBlk.time * 1000);
      newBlk.hour = d3.time.hour(newBlk.time);
      newBlk.week = d3.time.week(newBlk.time);
      newBlk.day = d3.time.day(newBlk.time);
      blks.push(newBlk);
    }
  }
  return blks;
}



