# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: cybrosys(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Hide Auto Sign Portal',
    'version': '13.0.1.1.2',
    'summary': """Integrating Biometric Device (Model: ZKteco uFace 202) With HR Attendance (Face + Thumb)""",
    'description': """This module integrates Odoo with the biometric device(Model: ZKteco uFace 202),odoo13,odd,hr,attendance""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Cybrosys Techno Solutions, Mostafa Shokiel',
    'company': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['web', 'base', 'website', 'sale', 'website_sale', 'portal'],
    'data': [
        'views/hide_auto.xml',
    ],

    'qweb': [
        # 'static/src/xml/hide_auto_sign_portal.xml'
    ],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
