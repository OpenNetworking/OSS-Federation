/*
 * TimeObj is a class that wrap some useful function related to handle
 * moment object (moment object is defined in moment.js)
 */

function TimeObj() {
    this.now = moment();
    this.resetTime()
    this.YEAR_INTERVAL = 1;
    this.MONTH_INTERVAL = 2;
    this.DAY_INTERVAL = 3;
    this.interval = this.DAY_INTERVAL;
}

TimeObj.prototype.next = function() {
    switch(this.interval){
        case this.DAY_INTERVAL:
            this.now.add(moment.duration({"days": 1}));
            break;
        case this.MONTH_INTERVAL:
            this.now.add(moment.duration({"months": 1}));
            break;
        case this.YEAR_INTERVAL:
            this.now.add(moment.duration({"years": 1}));
            break;
    }
}

TimeObj.prototype.prev = function() {
    switch(this.interval){
        case this.DAY_INTERVAL:
            this.now.subtract(moment.duration({"days": 1}));
            break;
        case this.MONTH_INTERVAL:
            this.now.subtract(moment.duration({"months": 1}));
            break;
        case this.YEAR_INTERVAL:
            this.now.subtract(moment.duration({"years": 1}));
            break;
    }
}

TimeObj.prototype.getSinceUntil = function() {
    var since = this.now.unix();
    this.next();
    var until = this.now.unix();
    this.prev();
    return [since, until]
}

TimeObj.prototype.resetTime = function(){
    switch(this.interval){
        case this.DAY_INTERVAL:
            this.now = moment().startOf("day");
            break;
        case this.MONTH_INTERVAL:
            this.now = moment().startOf("month");
            break;
        case this.YEAR_INTERVAL:
            this.now = moment().startOf("year");
            break;
    }
}

TimeObj.prototype.changeInterval = function(newInterval){
    this.interval = newInterval;
    this.resetTime();
}

TimeObj.prototype.yearInterval = function() {
    this.changeInterval(this.YEAR_INTERVAL);
}

TimeObj.prototype.monthInterval = function() {
    this.changeInterval(this.MONTH_INTERVAL);
}

TimeObj.prototype.dayInterval = function() {
    this.changeInterval(this.DAY_INTERVAL);
}

TimeObj.prototype.getTimeIndicator = function() {
    var str;
    switch(this.interval){
        case this.DAY_INTERVAL:
            str = this.now.format("YYYY/MM/DD");
            break;
        case this.MONTH_INTERVAL:
            str = this.now.format("MMM");
            break;
        case this.YEAR_INTERVAL:
            str = this.now.format("YYYY");
            break;
    }
    return str;
}
