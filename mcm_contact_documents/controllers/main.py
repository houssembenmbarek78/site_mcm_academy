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
        print('helloooo')
        folder_id = request.env['documents.folder'].sudo().search([('name', "=" , _('Documents Clients'))])
        if not folder_id:
            vals_list = []
            vals = {
                'name': "Documents Clients"
            }
            vals_list.append(vals)
            folder_id = request.env['documents.folder'].sudo().create(vals)
            vals_list = []
            vals = {
                'name': "Statut document",
                'folder_id': folder_id.id,
            }
            vals_list.append(vals)
            facet = request.env['documents.facet'].sudo().create(vals_list)
        files = request.httprequest.files.getlist('identity')
        files1 = request.httprequest.files.getlist('permis')
        print(len(files))
        print(len(files1))
        if(len(files) >2 or len(files1) > 2):
            name = http.request.env.user.name
            email = http.request.env.user.email
            return request.redirect('/new_documents')
        try:
            try:
                files = request.httprequest.files.getlist('identity')
                if len(files) == 2:
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité Recto " + str(partner_id.name),
                        'datas': datas,
                        'code': 'identity_recto',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code', "=", 'identity_recto'), ('owner_id', "=", http.request.env.user.id)], limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité Verso " + str(partner_id.name),
                        'datas': datas2,
                        'code': 'identity_verso',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code', "=", 'identity_verso'), ('owner_id', "=", http.request.env.user.id)], limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité " + str(partner_id.name),
                        'datas': datas,
                        'code': 'identity',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code', "=", 'identity'), ('owner_id', "=", http.request.env.user.id)], limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")
            try:
                files = request.httprequest.files.getlist('domicile')
                vals_list = []
                for ufile in files:
                    # mimetype = self._neuter_mimetype(ufile.content_type, http.request.env.user)
                    datas = base64.encodebytes(ufile.read())
                    vals = {
                        'name': "Justificatif de domicile " + str(partner_id.name),
                        'datas': datas,
                        'code': 'domicile',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code', "=", 'domicile'), ('owner_id', "=", http.request.env.user.id)], limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)
            try:
                files = request.httprequest.files.getlist('permis')
                if len(files) == 2:
                    datas = base64.encodebytes(files[0].read())
                    datas2 = base64.encodebytes(files[1].read())
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire Recto " + str(partner_id.name),
                        'datas': datas,
                        'code' : 'permis_recto',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number_permis'),
                        'confirmation': kw.get('confirmation2'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code', "=", 'permis_recto'), ('owner_id', "=", http.request.env.user.id)], limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                    vals_list = []
                    vals = {
                        'name': "Permis de conduire Verso" + str(partner_id.name),
                        'datas': datas2,
                        'code': 'permis_verso',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number_permis'),
                        'confirmation': kw.get('confirmation2'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document = request.env['documents.document'].sudo().search(
                        [('code', "=", 'permis_verso'), ('owner_id', "=", http.request.env.user.id)], limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
                elif len(files) == 1:
                    datas = base64.encodebytes(files[0].read())
                    vals_list = []
                    vals = {
                        'name': "Pièce d'identité " + str(partner_id.name),
                        'datas': datas,
                        'code': 'permis',
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id),
                        'attachment_number': kw.get('number'),
                        'confirmation': kw.get('confirmation'),
                        'owner_id': http.request.env.user.id}
                    vals_list.append(vals)
                    document=request.env['documents.document'].sudo().search([('code', "=", 'permis'),('owner_id',"=",http.request.env.user.id)],limit=1)
                    if document:
                        document = request.env['documents.document'].sudo().write(vals_list)
                    else:
                        document = request.env['documents.document'].sudo().create(vals_list)
            except Exception as e:
                logger.exception("Fail to upload document ")
            return http.request.render('mcm_contact_documents.success_documents')
        except:
            logger.exception("Fail to upload documents")
        return http.request.render('mcm_contact_documents.success_documents')

    @http.route('/new_documents', type="http", auth="user", website=True)
    def create_documents(self, **kw):
        name = http.request.env.user.name
        email = http.request.env.user.email
        return http.request.render('mcm_contact_documents.mcm_contact_documents_new_documents', {
            'email': email, 'name': name})

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
        try:
            document_sudo = self._document_check_access('documents.document', document_id, access_token)
        except AccessError:
            return request.redirect('/my')
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

