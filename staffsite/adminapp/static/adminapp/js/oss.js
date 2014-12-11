function convert_unix_timestamp_to_data (unix_timestamp) {
    var date = new Date(unix_timestamp * 1000);
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var seconds = date.getSeconds();
    var years = date.getFullYear();

    // will display time in 10:30:23 format
    var formattedTime = years + " " + hours + ':' + minutes + ':' + seconds;

    return formattedTime;
}
function reset_send_money_dialog() {
    var cur_money_color = $("#send_money_color");

    $("#send_money_name").val('');
    $("#send_money_color").val('');
    $("#send_money_amount").val('');
    $("#send_money_message").val('');
    $("#color_items").children().remove();
    $("#send_money_color_selection").hide();
    $("#send_money_error").hide;
    cur_money_color.attr("class", "btn").removeAttr("data-color_id");
}

function create_send_money_dialog(url, address) {
    $(".send_money_error_msg").hide();
    $("#dialog_send_money").dialog({
        autoOpen: false,
        width: 500,
        modal: true,
        buttons: [
            {
                text: "Send",
                click: function() {
                    // check account is gcoin address or email account
                    var sender_type = "";
                    var data_obj = {};

                    data_obj["address"] = address;
                    data_obj["amount"] = $("#send_money_amount").val();
                    data_obj["color"] = $("#send_money_color").attr("data-color_id");
                    data_obj["message"] = $("#send_money_message").val();


                    // post data to server to use local rpc call to send money
                    url = url + "?addr=" + data_obj["address"] + "&amount=" + data_obj["amount"]
                          + "&color=" + data_obj["color"] + "&msg=" + data_obj["message"];

                    $.ajax({
                        type: "GET",
                        cache: false,
                        async: false,
                        url: url,
                        dataType: "json",
                        success: function(j_data) {
                            alert("success")
                        },
                        error: function() {
                            alert("error send money");
                        }
                    });

                    $(this).dialog( "close" );
                },
                class: "btn btn-default"
            },
            {
                text: "Cancel",
                click: function() {
                    $(this).dialog( "close" );
                },
                class: "btn btn-default"
            }
        ]
    });
}

function create_tx_info_dialog(cur_tx_info_block) {
    $(cur_tx_info_block).dialog({
        autoOpen: false,
        width: 500,
        modal: true,
        buttons: [
            {
                text: "Close",
                click: function() {
                    $( this ).dialog( "close" );
                },
                class: "btn btn-default"
            }
        ]
    });
}

function get_tx_info(tx_id, ret_code) {
    var get_tx_info_url = TX_URL + tx_id;

    $.ajax({
        type: "GET",
        async: false,
        cache: false,
        url: get_tx_info_url,
        dataType: "json",
        success: function(j_data) {
            var tx_info = j_data;
            // 3. create new tx_info_dialog
            var cur_tx_info_dialog = $("#template_tx_info_block").clone(true, true);

            // 4. set tx_info_dialog value
            cur_tx_info_dialog.attr("title", tx_id);

            // check whether is coinbase
            if (tx_info["data"]["is_coinbase"] == false) {
                // input address
                input_addr_count = tx_info["data"]["inputs"].length;
                template_input_addr = cur_tx_info_dialog.find("#template_input_addr");
                for (i = 0; i < input_addr_count; i++) {
                   tmp_addr = template_input_addr.clone(true, true);
                   tmp_addr.html(tx_info["data"]["inputs"][i]["from_address"]);
                   tmp_addr.attr("id", tx_info["data"]["inputs"][i]["from_address"]);
                   tmp_addr.insertBefore(template_input_addr);
                   tmp_addr.show();
                }

                // output address & its output money
                output_addr_count = tx_info["data"]["outputs"].length;
                template_output_addr_money = cur_tx_info_dialog.find("#template_output_addr_money_block");
                for (i = 0; i < output_addr_count; i++) {
                    tmp_addr = template_output_addr_money.clone(true, true);
                    tmp_addr.find("#template_output_addr").html(tx_info["data"]["outputs"][i]["to_address"]);
                    tmp_addr.find("#template_output_addr").attr("id", tx_info["data"]["outputs"][i]["to_address"]);
                    // TODO: color money
//                    tmp_addr.find("#template_output_money").addClass(COLOR_MAPPING[tx_info["data"]["color"]]).html(tx_info["data"]["outputs"][i]["value"]);
                    //tmp_addr.find("#template_output_money").html(tx_info["data"]["outputs"][i]["value"]);
                    tmp_addr.attr("id", tx_info["data"]["outputs"][i]["to_address"]);
                    tmp_addr.insertBefore(template_output_addr_money);
                    tmp_addr.show();
                }
            }
           
            if (tx_info["data"]["is_coinbase"] == false) {
                cur_tx_info_dialog.find("#if_tx_coinbase").hide();
            }

            // confirmed
            if (tx_info["data"]["confirmations"] >= CONFIRMATION_THRESHOLD) {
                cur_tx_info_dialog.find("#if_tx_confirmed").addClass("confirm_tx");
                cur_tx_info_dialog.find("#if_tx_confirmed").html("confirmed")
            }
            else {
                cur_tx_info_dialog.find("#if_tx_confirmed").addClass("unconfirm_tx");
                cur_tx_info_dialog.find("#if_tx_confirmed").html("unconfirmed")
            }
            // total_output_money
   //         cur_tx_info_dialog.find("#total_output_money").addClass(COLOR_MAPPING[tx_info["data"]["color"]]);
  //          cur_tx_info_dialog.find("#total_output_money").html(tx_info["data"]["outputs_value"]);
            // size
            cur_tx_info_dialog.find("#tx_size").html(tx_info["data"]["size"]);
            // receive time
            var time = convert_unix_timestamp_to_data(tx_info["data"]["created_at"]);
            //cur_tx_info_dialog.find("#tx_r_time").html(tx_info["data"]["created_at"]);
            cur_tx_info_dialog.find("#tx_r_time").html(time);
            
            // total input
            cur_tx_info_dialog.find("#tx_input").html(tx_info["data"]["inputs_value"]);
            // total output
            cur_tx_info_dialog.find("#tx_output").html(tx_info["data"]["outputs_value"]);
            // fee
            cur_tx_info_dialog.find("#tx_fee").html(tx_info["data"]["fee"]);

            create_tx_info_dialog(cur_tx_info_dialog);
            $(cur_tx_info_dialog).dialog("open");
            g_tx_found = true;
            return 0;
        },
        error: function(err) {
            var j_error = $.parseJSON(err.responseText);
            g_tx_found = false;

           // $("#srch_tx_warning_msg").html(j_error["error"]["message"]);
           // $("#srch_tx_warning_msg").show();
            console.log("Error: fail to get transaction info");
        }
    });
}

function get_issuer_balance(get_balance_url) {
    $.ajax({
        type: "GET",
        cache: "false",
        url: get_balance_url,
        dataType: "json",
        success: function(j_data) {
            coin_list = j_data["data"];
            gen_send_money_color(coin_list);
        },
        error: function() {
            console.log("Error: fail to get issue balance error");
        }
    });
}

function get_service_list(get_service_url) {
    $.ajax({
        type: "GET",
        cache: "false",
        url: get_service_url,
        dataType: "json",
        success: function(j_data) {
            alert("list service success");
            alert(j_data[0]["fields"]["name"]);
            alert(j_data.length);
            var i = 0;
            var options_dom = "";

            for (i = 0; i < j_data.length; i++) {
                options_dom = "<option value=" + j_data[i]["fields"]["addr"] + ">"
                                + j_data[i]["fields"]["name"] + "</option>";
                $("#send_money_service").append(options_dom);
            }
        },
        error: function() {
            alert("list service fail");
        }
    });
}

function gen_color_money_dom(color, amount) {
    var money_dom = "";
    money_dom = "<button class='btn'>" + color + ":" + amount + "</button>";

    return money_dom;
}

function gen_send_money_color(money) {
    var cur_money_color = $("#send_money_color");
    var money_dom;

    // clean
    $("#send_money_color_selection").children().remove();

    // set
    $.each(money, function(key, money_obj) {
        money_dom = gen_color_money_dom(money_obj["color"], money_obj["amount"]);
        $(money_dom).appendTo("#send_money_color_selection").attr("data-color_id", money_obj["color"]).on("click", function(event) {
            
            cur_money_color.attr("data-color_id", money_obj["color"]).html(money_obj["color"]);
            event.preventDefault();
        });
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
