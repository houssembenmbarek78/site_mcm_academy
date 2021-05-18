odoo.define('hide_auto_sign_portal.qweb_template', [ 'web.ajax' ], function (require) {
'use strict';
var ajax = require('web.ajax');
var core = require('web.core');
var qweb = core.qweb;

ajax.loadXML('/hide_auto_sign_portal/static/src/js/qweb_template.js', qweb);