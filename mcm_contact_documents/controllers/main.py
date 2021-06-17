import logging
import werkzeug
import odoo.http as http
import base64
import werkzeug
import requests
from PIL import Image
import PIL
import os
import glob
from odoo.http import request
from odoo import _
from addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError
from bs4 import BeautifulSoup as BSHTML
import urllib3
from werkzeug import FileStorage as storage
import PIL
from PIL import Image
import os
import glob


logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        document_count = request.env['documents.document'].sudo().search_count(
            [('owner_id', '=', user.id)])
        values['document_count'] = document_count
        return values

    # def _document_check_access(self, document_id):
    #     document = request.env['documents.document'].browse([document_id])
    #     document_sudo = document.sudo()
    #     try:
    #         document.check_access_rights('read')
    #         document.check_access_rule('read')
    #     except AccessError:
    #         raise
    #     return document_sudo

    @http.route(
        ['/my/documents', '/my/documents/page/<int:page>'],
        type='http',
        auth="user",
        website=True,
    )
    def portal_my_tickets(
            self,
            page=1,
            date_begin=None,
            date_end=None,
            sortby=None,
            filterby=None,
            **kw):
        values = self._prepare_portal_layout_values()
        Document = request.env['documents.document']
        user = request.env.user
        website = request.website
        domain = [('owner_id', '=', user.id)]

        searchbar_sortings = {
            'date': {'label': _('Nouveau'), 'order': 'create_date desc'},
            'name': {'label': _('Nom'), 'order': 'name'},
            'stage': {'label': _('État'), 'order': 'state'},
        }
        searchbar_filters = {
            'all': {'label': _('Tous'), 'domain': []},
            'refused': {'label': _('Refuser'), 'domain': [("state", "=", "refused")]},
            'waiting': {'label': _('En Attente de validation'), 'domain': [("state", "=", "waiting")]},
            'validated': {'label': _('Valider'), 'domain': [("state", "=", "validated")]},
        }

        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        document_count = Document.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/documents",
            url_args={},
            total=document_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        documents = Document.sudo().search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        values.update({
            'date': date_begin,
            'documents': documents,
            'page_name': 'document',
            'website' : website,
            'pager': pager,
            'default_url': '/my/documents',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
        })
        return request.render("mcm_contact_documents.portal_my_documents", values)
#upload documents MCM-Academy
    @http.route(['/submitted/document'], type="http", auth="user", methods=['POST'], website=True, csrf=False)
    def submit_documents(self, **kw):
        partner_id = http.request.env.user.partner_id
        print('partner')
        print(partner_id.name)
        folder_id = request.env['documents.folder'].sudo().search([('name', "=", _('Documents Clients')),('company_id',"=",1)])
        if not folder_id:
            vals_list = []
            vals = {
                'name': "Documents Clients"
            }
            vals_list.append(vals)
            folder_id = request.env['documents.folder'].sudo().create(vals_list)
            vals_list = []
            vals = {
                'name': "Statut document",
                'folder_id': folder_id.id,
                'company_id':1,
            }
            vals_list.append(vals)
            facet = request.env['documents.facet'].sudo().create(vals_list)
        files_identity = request.httprequest.files.getlist('identity[]')
        files_permis = request.httprequest.files.getlist('permis[]')
        files_domicile = request.httprequest.files.getlist('domicile[]')
        check = False
        error_identity = ''
        error_identity_number = ''
        error_permis = ''
        error_permis_number = ''
        error_domicile = ''
        if (len(files_identity) == 0):
            check = True
            error_identity = 'error'
        if (len(files_permis) == 0):
            check = True
            error_permis = 'error'
        if not (kw.get('number')):
            check = True
            error_identity_number = 'error'
        if (len(files_domicile) == 0):
            check = True
            error_domicile = 'error'
        if not (kw.get('number_permis')):
            check = True
            error_permis_number = 'error'
        if check == True:
            return request.render("mcm_contact_documents.mcm_contact_documents_new_documents",
                                  {'partner_id': partner_id, 'error_identity': error_identity,
                                   'error_permis': error_permis, 'error_identity_number': error_identity_number,
                                   'error_permis_number': error_permis_number, 'error_domicile': error_domicile})
        if (len(files_identity) > 2 or len(files_permis) > 2):
            name = http.request.env.user.name
            email = http.request.env.user.email
            return request.redirect('/new_documents')
        if not files_identity:
            return request.redirect('/new_documents')
        try:
            try:
                files = request.httprequest.files.getlist('identity[]')
                if len(files) == 2:
                    datas_idendity_name = base64.encodebytes(files[0].read())
                    datas_identity_email = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité Recto " + str(partner_id.name),
                        'datas': datas_idendity_name,
                        'folder_id': int(folder_id),
                        'code_document': 'identity_1',
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        ['|', '&', ('code_document', "=", 'identity_1'), ('owner_id', "=", http.request.env.user.id),
                         ('code_document', "=", 'identity')
                         ], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité Verso " + str(partner_id.name),
                        'datas': datas_identity_email,
                        'code_document': 'identity_2',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'identity_2'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                elif len(files) == 1:
                    datas_piece_identite_verso = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité " + str(partner_id.name),
                        'datas': datas_piece_identite_verso,
                        'code_document': 'identity',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'identity'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        #parser les deux piece recto verso dans le mm model
                        document = document.sudo().write(vals)
                    else:
                        print('document not found')
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")

            try:
                files = request.httprequest.files.getlist('permis[]')
                if len(files) == 2:
                    datas_permis_recto = base64.encodebytes(files[0].read())
                    datas_permis_verso = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire Recto " + str(partner_id.name),
                        'datas': datas_permis_recto,
                        'folder_id': int(folder_id),
                        'code_document': 'permis_1',
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number_permis'),
                        'confirmation': kw.get('confirmation_permis'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        ['|', '&', ('code_document', "=", 'permis_1'), ('owner_id', '=', http.request.env.user.id),
                         ('code_document', "=", 'permis')
                         ], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire Verso " + str(partner_id.name),
                        'datas': datas_permis_verso,
                        'code_document': 'permis_2',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number_permis'),
                        'confirmation': kw.get('confirmation_permis'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'permis_2'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                elif len(files) == 1:
                    datas_permis = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire " + str(partner_id.name),
                        'datas': datas_permis,
                        'code_document': 'permis',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number_permis'),
                        'confirmation': kw.get('confirmation_permis'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'permis'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        print('permis found')
                        document = document.sudo().write(vals)
                    else:
                        print('permis not found')
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")

            try:
                files = request.httprequest.files.getlist('domicile[]')
                if files:
                    datas_justificatif_domicile = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Justificatif de domicile " + str(partner_id.name),
                        'datas': datas_justificatif_domicile,
                        'code_document': 'domicile',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'domicile'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")
                return http.request.render('mcm_contact_documents.success_documents')

            try:
                files = request.httprequest.files.getlist('changed_file[]')
                if files:
                    datas_changed_file = base64.encodebytes(files[0].read())
                    vals_list = []
                    name = 'Document '
                    if partner_id.module_id:
                        if partner_id.module_id.product_id.name in (
                                'Formation intensive VTC', 'Formation intensive TAXI', 'Formation intensive VMDTR'):
                            name = 'Reçu de paiement de l’examen CMA '
                        elif partner_id.module_id.product_id.name in (
                                'Formation continue TAXI', 'Formation continue VTC', 'Formation continue VMDTR'):
                            name = 'Carte Taxi ou VTC ou VMDTR '
                        elif partner_id.module_id.product_id.name in ('Formation mobilité TAXI'):
                            name = 'Carte Taxi '
                        elif partner_id.module_id.product_id.name in (
                                'Formation à distance TAXI', 'Formation à distance VTC', 'Formation à distance VMDTR'):
                            name = 'Examen Chambre des métiers '
                        elif partner_id.module_id.product_id.name in (
                                'Formation à distance passerelle VTC', 'Formation à distance passerelle Taxi'):
                            name = 'Obtention Examen ou Carte Taxi / VTC '
                    vals = {
                        'name': name + str(partner_id.name),
                        'datas': datas_changed_file,
                        'code_document': 'carte_exam',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'carte_exam'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")
                return http.request.render('mcm_contact_documents.success_documents')

            try:
                files = request.httprequest.files.getlist('attestation[]')
                if files:
                    datas_attestation = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Attestation d'hébergement " + str(partner_id.name),
                        'datas': datas_attestation,
                        'code_document': 'hebergement',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'hebergement'), ('owner_id', '=', http.request.env.user.id)], limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")
                return http.request.render('mcm_contact_documents.success_documents')

            try:
                files = request.httprequest.files.getlist('hebergeur_identity[]')
                if len(files) == 2:
                    datas_hebergeur_identity_recto = base64.encodebytes(files[0].read())
                    datas_hebergeur_identity_verso = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Carte d'identité hebergeur Recto " + str(partner_id.name),
                        'datas': datas_hebergeur_identity_recto,
                        'folder_id': int(folder_id),
                        'code_document': 'hebergeur_identity_1',
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('identity_hebergeur_card_number'),
                        'confirmation': kw.get('confirmation_hebergeur'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        ['|', '&', ('code_document', "=", 'hebergeur_identity_1'),
                         ('owner_id', '=', http.request.env.user.id),
                         ('code_document', "=", 'hebergeur_identity')], limit=1)
                    if document:
                        print('document1')
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                    vals_list = []
                    vals = {
                        'name': "Carte d'identité hebergeur Verso " + str(partner_id.name),
                        'datas': datas_hebergeur_identity_verso,
                        'code_document': 'hebergeur_identity_2',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('identity_hebergeur_card_number'),
                        'confirmation': kw.get('confirmation_hebergeur'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'hebergeur_identity_2'), ('owner_id', '=', http.request.env.user.id)],
                        limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                elif len(files) == 1:
                    datas_hebergeur_identity_verso = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Carte d'identité hebergeur " + str(partner_id.name),
                        'datas': datas_hebergeur_identity_verso,
                        'code_document': 'hebergeur_identity',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('identity_hebergeur_card_number'),
                        'confirmation': kw.get('confirmation_hebergeur'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code_document', "=", 'hebergeur_identity'), ('owner_id', '=', http.request.env.user.id)],
                        limit=1)
                    if document:
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")
            vals = {
                'partner_email': False,
                'partner_id': False,
                'description': '%s a envoyé ses documents ' % (partner_id.name),
                'name': 'News : Documents reçu',
                'team_id': request.env['helpdesk.team'].sudo().search([('name', 'like', _('Documents'))],
                                                                      limit=1).id,

            }
            new_ticket = request.env['helpdesk.ticket'].sudo().create(
                vals)
        except:
            logger.exception("Fail to upload documents")
        return http.request.render('mcm_contact_documents.success_documents')
# Upload documents digimoov
    @http.route('/upload_my_files', type="http", auth="user", methods=['POST'], website=True, csrf=False)
    def upload_my_files(self, **kw):
        print('upload_my_files')
        print(http.request.env.user.name)
        # charger le dossier des documents clients appartenant a Digimoov
        folder_id = request.env['documents.folder'].sudo().search([('name', "=", _('Documents Digimoov')),('company_id',"=",2)])
        if not folder_id:
            vals_list =[]
            #charger les documents appartenant seulement a digimoov
            vals = {
                'name': "Documents Digimoov",
                'company_id':2
            }
            vals_list.append(vals)
            folder_id = request.env['documents.folder'].sudo().create(vals_list)
            vals_list = []
            vals = {
                'name': "Statut document",
                'folder_id': folder_id.id,
            }
            vals_list.append(vals)
            facet = request.env['documents.facet'].sudo().create(vals_list)
            # Ce code  a été modifiée par Seif le 10/03/2021  (!datas!)
        try:
            # Preparation de l'environemnt de travail celons le profile et preparation de chargement des fichiers
            files = request.httprequest.files.getlist('identity')
            files2 = request.httprequest.files.getlist('identity2')
            document=False
            if files:
                vals_list = []
                #charge le modele de la carte d'identité [un seul modele pour deux attachements]
                # on a pris les precaution au cas ou un client télécharge le recto et le verso avec le meme upload file
                #on a supprimer datas=False
                vals = {
                    'name': "Carte d'identité Recto",
                    'folder_id': int(folder_id),
                    'code_document': 'identity',
                    'confirmation': kw.get('confirm_identity'),
                    'attachment_number': kw.get('identity_number'),
                    'type': 'binary',
                    'partner_id': False,
                    'owner_id': False}
                vals_list.append(vals)
                document = request.env['documents.document'].sudo().create(vals_list)
                if document:
                    uid = document.create_uid
                    document.sudo().write(
                        {'owner_id': uid, 'partner_id': uid.partner_id, 'name': document.name + ' ' + str(uid.name)})
                if len(files) == 2:
                    datas_Carte_didentité_Recto = base64.encodebytes(files[0].read())
                    datas_Carte_didentité_Verso = base64.encodebytes(files[1].read())
                    #Attachement Carte d'identité Recto
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité recto",
                        'type': 'binary',
                        'datas': datas_Carte_didentité_Recto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    # Attachement Carte d'identité Verso
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité Verso",
                        'type': 'binary',
                        'datas': datas_Carte_didentité_Verso,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    #Attachement Carte d'identité recto
                elif len(files) == 1:
                    datas_carte_didentiterecto = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité recto",
                        'type': 'binary',
                        'datas': datas_carte_didentiterecto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
            if files2 and document:
                datas_carte_didentite = base64.encodebytes(files2[0].read())
                request.env['ir.attachment'].sudo().create({
                    'name': "Carte d'identité Verso",
                    'type': 'binary',
                    'datas': datas_carte_didentite,
                    'res_model': 'documents.document',
                    'res_id': document.id
                })
            document.sudo().write({'name':"Carte d'identité Recto/Verso"})
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")

        # try:
        #     files2 = request.httprequest.files.getlist('identity2')
        #     if files2:
        #         vals_list = []
        #         vals = {
        #             'name': "Carte d'identité verso",
        #             'folder_id': int(folder_id),
        #             'code_document': 'identity2',
        #             'confirmation': kw.get('confirm_identity'),
        #             'attachment_number': kw.get('identity_number'),
        #             'type': 'binary',
        #             'partner_id': False,
        #             'owner_id': False}
        #         vals_list.append(vals)
        #         document = request.env['documents.document'].sudo().create(vals_list)
        #         if document:
        #             uid = document.create_uid
        #             document.sudo().write(
        #                 {'owner_id': uid, 'partner_id': uid.partner_id, 'name': document.name + ' ' + str(uid.name)})
        #             #dans cette partie on a pris on compte si un client télécharge deux fichier par l'upload file
        #             # cette option est désactiver dans la vue xml par le champs multiple
        #         if len(files2) == 2:
        #             datas_cartedidenditeerecto = base64.encodebytes(files2[0].read())
        #             datas_cartedidenditeeverso = base64.encodebytes(files2[1].read())
        #             request.env['ir.attachment'].sudo().create({
        #                 'name': "Carte d'identité Recto",
        #                 'type': 'binary',
        #                 'datas': datas_cartedidenditeerecto,
        #                 'res_model': 'documents.document',
        #                 'res_id': document.id
        #             })
        #             # creation de l'attachement carte d'identité verso
        #             request.env['ir.attachment'].sudo().create({
        #                 'name': "Carte d'identité verso",
        #                 'type': 'binary',
        #                 'datas': datas_cartedidenditeeverso,
        #                 'res_model': 'documents.document',
        #                 'res_id': document.id
        #             })
        #         elif len(files2) == 1:
        #             # cest notre cas puisqu'on a un seul attachement on parse la carte d identité verso
        #             datas_cartedidenditeverso = base64.encodebytes(files2[0].read())
        #             request.env['ir.attachment'].sudo().create({
        #                 'name': "Carte d'identité Verso",
        #                 'type': 'binary',
        #                 'datas': datas_cartedidenditeverso,
        #                 'res_model': 'documents.document',
        #                 'res_id': document.id
        #             })
        # except Exception as e:
        #     logger.exception("Fail to upload document Carte d'identité ")
        try:
            files = request.httprequest.files.getlist('address_proof')
            if files:
                vals_list = []
                #Attacher la justificatif de domicile
                vals = {
                    'name': "Jusitificatif de domicile",
                    'folder_id': int(folder_id),
                    'code_document': 'proof',
                    'type': 'binary',
                    'partner_id': False,
                    'owner_id': False
                }
                vals_list.append(vals)
                #Préparation du doc
                document = request.env['documents.document'].sudo().create(vals_list)
                if document:
                    #attacher le document à son créateur
                    uid = document.create_uid
                    document.sudo().write(
                        {'owner_id': uid, 'partner_id': uid.partner_id, 'name': document.name + ' ' + str(uid.name)})
                if len(files) == 2:
                    #lire les docs on cas ou le document contient deux attachement
                    datas_justificatifrecto = base64.encodebytes(files[0].read())
                    datas_justificatifverso = base64.encodebytes(files[1].read())
                    #creation du document justification du domicile en cas il est compose d un recto verso
                    request.env['ir.attachment'].sudo().create({
                        'name': "Jusitificatif de domicile Recto",
                        'type': 'binary',
                        'datas': datas_justificatifrecto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Jusitificatif de domicile Verso",
                        'type': 'binary',
                        'datas': datas_justificatifverso,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    # creation du document justification du domicile en cas il est compose d'un seul document
                elif len(files) == 1:
                    datas_justificatif = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Jusitificatif de domicile",
                        'type': 'binary',
                        'datas': datas_justificatif,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        try:
            #préparation de l'espace de document pour identity hebergeur
            hfiles = request.httprequest.files.getlist('identity_hebergeur')
            hfiles1 = request.httprequest.files.getlist('identity_hebergeur1')
            document = False
            #Regroupement des 2 fichers
            if hfiles:
                vals_list = []
                #charger le document identitée hebergeur
                #on a supprimer datas
                vals = {
                    'name': "Carte d'identité hébergeur",
                    'folder_id': int(folder_id),
                    'code_document': 'identity_hebergeur',
                    'type': 'binary',
                    'partner_id': False,
                    'owner_id': False
                }
                #ajouter les les valeurs à la liste vals_list
                vals_list.append(vals)
                document = request.env['documents.document'].sudo().create(vals_list)
                if document:
                    uid = document.create_uid
                    #concatiner le nom du document avec son createur
                    document.sudo().write(
                        {'owner_id': uid, 'partner_id': uid.partner_id, 'name': document.name + ' ' + str(uid.name)})
                    #on cas ou le document est composé de deux attachements on va lire ces deux  attachements
                if len(hfiles) == 2:
                    datas_carteidentite_hybergeur_recto = base64.encodebytes(hfiles[0].read())
                    datas_carteidentite_hybergeur_verso = base64.encodebytes(hfiles[1].read())
                    #parser la carte déidentité hebergeur recto
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité hébergeur recto",
                        'type': 'binary',
                        'datas': datas_carteidentite_hybergeur_recto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    # parser la carte d'identité hebergeur verso
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité hébergeur verso",
                        'type': 'binary',
                        'datas': datas_carteidentite_hybergeur_verso,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    #notre cas ou on attache un seul fichier carte d'identité hebergeur
                elif len(hfiles) == 1:
                    datas_identite_hybergeur = base64.encodebytes(hfiles[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité hébergeur",
                        'type': 'binary',
                        'datas': datas_identite_hybergeur,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
            if hfiles1:
                datas_identite_hybergeur = base64.encodebytes(hfiles1[0].read())
                request.env['ir.attachment'].sudo().create({
                    'name': "Carte d'identité hébergeur",
                    'type': 'binary',
                    'datas': datas_identite_hybergeur,
                    'res_model': 'documents.document',
                    'res_id': document.id
                })
            document.sudo().write({'name':"Carte d'identité hebergeur Recto/Verso"})
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")

        try:
            #charger les documents mis (attestation hebergeur)
            files = request.httprequest.files.getlist('attestation_hebergeur')
            if files:
                vals_list = []
                #charger son nom et son dossier
                #supprimer datas
                vals = {
                    'name': "Attestation d'hébergement",
                    'folder_id': int(folder_id),
                    'code_document': 'attestation_hebergeur',
                    'type': 'binary',
                    'partner_id': False,
                    'owner_id': False
                }
                vals_list.append(vals)
                document = request.env['documents.document'].sudo().create(vals_list)
                if document:
                    uid = document.create_uid
                    document.sudo().write(
                        {'owner_id': uid, 'partner_id': uid.partner_id, 'name': document.name + ' ' + str(uid.name)})
                if len(files) == 2:
                    datas_attestation_hebergeurrecto = base64.encodebytes(files[0].read())
                    datas_attestation_hebergeurverso = base64.encodebytes(files[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Attestation d'hébergement",
                        'type': 'binary',
                        'datas': datas_attestation_hebergeurrecto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Attestation d'hébergement",
                        'type': 'binary',
                        'datas': datas_attestation_hebergeurverso,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    #charger le document attestation d'hebergement
                elif len(files) == 1:
                    datas_attestation_hebergeur = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Attestation d'hébergement",
                        'type': 'binary',
                        'datas': datas_attestation_hebergeur,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    #charger une exception en cas  derreur de chargement des docs
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        try:
            # charger les docs cerfa dans files
            files = request.httprequest.files.getlist('cerfa')
            files_cerfa_page_2 = request.httprequest.files.getlist('cerfa2')
            files_cerfa_page_3 = request.httprequest.files.getlist('cerfa3')
            document = False
            if files:
                vals_list = []
                #parser le doc cerfa avec les cordonnee associée
                #supprime datas=false
                vals = {
                    'name': "CERFA 11414-05",
                    'folder_id': int(folder_id),
                    'code_document': 'cerfa',
                    'confirmation' : kw.get('confirm_cerfa'),
                    'type': 'binary',
                    'partner_id': False,
                    'owner_id': False
                }
                vals_list.append(vals)
                document = request.env['documents.document'].sudo().create(vals_list)
                if document:
                    uid = document.create_uid
                    # concatiner le nom du doc avec le nom du propriétaire
                    document.sudo().write(
                        {'owner_id': uid, 'partner_id': uid.partner_id, 'name': document.name + ' ' + str(uid.name)})
                    #on cas d'attacher deux attachements aux doc Cerfa
                page_number=1
                #Loop & create cerfa attachments
                for ufile in files:
                    datas_cerfa= base64.encodebytes(ufile.read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Cerfa Page "+ str(page_number),
                        'type': 'binary',
                        'datas': datas_cerfa,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    page_number+=1
            if files_cerfa_page_2:
                datas_cerfa = base64.encodebytes(files_cerfa_page_2[0].read())
                request.env['ir.attachment'].sudo().create({
                    'name': "Cerfa Page 2",
                    'type': 'binary',
                    'datas': datas_cerfa,
                    'res_model': 'documents.document',
                    'res_id': document.id
                })
            if files_cerfa_page_3:
                datas_cerfa = base64.encodebytes(files_cerfa_page_3[0].read())
                request.env['ir.attachment'].sudo().create({
                    'name': "Cerfa Page 3",
                    'type': 'binary',
                    'datas': datas_cerfa,
                    'res_model': 'documents.document',
                    'res_id': document.id
                })
            document.sudo().write({'name':"CERFA 11414-05"})
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        return http.request.render('mcm_contact_documents.success_documents')

    @http.route('/new_documents', type="http", auth="user", website=True)
    def create_documents(self, **kw):
        name = http.request.env.user.name
        email = http.request.env.user.email
        partner_id = http.request.env.user.partner_id
        print(partner_id.module_id.name)
        return http.request.render('mcm_contact_documents.mcm_contact_documents_new_documents', {
            'email': email, 'name': name, 'partner_id':partner_id ,'error_identity':'','error_permis':'','error_identity_number':'','error_permis_number':'','error_domicile':'' })

    @http.route('/charger_mes_documents', type="http", auth="user", website=True)
    def create_documents_digimoov(self, **kw):
        name = http.request.env.user.name
        email = http.request.env.user.email
        partner_id = http.request.env.user.partner_id
        return http.request.render('mcm_contact_documents.mcm_contact_document_charger_mes_documents', {
            'email': email, 'name': name, 'partner_id': partner_id, 'error_identity': '', 'error_permis': '',
            'error_identity_number': '', 'error_permis_number': '', 'error_domicile': ''})

    def _document_get_page_view_values(self, document, access_token, **kwargs):
        values = {
            'page_name': 'document',
            'document': document,
        }
        return self._get_page_view_values(document, access_token, values, 'my_documents_history', False, **kwargs)

    @http.route(['/my/document/<int:document_id>'], type='http', website=True)
    def portal_my_document(self, document_id=None,access_token=None, **kw):
        document=request.env['documents.document'].sudo().search(
            [('id', '=', document_id)],limit=1)

        if document:
            if document.state != 'refused':
                return request.redirect('/my/documents')
            document_sudo=document.sudo()
            if document.owner_id.id != http.request.env.user.id:
                return request.redirect('/my/documents')
        values = self._document_get_page_view_values(document_sudo, access_token, **kw)

        return request.render("mcm_contact_documents.portal_document_page",
                              values)

    @http.route(['/update/<int:document_id>'], type="http", auth="user", methods=['POST'], website=True, csrf=False)
    def update_document(self,document_id=None, **kw):
        document = request.env['documents.document'].sudo().search(
            [('id', '=', document_id)], limit=1)

        if document:
            try:
                files = request.httprequest.files.getlist('updated_document')
                attachments = request.env['ir.attachment'].sudo().search(
                    [("res_model", "=", "documents.document"), (("res_id", "=", document.id))])
                if not files:
                    files = request.httprequest.files.getlist('updated_document_cerfa')
                files2 = request.httprequest.files.getlist('updated_document_cerfa2')
                files3 = request.httprequest.files.getlist('updated_document_cerfa2')
                for ufile in files:
                    # mimetype = self._neuter_mimetype(ufile.content_type, http.request.env.user)
                    datas = base64.encodebytes(ufile.read())
                    if request.website.id==1:
                        vals = {
                            'state':'waiting',
                        }
                        document.sudo().write(vals)
                        request.env['ir.attachment'].sudo().create({
                            'name': "Cerfa",
                            'type': 'binary',
                            'datas': datas,
                            'res_model': 'documents.document',
                            'res_id': document.id
                        })
                    else:
                        vals = {
                            'state': 'waiting',
                        }
                        document.sudo().write(vals)
                        request.env['ir.attachment'].sudo().create({
                            'name': "Cerfa",
                            'type': 'binary',
                            'datas': datas,
                            'res_model': 'documents.document',
                            'res_id': document.id
                        })
                if files2:
                    datas_cerfa = base64.encodebytes(files2[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Cerfa Page 3",
                        'type': 'binary',
                        'datas': datas_cerfa,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                if files3:
                    datas_cerfa = base64.encodebytes(files3[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Cerfa Page 3",
                        'type': 'binary',
                        'datas': datas_cerfa,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)

        return request.redirect('/my/documents')

    @http.route(['/my/cerfa'], type='http', auth="public", website=True)
    def portal_cerfa(self):
        return request.render("mcm_contact_documents.cerfa_portal_template")


