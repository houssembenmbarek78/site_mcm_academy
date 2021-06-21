odoo.define('sh_corpomate_theme.editor.link', function (require) {
'use strict';

var weWidgets = require('wysiwyg.widgets');
var wUtils = require('website.utils');


weWidgets.LinkDialog.include({

	xmlDependencies: (weWidgets.LinkDialog.prototype.xmlDependencies || []).concat(
        ['/sh_corpomate_theme/static/src/xml/website.editor.xml']
    ),

    
    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        
        var allBtnClassSuffixes = /(^|\s+)btn(-[a-z0-9_-]*)?/gi;
        //var allBtnShapes = /\s*(rounded-circle|flat)\s*/gi;
        
        var allBtnShapes = /\s*(rounded-circle|flat|sh_btn_cm_1|sh_btn_cm_2|sh_btn_cm_3|sh_btn_cm_4|sh_btn_cm_5|sh_btn_cm_6|sh_btn_cm_7|sh_btn_cm_8)\s*/gi;        
        this.data.className = this.data.iniClassName
            .replace(allBtnClassSuffixes, ' ')
            .replace(allBtnShapes, ' ');        
        
    },    
    
    
});

});
