odoo.define('portal.portal', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.portalDetails = publicWidget.Widget.extend({
     events: _.extend({}, publicWidget.registry.portalDetails.events, {
       'change #identity': 'onCheckDocuments',
       'change #permis': 'onCheckDocuments',
    }),

    /**
     * @private
     */
         onCheckDocuments: function (ev) {
        var $identity = $("input[id='identity']");
                        var $permis = $("input[id='permis']");
                        if ((parseInt($identity.get(0).files.length)>2) || (parseInt($permis.get(0).files.length)>2)){
                        if (parseInt($identity.get(0).files.length)>2){
                        alert("Vous ne pouvez télécharger qu'un maximum de 2 fichiers ( Recto , Verso ) à votre pièce
                        d'identité");
                        button=document.getElementById('submit_documents');
                        document.getElementById('identity').value=null;
                        button.disabled=true;
                        }
                        if (parseInt($permis.get(0).files.length)>2){
                        alert("Vous ne pouvez télécharger qu'un maximum de 2 fichiers ( Recto , Verso ) à votre permis
                        de conduire");
                        button=document.getElementById('submit_documents');
                        document.getElementById('permis').value=null;
                        button.disabled=true;
                        }
                        }
                        else {
                        button=document.getElementById('submit_documents');
                        button.disabled=false;
                        }
    },
    _onCountryChange: function () {
        this._adaptAddressForm();
    },
});