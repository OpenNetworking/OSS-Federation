
// some global variable
var BASE_URL;
var gTimeObj;
var txData;
var loaderImg;

var YEAR = 1;
var MONTH = 2;
var DAY = 3;

$( document ).ready(function() {
    initDatePickerBtn();
    initDateTimePicker();

    // prepare chart api url
    BASE_URL = $("#chart_api_url")[0].value;

    // prepare loader image url
    loaderImg = $("#loader-img").css("background-image");

    $("#color-select-all").bind("click", function(event) {
        $("input[name='color-filter']").each(function() {
            $(this).prop("checked", $("#color-select-all").prop("checked"));
        });
    });

    $("#issuer-select-all").bind("click", function(event) {
        $("input[name='issuer-filter']").each(function() {
            $(this).prop("checked", $("#issuer-select-all").prop("checked"));
        });
    });

    $("#submit-btn").bind("click", function(event) {
        loadData();
    });

    initTxAmountChart();
    initTxNumChart();
    initIssuerChart();
    initColorChart();
    // first time load data
    loadData();
});

var updateTimeIndicator = function(unit, date) {
    var m = moment(date);
    switch(unit) {
        case DAY:
            $("#time-indicator")[0].innerHTML = m.format("YYYY/MM/DD");
            break;
        case MONTH:
            $("#time-indicator")[0].innerHTML = m.format("YYYY/MM");
            break;
        case YEAR:
            $("#time-indicator")[0].innerHTML = m.format("YYYY");
            break;
    }
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
    console.log("ok");
}

var issuerChart;
var colorChart;
var txAmountChart;
var txNumChart;

var lineChartHeight = 150;
var lineChartWidth = 600;
var pieChartHeight = 150;
var pieChartWidth = 150;
var lineChartMargins = {top: 30, bottom: 30, left: 60, right: 60};


var initIssuerChart = function() {
    var width = $("#issuer-chart").width();
    var height = $("#issuer-panel").height() - $("#issuer-heading").height()
    issuerChart = dc.pieChart("#issuer-chart", "chart");
    issuerChart.width(width).height(height)
               .slicesCap(4)
               .legend(dc.legend().x(width+20).y(30).itemHeight(10).gap(10));
}

var initColorChart = function() {
    var width = $("#color-chart").width();
    var height = $("#color-panel").height() - $("#color-heading").height()
    colorChart = dc.pieChart("#color-chart", "chart");
    colorChart.width(width).height(height)
              .slicesCap(4)
              .legend(dc.legend().x(width+20).y(30).itemHeight(10).gap(10));
}

var initTxAmountChart = function() {
    var width = $("#tx-amount-panel").width();
    var height = $("#tx-amount-panel").height() - $("#tx-amount-heading").height();
    txAmountChart = dc.lineChart("#tx-amount-chart", "chart");
    txAmountChart
        .width(width).height(height)
        .margins(lineChartMargins)
        .xAxisLabel("時間")
        .renderHorizontalGridLines(true)
        .elasticY(true)
        .brushOn(false)
        .renderArea(true);

    txAmountChart.renderlet(function(chart){chart.selectAll("circle.dot").style("fill-opacity", 1).on('mousemove', null).on('mouseout', null);});
}

var initTxNumChart = function() {
    var width = $("#tx-num-panel").width();
    var height = $("#tx-num-panel").height() - $("#tx-num-heading").height();
    txNumChart = dc.lineChart("#tx-num-chart", "chart");
    txNumChart
        .width(width).height(height)
        .margins(lineChartMargins)
        .xAxisLabel("時間")
        .elasticY(true)
        .renderHorizontalGridLines(true)
        .brushOn(false)
        .renderArea(true);
    txNumChart.renderlet(function(chart){chart.selectAll("circle.dot").style("fill-opacity", 1).on('mousemove', null).on('mouseout', null);});

}

var drawDayChart = function(date, data) {
    console.log(data);
    console.log(date);
    for(var i = 0; i < data.length; ++i){
        hour = d3.time.day(date);
        data[i].hour = hour.setHours(data[i].hour);
        data[i].total_out = data[i].total_out.toFixed();
        data[i].issuer_name = issuer_mapper[data[i].issuer];
        data[i].color_name = color_mapper[data[i].color];
    }

    date = d3.time.day(date);
    var since = moment(date);
    var until = moment(date);
    until = until.add(moment.duration({"hours": 23}));
    since = d3.time.hour(since.toDate());
    until = d3.time.hour(until.toDate());

    var crossfilter_data = crossfilter(data);
    var dim = crossfilter_data.dimension(function(t) { return t.hour; });
    var g = dim.group().reduceSum(function(t) { return t.total_out; });
    txAmountChart.dimension(dim)
                 .group(g)
                 .x(d3.time.scale().domain([since, until]));

    txAmountChart.xAxis().tickFormat(d3.time.format("%H"));
    txAmountChart.xAxis().ticks(d3.time.hour, 1);
    txAmountChart.yAxis().ticks(5);
    txAmountChart.render();

    var g2 = dim.group().reduceSum(function(t) { return t.tx_num; });

    txNumChart.dimension(dim)
              .group(g2)
              .x(d3.time.scale().domain([since, until]));

    txNumChart.xAxis().tickFormat(d3.time.format("%H"));
    txNumChart.xAxis().ticks(d3.time.hour, 1);
    txNumChart.yAxis().ticks(5);
    txNumChart.render();


    var issuerDim = crossfilter_data.dimension(function(t) {
        if (t.issuer === null) {
            return "0";
        } else {
            return t.issuer_name;
        }
    });

    var g3 = issuerDim.group().reduceSum(function(t) {return t.tx_num;});

    issuerChart.dimension(issuerDim)
               .group(g3)

    issuerChart.render();

    var colorDim = crossfilter_data.dimension(function(t) {return t.color_name;});
    var g4 = colorDim.group().reduceSum(function(t) {return t.tx_num;});
    colorChart.dimension(colorDim)
               .group(g4)

    colorChart.render();
}


var drawMonthChart = function(date, data) {

    for(var i = 0; i < data.length; ++i){
        day = d3.time.month(date);
        data[i].day = day.setDate(data[i].day);
        data[i].total_out = data[i].total_out.toFixed();
        data[i].issuer_name = issuer_mapper[data[i].issuer];
        data[i].color_name = color_mapper[data[i].color];
    }

    date = d3.time.month(date);
    var since = moment(date);
    var until = moment(date);
    until = until.add(moment.duration({"months": 1}));
    until = until.subtract(moment.duration({"days": 1}));
    since = d3.time.day(since.toDate());
    until = d3.time.day(until.toDate());

    var crossfilter_data = crossfilter(data);
    var dim = crossfilter_data.dimension(function(t) { return t.day; });
    var g = dim.group().reduceSum(function(t) { return t.total_out; });

    txAmountChart.dimension(dim)
                 .group(g)
                 .x(d3.time.scale().domain([since, until]));

    txAmountChart.xAxis().tickFormat(d3.time.format("%d"));
    txAmountChart.xAxis().ticks(d3.time.day, 1);
    txAmountChart.yAxis().ticks(5);
    txAmountChart.render();

    var g2 = dim.group().reduceSum(function(t) { return t.tx_num; });

    txNumChart.dimension(dim)
              .group(g2)
              .x(d3.time.scale().domain([since, until]));

    txNumChart.xAxis().tickFormat(d3.time.format("%d"));
    txNumChart.xAxis().ticks(d3.time.day, 1);
    txNumChart.render();


    var issuerDim = crossfilter_data.dimension(function(t) {if (t.issuer === null) return "0"; else return t.issuer_name;});
    var g3 = issuerDim.group().reduceSum(function(t) {return t.tx_num;});
    issuerChart.dimension(issuerDim)
               .group(g3)

    issuerChart.render();
    var colorDim = crossfilter_data.dimension(function(t) {return t.color_name;});
    var g4 = colorDim.group().reduceSum(function(t) {return t.tx_num;});
    colorChart.dimension(colorDim)
               .group(g4)

    colorChart.render();
}

var drawYearChart = function(date, data) {
    for(var i = 0; i < data.length; ++i){
        month = d3.time.month(date);
        data[i].month = month.setMonth(data[i].month-1);
        data[i].total_out = data[i].total_out.toFixed();
        data[i].issuer_name = issuer_mapper[data[i].issuer];
        data[i].color_name = color_mapper[data[i].color];
    }

    date = d3.time.year(date);
    var since = moment(date);
    var until = moment(date);
    until = until.add(moment.duration({"months": 11}));
    since = d3.time.month(since.toDate());
    until = d3.time.month(until.toDate());

    var crossfilter_data = crossfilter(data);
    var dim = crossfilter_data.dimension(function(t) { return t.month; });
    var g = dim.group().reduceSum(function(t) { return t.total_out; });
    txAmountChart.dimension(dim)
                 .group(g)
                 .x(d3.time.scale().domain([since, until]));

    txAmountChart.xAxis().tickFormat(d3.time.format("%b"));
    txAmountChart.xAxis().ticks(d3.time.month, 1);
    txAmountChart.render();

    var g2 = dim.group().reduceSum(function(t) { return t.tx_num; });

    txNumChart.dimension(dim)
              .group(g2)
              .x(d3.time.scale().domain([since, until]));

    txNumChart.xAxis().tickFormat(d3.time.format("%b"));
    txNumChart.xAxis().ticks(d3.time.month, 1);
    txNumChart.render();


    var issuerDim = crossfilter_data.dimension(function(t) {
        if (t.issuer === null) {
            return "0";
        } else {
            return t.issuer_name;
        }
    });
    var g3 = issuerDim.group().reduceSum(function(t) {return t.tx_num;});
    issuerChart.dimension(issuerDim)
               .group(g3)

    issuerChart.render();
    var colorDim = crossfilter_data.dimension(function(t) {return t.color_name;});
    var g4 = colorDim.group().reduceSum(function(t) {return t.tx_num;});
    colorChart.dimension(colorDim)
               .group(g4)

    colorChart.render();
}

var makeURL = function() {

    // build issuer filter parameters
    var issuer_address = [];
    if ($("#issuer-select-all").prop("checked") === false) {
        var issuer_filter = $("input[name='issuer-filter']");
        var address = [];
        for(var i = 0; i < issuer_filter.length; i++) {
            var tmp = issuer_filter[i].value;
            if(tmp != "") {
                address.push(tmp);
            }
        }
    }

    // build color filter parameters
    var color_str = "";
    var color_address = [];
    if ($("#color-select-all").prop("checked") === false) {
        var color_filter = $("input[name='color-filter']");
        for(var i = 0; i < color_filter.length; i++) {
            var tmp = color_filter[i].value;
            if(tmp != "") {
               color_address.push(tmp);
            }
        }
    }

    // build time filter parameters
    var time_str;
    if ($("#day-btn").hasClass("active")) {
        var date = $("#day-picker").data("DateTimePicker").date();
        if (date === null) {
            date = moment();
        }
        time_str = date.format("/[year]/YYYY/[month]/M/[day]/D/");
        console.log("day timestr");
    } else if ($("#month-btn").hasClass("active")) {
        var date = $("#month-picker").data("DateTimePicker").date();
        if (date === null) {
            date = moment();
        }
        time_str = date.format("/[year]/YYYY/[month]/M/");
        console.log("month timestr");
    } else {
        var date = $("#year-picker").data("DateTimePicker").date();
        if (date === null) {
            date = moment();
        }
        time_str = date.format("/[year]/YYYY/");
        console.log("year timestr");
    }

    console.log(issuer_address);
    console.log(color_address);

    var url = "/statistics/txs" + time_str;
    if (issuer_address.length > 0 || color_address.length > 0) {
         url += "?"
         if(issuer_address.length > 0) {
             url += "issuer=" + issuer_address.join(",");
             if (color_address.length > 0) {
                url += "&color=" + color_address.join(",");
             }
         } else {
             if (color_address.length > 0) {
                url += "color=" + color_address.join(",");
             }
         }
    }
    console.log(url);
    console.log("hi");
    return url;
}

var getTimeUnit = function() {
    if ($("#day-btn").hasClass("active")) {
        return DAY;
    } else if ($("#month-btn").hasClass("active")) {
        return MONTH;
    } else {
        return YEAR;
    }
}

var getTimeByUnit = function(unit) {
    var date;
    switch(unit) {
        case DAY:
            date = $("#day-picker").data("DateTimePicker").date();
            break;
        case MONTH:
            date = $("#month-picker").data("DateTimePicker").date();
            break;
        case YEAR:
            date = $("#year-picker").data("DateTimePicker").date();
            break;
    }
    if (date === null) {
        var tmp = moment();
        return tmp.toDate();
    }
    console.log('+++++++++++++++++++');
    console.log(date);
    return date.toDate();
}

var drawChart = function(unit, date, data) {
    switch(unit) {
        case DAY:
            drawDayChart(date, data);
            break;
        case MONTH:
            drawMonthChart(date, data);
            break;
        case YEAR:
            drawYearChart(date, data);
            break;
    }
}

var loading = function() {
    $("#issuer-panel").css("background-image", loaderImg);
    $("#color-panel").css("background-image", loaderImg);
    $("#tx-amount-panel").css("background-image", loaderImg);
    $("#tx-num-panel").css("background-image", loaderImg);
    $("#tx-amount-chart").hide();
    $("#tx-num-chart").hide();
    $("#issuer-chart").hide();
    $("#color-chart").hide();
}

var finishing = function() {
    $("#tx-amount-chart").show();
    $("#tx-num-chart").show();
    $("#issuer-chart").show();
    $("#color-chart").show();
    $("#issuer-panel").css("background-image", "");
    var w = $("#issuer-chart svg").width();
    $("#issuer-chart svg").width(w+100);
    $("#color-panel").css("background-image", "");
    w = $("#color-chart svg").width();
    $("#color-chart svg").width(w+100);
    $("#tx-amount-panel").css("background-image", "");
    $("#tx-num-panel").css("background-image", "");
}

var loadData = function() {
    var url = BASE_URL + makeURL();
    console.log(url);
    loading();
    $.ajax({
        url: url,
        method: "GET",
        success: function(response){
            console.log("success");
            console.log(response);
            data = response.data
            console.log(data);
            unit = getTimeUnit();
            console.log("unit=" + unit);
            date = getTimeByUnit(unit);
            console.log(date);
            updateTimeIndicator(unit, date);
            drawChart(unit, date, data);
            finishing();
            console.log("finish");
        },
        error: function(response) {
            console.log("error");
        }
    });
}
