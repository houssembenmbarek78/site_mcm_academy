import logging
import werkzeug
import odoo.http as http
import base64
import werkzeug
import requests
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
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        invoice_count = request.env['account.move'].search_count([
            ('type', 'in', ('out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt', 'in_receipt')),
            ('type_facture', '=', 'web'), ('cpf_solde_invoice', '=', False), ('cpf_acompte_invoice', '=', False)])
        values['invoice_count'] = invoice_count
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
            'pager': pager,
            'default_url': '/my/documents',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
        })
        return request.render("mcm_contact_documents.portal_my_documents", values)

    @http.route(['/submitted/document'], type="http", auth="user", methods=['POST'], website=True, csrf=False)
    def submit_documents(self, **kw):
        partner_id = http.request.env.user.partner_id
        print('partner')
        print(partner_id.name)
        folder_id = request.env['documents.folder'].sudo().search([('name', "=", _('Documents Clients'))])
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité Recto " + str(partner_id.name),
                        'datas': datas,
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
                        'datas': datas2,
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
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité " + str(partner_id.name),
                        'datas': datas,
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
                        print('document not found')
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")

            try:
                files = request.httprequest.files.getlist('permis[]')
                if len(files) == 2:
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire Recto " + str(partner_id.name),
                        'datas': datas,
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
                        'datas': datas2,
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
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire " + str(partner_id.name),
                        'datas': datas,
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
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Justificatif de domicile " + str(partner_id.name),
                        'datas': datas,
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
                    datas = base64.encodebytes(files[0].read())
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
                        'datas': datas,
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
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Attestation d'hébergement " + str(partner_id.name),
                        'datas': datas,
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Carte d'identité hebergeur Recto " + str(partner_id.name),
                        'datas': datas,
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
                        'datas': datas2,
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
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Carte d'identité hebergeur " + str(partner_id.name),
                        'datas': datas,
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

    @http.route('/upload_my_files', type="http", auth="user", methods=['POST'], website=True, csrf=False)
    def upload_my_files(self, **kw):
        print('upload_my_files')
        print(http.request.env.user.name)
        folder_id = request.env['documents.folder'].sudo().search(
            [('name', "=", _('Documents Clients')), ('company_id', "=", 2)])
        if not folder_id:
            vals_list = []
            vals = {
                'name': "Documents Clients",
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
        try:
            files = request.httprequest.files.getlist('identity')
            if files:
                vals_list = []
                vals = {
                    'name': "Carte d'identité",
                    'datas': False,
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité Recto",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité Verso",
                        'type': 'binary',
                        'datas': datas2,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité Recto Verso",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        try:
            files = request.httprequest.files.getlist('address_proof')
            if files:
                vals_list = []
                vals = {
                    'name': "Jusitificatif à domicile",
                    'datas': False,
                    'folder_id': int(folder_id),
                    'code_document': 'proof',
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Jusitificatif à domicile Recto",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Jusitificatif à domicile Verso",
                        'type': 'binary',
                        'datas': datas2,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Jusitificatif à domicile",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        try:
            files = request.httprequest.files.getlist('identity_hebergeur')
            if files:
                vals_list = []
                vals = {
                    'name': "Carte d'identité hébergeur",
                    'datas': False,
                    'folder_id': int(folder_id),
                    'code_document': 'hebergeur',
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité hébergeur Recto",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité hébergeur Verso",
                        'type': 'binary',
                        'datas': datas2,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Carte d'identité hébergeur",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        try:
            files = request.httprequest.files.getlist('attestation_hebergeur')
            if files:
                vals_list = []
                vals = {
                    'name': "Attestation d'hébergement",
                    'datas': False,
                    'folder_id': int(folder_id),
                    'code_document': 'hebergement',
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Attestation d'hébergement Recto",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Attestation d'hébergement Verso",
                        'type': 'binary',
                        'datas': datas2,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Attestation d'hébergement",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
        except Exception as e:
            logger.exception("Fail to upload document Carte d'identité ")
        try:
            files = request.httprequest.files.getlist('cerfa')
            if files:
                vals_list = []
                vals = {
                    'name': "Cerfa",
                    'datas': False,
                    'folder_id': int(folder_id),
                    'code_document': 'cerfa',
                    'confirmation': kw.get('confirm_cerfa'),
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
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Cerfa Recto",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                    request.env['ir.attachment'].sudo().create({
                        'name': "Cerfa Verso",
                        'type': 'binary',
                        'datas': datas2,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    request.env['ir.attachment'].sudo().create({
                        'name': "Cerfa",
                        'type': 'binary',
                        'datas': datas,
                        'res_model': 'documents.document',
                        'res_id': document.id
                    })
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
        print('document')
        print(document)
        if document:
            try:
                files = request.httprequest.files.getlist('updated_document')
                for ufile in files:
                    # mimetype = self._neuter_mimetype(ufile.content_type, http.request.env.user)
                    print('ufile')
                    print(ufile)
                    datas = base64.encodebytes(ufile.read())
                    vals = {
                        'datas': datas,
                        'state':'waiting',
                    }
                    document.sudo().write(vals)
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)

        return request.redirect('/my/documents')

    @http.route(['/my/cerfa'], type='http', auth="public", website=True)
    def portal_cerfa(self):
        return request.render("mcm_contact_documents.cerfa_portal_template")



