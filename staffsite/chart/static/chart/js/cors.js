


$( document ).ready(function() {

    /*
    var request = {
        url: "https://api.parse.com/1/classes/events/",
        headers : {
            "X-Parse-Application-Id": "t2WrBzXQ2MPEcOVhltalPLUNQ1IhXCzzLfvYpjmi",
            "X-Parse-REST-API-Key": "zOUWZArOPKW832ePAJMLaCPBV6kUleAzexCeT04n"
        },
        type: "GET",
        success: function(r) {console.log(r); console.log("suc");},
        error: function(r) {console.log(r); console.log("err");},
        contentType: "applicatoin/json"
    }
    */

    var request = {
        url: "/chart/eee/",
        type: "GET",
        success: function(r) {console.log(r); console.log("suc");},
        error: function(r) {console.log(r); console.log("err");},
        contentType: "applicatoin/json"
    }

    jQuery.ajax(request);

});
