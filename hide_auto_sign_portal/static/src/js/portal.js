odoo.define('hide_auto_sign_portal.portal', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.SignTemplate = publicWidget.Widget.extend({
     selector: '.o_portal_sidebar',
     events: {
        'click a[id="accept_and_sign"]': 'hide_auto_sign',
    },

    hide_auto_sign: function (ev) {
         var self = this;
         this.$autoButton = this.$('a.o_web_sign_auto_button');
         this.$loadButton = this.$('a.o_web_sign_load_button');
         this.$drawButton = this.$('a.o_web_sign_draw_button');

//
         if (this.$autoButton){
            this.$('a.o_web_sign_auto_button').css('display','none');
         }
         if (this.$loadButton){
            this.$('a.o_web_sign_load_button').css('display','none');
         }
         if (this.$drawButton){
            this.$('a.o_web_sign_draw_button').html('Signature');
         }
    },
    });
});
