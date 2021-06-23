odoo.define('digimoov_sessions_modules.website_sale', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var VariantMixin = require('sale.VariantMixin');

publicWidget.registry.WebsiteSaleExamCenterDate = publicWidget.Widget.extend(VariantMixin, {
    selector: '#centre_date_examen',
    events: _.extend({}, VariantMixin.events || {}, {
        'change select[name="centre_examen"]': 'verify_centre',
        'change select[name="date_examen"]': 'verify_date_exam',
        'change input[id="checkbox_conditions"]': 'verify_conditions',
    }),
    verify_date_exam: function (ev) {
        var self = this;
        var center = false;
        var exam_date=document.getElementById('exam_date');
        var center = document.getElementById('centre_examen').value;
        var exam_date_id=false;

        if(exam_date){
            var exam=document.getElementById('exam_date').value;
            if(exam=='all'){
                var error=document.getElementById('error_exam_date');
                if (error && exam_date.style.display=='inline-block') {
                    error.style.display='inline-block';
                }
            } else {
                var error=document.getElementById('error_exam_date');
                if (error) {
                    error.style.display='none';
                }
            }
        }

        if(exam_date){
            var exam_date_id=exam_date.options[exam_date.selectedIndex].id;
            }
        if (center && exam_date) {
            if (center=='all' || exam_date.value=='all'){
                var pm_button=document.getElementById('pm_shop_check');
                var pm_button_checkout=document.getElementById('pm_shop_checkout');
            }
        }
        this._rpc({
            route: "/shop/cart/update_exam_date",
            params: {
                exam_date_id: exam_date_id,
            },
        }).then(function () {
                 return true;
              });
            },

    verify_centre: function (ev) {
        var self = this;
        var center = false;
        var center_exam = document.getElementById('centre_examen');
        if(center_exam){
            var center=document.getElementById('centre_examen').value;
            var id=center_exam.options[center_exam.selectedIndex].id;
        }
        if(center_exam){
            if(center_exam.value != 'all') {
                var t_modules=document.getElementById('exam_date');
                if (t_modules) {
                t_modules.style.display='inline-block' ;
                } else {
                t_modules.style.display='none' ;
            }
            }
        }
        $('#exam_date option').each(function () {
            var self = this;
            var select_option= $(this);
            var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
            var ios=false;
            if (isIOS) {
              ios=true;
            } else {
               ios=false;
            }
            if (self.value == center || self.value=='all') {
                if (ios==true){select_option.prop('disabled', false);select_option.prop('display', 'none');}
                else{
                select_option.show();
                }
            } else {
                  if (ios==true){select_option.prop('disabled', true);select_option.prop('display', 'inline');}
                   else{
                  select_option.hide(); }
            }
        });
        if(center_exam){
            var center=document.getElementById('centre_examen').value;
            if(center=='all'){
                var error=document.getElementById('error_exam_center');
                if (error) {
                    error.style.display='inline-block';
                }
            } else {
                var error=document.getElementById('error_exam_center');
                if (error) {
                    error.style.display='none';
                }
            }
        }

        var exam_date=document.getElementById('exam_date');
        if(exam_date){
            if (exam_date.value != 'all') {
                    exam_date.value='all';
            }
        }
        if(center && exam_date){
        if (center=='all' || exam_date=='all'){
            var pm_button=document.getElementById('pm_shop_check');
            var pm_button_checkout=document.getElementById('pm_shop_checkout');
        } }
        this._rpc({
            route: "/shop/cart/update_exam_center",
            params: {
                center: center,
            },
        }).then(function () {
                 return true;
              });
            },



//    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
//       'change select[name="centre_examen"]': 'verify_centre',
//    }),
//    verify_centre: function (ev) {
////        var self = this;
////        var center = false;
////        center=document.getElementById('centre_examen').value;
//        console.log('Centre examen);
//        console.log(centre);

//    this._rpc({
//    route: "/shop/cart/update_exam_center",
//    params: {
//        center: center,
//    },
//}).then(function () {
//         return true;
//      });
//    },
});
//publicWidget.registry.websiteSaleCart = publicWidget.Widget.extend({
//    selector: '.oe_website_sale .oe_cart',
//    events: {
//        'click .js_delete_product': '_onClickDeleteProduct',
//    },
//
//     _onClickDeleteProduct: function (ev) {
//        ev.preventDefault();
//        console.log('_onClickDeleteProduct digimoov');
//        $(ev.currentTarget).closest('tr').find('.js_quantity').val(0).trigger('change');
//    }
//});
});