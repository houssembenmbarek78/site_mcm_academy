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
        check = False
        error_identity = ''
        error_identity_number = ''
        error_permis = ''
        error_permis_number = ''
        error_domicile = ''
        if (len(files_identity) == 0):
            check = True
            error_identity = 'error'
            check = True
            error_domicile = 'error'
        if check == True:
            return request.render("mcm_contact_documents.mcm_contact_documents_new_documents",
                                  {'partner_id': partner_id, 'error_identity': error_identity, 'error_identity_number': error_identity_number,
                                   'error_permis_number': error_permis_number})
        if (len(files_identity) > 2 ):
            name = http.request.env.user.name
            email = http.request.env.user.email
            return request.redirect('/new_documents')
        if not files_identity:
            return request.redirect('/new_documents')
        try:
            try:
                files = request.httprequest.files.getlist('identity')
                if len(files) == 1:
                    datas_idendity_name = base64.encodebytes(files[0].read())
                    datas_identity_email = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité Recto " + str(partner_id.name),
                        'datas': datas_idendity_name,
                        'folder_id': int(folder_id),
                        'code_document': 'identity',
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        ['|', '&', ('code_document', "=", 'identity'), ('owner_id', "=", http.request.env.user.id),
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
                        document = document.sudo().write(vals)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
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
            new_ticket = request.env['helpdesk.ticket'].sudo().create(
                vals)
        except:
            logger.exception("Fail to upload documents")
        return http.request.render('mcm_contact_documents.success_documents')
# Upload documents digimoov
    @http.route('/upload_my_files', type="http", auth="user", methods=['POST'], website=True, csrf=False)
    def upload_my_files(self, **kw):
        # charger le dossier des documents clients appartenant a Digimoov
        folder_id = request.env['documents.folder'].sudo().search(
            [('name', "=", _('Documents Digimoov')), ('company_id', "=", 2)])
        if not folder_id:
            vals_list = []
            # charger les documents appartenant seulement a digimoov
            vals = {
                'name': "Documents Digimoov",
                'company_id': 2
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
            if files:
                vals_list = []
                # charge le modele de la carte d'identité [un seul modele pour deux attachements]
                # on a pris les precaution au cas ou un client télécharge le recto et le verso avec le meme upload file
                # on a supprimer datas=False
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
                    # Attachement Carte d'identité Recto
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
                    # Attachement Carte d'identité recto
                elif len(files) == 1:
                    datas_carte_didentiterecto = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité recto",
                        'type': 'binary',
                        'datas': datas_carte_didentiterecto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")

        try:
            files2 = request.httprequest.files.getlist('identity2')
            if files2:
                vals_list = []
                vals = {
                    'name': "Carte d'identité verso",
                    'folder_id': int(folder_id),
                    'code_document': 'identity2',
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
                    # dans cette partie on a pris on compte si un client télécharge deux fichier par l'upload file
                    # cette option est désactiver dans la vue xml par le champs multiple
                if len(files2) == 2:
                    datas_cartedidenditeerecto = base64.encodebytes(files2[0].read())
                    datas_cartedidenditeeverso = base64.encodebytes(files2[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité Recto",
                        'type': 'binary',
                        'datas': datas_cartedidenditeerecto,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    # creation de l'attachement carte d'identité verso
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité verso",
                        'type': 'binary',
                        'datas': datas_cartedidenditeeverso,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                elif len(files2) == 1:
                    # cest notre cas puisqu'on a un seul attachement on parse la carte d identité verso
                    datas_cartedidenditeverso = base64.encodebytes(files2[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité Verso",
                        'type': 'binary',
                        'datas': datas_cartedidenditeverso,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")

        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        return http.request.render('mcm_contact_documents.success_documents')

        return http.request.render('mcm_contact_documents.success_documents')
    @http.route('/new_documents', type="http", auth="user", website=True)
    def create_documents(self, **kw):
        name = http.request.env.user.name
        email = http.request.env.user.email
        partner_id = http.request.env.user.partner_id
        print(partner_id.module_id.name)
        return http.request.render('mcm_contact_documents.mcm_contact_documents_new_documents', {
            'email': email, 'name': name, 'partner_id':partner_id ,'error_identity':'','error_identity_number':''})

    @http.route('/charger_mes_documents', type="http", auth="user", website=True)
    def create_documents_digimoov(self, **kw):
        name = http.request.env.user.name
        email = http.request.env.user.email
        partner_id = http.request.env.user.partner_id
        return http.request.render('mcm_contact_documents.mcm_contact_document_charger_mes_documents', {
            'email': email, 'name': name, 'partner_id': partner_id, 'error_identity': '', 'error_permis': '',
            'error_identity_number': ''})

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
        #view portal of refused document
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
        #search and get the refused document
        return request.redirect('/my/documents')

    @http.route(['/my/cerfa'], type='http', auth="public", website=True)
    def portal_cerfa(self):
        return request.render("mcm_contact_documents.cerfa_portal_template")

