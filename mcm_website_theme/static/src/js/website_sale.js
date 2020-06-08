odoo.define('mcm_website_theme.mcm_website_sale', function (require) {
'use strict';

var VariantMixin = require('sale.VariantMixin');
var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var core = require('web.core');
var session = require('web.session');
var rpc = require('web.rpc');
var QWeb = core.qweb;

publicWidget.registry.WebsiteSale.include({
    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
       'click #checkbox_instalment': 'verify_check',
//       'click #pm_shop_check': 'verify_pm',
//       'click #pm_shop_checkout': 'verify_pm',
//       'click #pm_shop': 'verify_pm',

    }),

    verify_check: function (ev) {
    var self = this;
    var instalment = false;
    if (document.getElementById('checkbox_instalment').checked==true) {
                instalment=true
                document.getElementById("order_amount_to_pay").style.visibility = 'visible';
                document.getElementById("order_instalment_number").style.visibility = 'visible';

     } else {
                instalment=false
                document.getElementById("order_amount_to_pay").style.visibility = 'hidden';
                document.getElementById("order_instalment_number").style.visibility = 'hidden';
                }
            console.log('instalment');
            console.log(instalment);

            this._rpc({
            route: "/shop/payment/update_amount",
            params: {
                instalment: instalment,
            },
        }).then(function () {
                 return true;
              });
    },
    verify_pm: function (ev) {
                console.log('verify');
                stripe_pm=document.getElementById('stripe_pm');
                console.log('verify');
                if (stripe_pm){
                    if (stripe_pm.checked==true) {
                    document.getElementById('pm_shop').href='/shop/checkout?express=1';
                    document.getElementById('pm_shop_check').href='/shop/checkout?express=1';
                    document.getElementById('pm_shop_checkout').href='/shop/checkout?express=1';
                } else {
                    document.getElementById('pm_shop').href='/new/ticket';
                    document.getElementById('pm_shop_check').href='/new/ticket';
                    document.getElementById('pm_shop_checkout').href='/new/ticket';


                }
                }

    }

});
});