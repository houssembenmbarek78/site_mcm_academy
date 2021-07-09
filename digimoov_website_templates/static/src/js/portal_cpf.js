odoo.define('digimoov_website_templates.portal_cpf', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.RequestRenouncee = publicWidget.Widget.extend({
    selector: '.o_portal_my_home',
    events: {
        'change #renonce_request_box': 'check_renounce', // vérifier s'il y a eu un changement de valeur au niveau de checkbox du demande de renonce dans le portal client

    },
    check_renounce: function () {
        var self = this;
        var demande_renonce = false;
        var renonce = document.getElementById('renonce_request_box') // on recupère la demande de renonce en portal à partir id
        if (renonce) { // on teste si on a trouvé le checkbox de la demande de renonce dans le portal client
            if (renonce.checked==true) { // on vérifie si le client a cocher la demande de renonce
                demande_renonce = true; // on change le variable demande renonce à vrai pour l'envoyer via url en python pour mettre à jour la fiche de client
            }
        }
        this._rpc({
            route: "/update_renonce", // on prepare un url de mise à jour de la demande de renonce par la suite on va la developpé en python dans controller
            params: {
                demande_renonce: demande_renonce, // on envoi la valeur du demande du renonce comme paramètre avec l'url
            },
        }).then(function () {
                 return window.location.reload(); // dés que l'url termine l'éxécution on recharge la page de portal client
              });
            },
});
});