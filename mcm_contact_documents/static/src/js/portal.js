doo.define('mcm_contact_documents.portal', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.ExamCenterDate = publicWidget.Widget.extend({
    selector: '#digimoov_my_documents_form',
    events: {
        'click #check_domicile_not_checked': 'check_domicile',
        'click #check_domicile_checked': 'check_domicile',
    },

        check_domicile: function (ev) {
        console.log('verify date exam');
        var self = this;
        var domic_checked= document.getElementById('check_domicile_checked');
        var domic_not_checked= document.getElementById('check_domicile_not_checked');
        var domic_identity_hebergeur=
        document.getElementById('o_website_form_identity_hebergeur');
        var domic_attestation_hebergeur=
        document.getElementById('o_website_form_attestation_hebergeur');
        var identity_hebergeur = document.getElementById('identity_hebergeur');
        var attestation_hebergeur = document.getElementById('attestation_hebergeur');
        if(domic_checked.checked){
        if(domic_identity_hebergeur) {
        domic_identity_hebergeur.style.display='none';
        domic_identity_hebergeur.className='form-group row form-field';
        identity_hebergeur.required = 0;
        }
        if(domic_attestation_hebergeur) {
        domic_attestation_hebergeur.style.display='none';
        domic_attestation_hebergeur.className='form-group row form-field';
        attestation_hebergeur.required = 0;
        }
        }
        if(domic_not_checked.checked){
        if(domic_identity_hebergeur) {
        domic_identity_hebergeur.style.display='block';
        domic_identity_hebergeur.className='form-group row form-field
        o_website_form_required';
        identity_hebergeur.required = 1;
        }
        if(domic_attestation_hebergeur) {
        domic_attestation_hebergeur.style.display='block';
        domic_attestation_hebergeur.className='form-group row form-field
        o_website_form_required';
        attestation_hebergeur.required = 1;
        }
        }
            },

})
});