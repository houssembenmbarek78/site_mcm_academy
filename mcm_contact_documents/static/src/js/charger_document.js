odoo.define('mcm_contact_documents.charger_document', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.digimoov_documents = publicWidget.Widget.extend({
    selector: '#digimoov_my_documents_form',
    events: {
        'click #domicile_personnel_oui': 'domicile_personnel',
        'click #domicile_personnel_non': 'domicile_personnel',
    },

        domicile_personnel: function (ev) {
        var self = this;
        var domicile_personnel_oui = document.getElementById('domicile_personnel_oui');
        var domicile_personnel_non = document.getElementById('domicile_personnel_non');
        var identite_hebergeur = document.getElementById('identite_hebergeur_form');
        var attestation_hebergement = document.getElementById('attestation_hebergement_form');
        var justificatif_domicile = document.getElementById('justificatif_domicile_form');

        if(domicile_personnel_oui.checked){
            if(identite_hebergeur) {
                identite_hebergeur.style.display='none';
                identite_hebergeur.className='form-group row form-field';
                identite_hebergeur.required = 0;
            }
            if(attestation_hebergement) {
                attestation_hebergement.style.display='none';
                attestation_hebergement.className='form-group row form-field';
                attestation_hebergement.required = 0;
            }
            if(justificatif_domicile) {
                justificatif_domicile.style.display='block';
                justificatif_domicile.className='form-group row form-field o_website_form_required';
                justificatif_domicile.required = 1;
            }
        }
        if(domicile_personnel_non.checked){
            if(identite_hebergeur) {
                identite_hebergeur.style.display='block';
                identite_hebergeur.className='form-group row form-field o_website_form_required';
                identite_hebergeur.required = 1;
            }
            if(attestation_hebergement) {
                attestation_hebergement.style.display='block';
                attestation_hebergement.className='form-group row form-field o_website_form_required';
                attestation_hebergement.required = 1;
            }
            if(justificatif_domicile) {
                justificatif_domicile.style.display='none';
                justificatif_domicile.className='form-group row form-field';
                justificatif_domicile.required = 0;
            }
        }
            },

})

});