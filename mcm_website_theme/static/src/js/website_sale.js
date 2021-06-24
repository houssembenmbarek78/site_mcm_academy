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
       'click #checkbox_conditions': 'verify_conditions',
       'click #checkbox_failures': 'verify_failures',
       'click #checkbox_accompagnement': 'verify_accompagnement',
       'click #cpf_pm': 'verify_cpf',
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

    this._rpc({
    route: "/shop/payment/update_amount",
    params: {
        instalment: instalment,
    },
}).then(function () {
         return true;
      });
    },
    verify_cpf: function(ev){
        var self = this;
        var cpf = false;
        if(document.getElementById('cpf_pm')){
            if (document.getElementById('cpf_pm').checked==true) {
            cpf=true;
            } else {
             cpf=false
             }
         }

         this._rpc({
            route: "/shop/payment/update_cpf",
            params: {
                cpf: cpf,
            },
        }).then(function () {
                 return true;
              });
    },
    verify_pm: function (ev) {
                stripe_pm=document.getElementById('stripe_pm');
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

    },
    verify_conditions : function(ev) {
        var self = this;
        var condition = false;
        var conditions=document.getElementById('checkbox_conditions')
        if (document.getElementById('checkbox_conditions')) {
            if (document.getElementById('checkbox_conditions').checked==true) {
                var error=document.getElementById('error_conditions');
                if (error) {
                    error.style.display='none';
                }
                condition=true;
            } else {
                var error=document.getElementById('error_conditions');
                if (error) {
                    error.style.display='inline-block';
                }
                condition=false;
            }
        }
        this._rpc({
            route: "/shop/payment/update_condition",
            params: {
                condition: condition,
         },
        }).then(function () {
            return true;
        });
    },
    verify_failures : function(ev) {
        var self = this;
        var failures = false;
        if (document.getElementById('checkbox_failures')) {
            if (document.getElementById('checkbox_failures').checked==true) {
                failures=true;
            } else {
                failures=false;
            }
        }
        this._rpc({
            route: "/shop/payment/update_failures",
            params: {
                failures: failures,
         },
        }).then(function () {
            return true;
        });
    },
    verify_accompagnement : function(ev) {
        var self = this;
        var accompagnement = false;
        if (document.getElementById('checkbox_accompagnement')) {
            if (document.getElementById('checkbox_accompagnement').checked==true) {
                accompagnement=true;
            } else {
                accompagnement=false;
            }
        }
        this._rpc({
            route: "/shop/payment/update_accompagnement",
            params: {
                accompagnement: accompagnement,
         },
        }).then(function () {
            return true;
        });
    },


});
});