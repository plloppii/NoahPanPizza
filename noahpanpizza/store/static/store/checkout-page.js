class CheckoutProcess {
    constructor(field_elements) {
        this.steps = [];
        this.current_index = 0;
        this.paypal_info = {};
        field_elements.map(element => {
            let step = {
                id: element.id,
                edit_btn: $(element).find("a"),
                form: $(element).find(".collapse"),
                info: $(element).find("#" + element.id + "-form-info")
            }
            $(step.edit_btn).click(() => {
                $(step.info).text("");
                this.current_index = this.steps.findIndex(stp => stp.id === step.id)
                this.current_step = this.steps[this.current_index];
                this.steps.slice(this.current_index).map(step => {
                    $(step.edit_btn).hide();
                    $(step.info).text("");
                });
            });
            $(step.edit_btn).hide();
            $(step.form).on("submit", (e) => {
                e.preventDefault();
                $.ajax({
                    url: "/store/" + step.id + "-form/",
                    type: "POST",
                    data: serializedToJSON($(step.form).serializeArray()),
                    success: (rtn) => {
                        if (!("error" in rtn)) {
                            $(step.info).text(rtn[step.id + "-text"]);
                            if (step.id === "contact" || step.id === "shipping") {
                                this.paypal_info[step.id] = JSON.parse(rtn[step.id]);
                            }
                            if ("billing" in rtn) {
                                this.paypal_info["billing"] = JSON.parse(rtn["billing"]);
                            }
                            this.continue_to_next();
                        } else {
                            alert(rtn["error"]);
                        }
                    },
                    error: (xhr, errmsg, err) => {
                        alert("Something went wrong! Please try again later!\nError: " + xhr.status);
                    }
                });
            });
            this.steps.push(step);
        });
        this.current_step = this.steps[this.current_index];
        $(this.current_step.form).collapse("toggle");
    }
    continue_to_next() {
        $(this.current_step.edit_btn).show()
        this.current_index++;
        this.current_step = this.steps[this.current_index];
        $(this.current_step.form).collapse("toggle");
        $(this.current_step.edit_btn).hide();
    }
}

var fields = $("#checkout_accordian").find("fieldset").get();
var checkout_process = new CheckoutProcess(fields);
//console.log(checkout_process);

$("#coupon-form").on("submit", (e) => {
    e.preventDefault();
    $.ajax({
        url: "/store/coupon-form/",
        type: "POST",
        data: serializedToJSON($("#coupon-form").serializeArray()),
        success: (rtn) => {
            console.log(rtn);
            if (!("error" in rtn)) {
                $("#coupon-input")[0].value = "";
                $("#coupon-list-name").text(rtn["coupon"]);
                $("#coupon-list-discount").text("-" + rtn["discount"]);
                $("#coupon-list-item").attr('hidden', false);
                $("#cart").load(location.href + " #cart");
            } else {
                alert(rtn["error"]);
            }
        },
        error: (xhr, errmsg, err) => {
            alert("Something went wrong! Please try again later!\nError: " + xhr.status);
        }
    });
})

var subtotal = JSON.parse(document.getElementById('subtotal').textContent);
var order_id = JSON.parse(document.getElementById('order_id').textContent);
// console.log(subtotal);
// console.log(order_id);

$("#loading-spinner").hide();

paypal.Buttons({
    createOrder: function (data, actions) {
        var order = checkout_process.paypal_info;
        console.log(checkout_process.paypal_info);
        console.log(order.contact.first_name);
        var rtn_order = {
            intent: 'CAPTURE',
            payer: {
                name: {
                    given_name: order.contact.first_name,
                    surname: order.contact.last_name
                },
                email_address: order.contact.email_address,
                phone: {
                    phone_type: "MOBILE",
                    phone_number: {
                        national_number: order.contact.phone_number
                    }
                }
            },
            purchase_units: [{
                amount: {
                    value: subtotal,
                    currency_code: 'USD'
                }
            }],
            application_context: {
                shipping_preference: "NO_SHIPPING"
            }
        }
        if (order.billing) {
            let billing_address = checkout_process.paypal_info.shipping;
            rtn_order.payer.address = {
                address_line_1: billing_address.address1,
                address_line_2: billing_address.address2,
                admin_area_2: billing_address.city,
                admin_area_1: billing_address.state,
                postal_code: billing_address.zipcode,
                country_code: billing_address.country
            };
        }
        console.log(rtn_order);

        return actions.order.create(rtn_order);
    },
    //Approved, show review dropdown.
    onApprove: (data, actions) => {
        // This function captures the funds from the transaction.
        checkout_process.continue_to_next();
        return actions.order.get()
            .then(function (details) {
                console.log(details);
                document.querySelector('#place-order').addEventListener('click', function () {
                    $("#loading-spinner").toggle();
                    return actions.order.capture().then(function () {
                        //Send order information to page to update order with payment information. 
                        console.log("/store/checkout-success/order/" + order_id)
                        $.ajax({
                            url: "/store/checkout-success/order/" + order_id,
                            type: "POST",
                            data: { value: JSON.stringify(details) },
                            success: (rtn) => {
                                if (!("error" in rtn)) {
                                    //alert('Transaction completed by ' + details.payer.name.given_name);
                                    window.location = "/store/checkout-success/order/" + order_id;
                                } else {
                                    alert("Unable to store order information: " + rtn["error"]);
                                }
                            },
                            error: (xhr, errmsg, err) => {
                                alert("Something went wrong! Please try again later!\nError: " + xhr.status);
                            }
                        });
                    })
                })
            });
    },
    onError: function (err) {
        console.log("And error has occured.");
        alert("An Error has occured! Please review your shipping info");
        console.log(error);
    },
    style: {
        shape: "pill",
        color: "blue",
        label: "pay"
    }
}).render('#paypal-button-container');
// This function displays Smart Payment Buttons on your web page.


function serializedToJSON(arr) {
    var rtn = {};
    arr.forEach(obj => rtn[obj.name] = obj.value)
    return rtn;
}

// Cookie/ Ajax setup.
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
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});