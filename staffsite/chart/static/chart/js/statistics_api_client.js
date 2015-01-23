/*
 * Statistics api client
 */

BASE_URL = $("#chart_api_url")[0].value;

function Statistics(config) {
    var defaultConfig = {};
    defaultConfig.baseURL = $("#chart_api_url")[0].value;
    defaultConfig.accessToken = "Token 867865a1e0ed3f19cf3db3bf43d500e6c28167aa";
    var config = config || defaultConfig
    this.accessToken = config.accessToken;
    this.baseURL = config.baseURL;
}

Statistics.prototype.buildQs = function(params) {
    console.log(params)
    params = params || {};
    var qs = jQuery.param(params);
    console.log("qs=" + qs);
    if (qs === "") {
        return "";
    } else {
        return "?" + qs;
    }
}

Statistics.prototype.get = function(url, error, success) {
    console.log("GET URL: " + url);
    var args = {
        url: url,
        type: "GET",
        dataType: "json",
        accept: "application/json",
        success: success,
        error: error,
    };
    jQuery.ajax(args);
}

Statistics.prototype.getAEInfo = function(params, error, success) {
    console.log("getAEinfo")
    var params = params || {}
    var endpoint = '/aeinfo/';
    var url = this.baseURL + endpoint + this.buildQs(params);
    this.get(url, error, success);
};

Statistics.prototype.getOrphan = function(params, error, success) {
    var params = params || {}
    var endpoint = '/orphan/';
    var url = this.baseURL + endpoint + this.buildQs(params);
    this.get(url, error, success);
}

Statistics.prototype.getBandwidth = function(params, error, success) {
    var params = params || {}
    var endpoint = '/bandwidth/';
    var url = this.baseURL + endpoint + this.buildQs(params);
    this.get(url, error, success);
}

Statistics.prototype.getRtt = function(params, error, success) {
    var params = params || {}
    var endpoint = '/rtt/';
    var url = this.baseURL + endpoint + this.buildQs(params);
    this.get(url, error, success);
}

Statistics.prototype.test = function(params, error, success) {
    console.log('test');
    var endpoint = '/qqq/'
    var url = "http://128.199.176.196:9000/chart" + endpoint + this.buildQs(params)
    this.get(url, error, success)
}
