# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pdb
from odoo.exceptions import UserError
from babel.dates import format_datetime, format_date, format_time

from datetime import datetime

import pytz
import time

from . import const
from .base import ZK


import logging

_logger = logging.getLogger(__name__)


class zkMachine(models.Model):

    _name = 'zk.machine.demo.udp'
    _description = 'Zk machine Model'

    name = fields.Char("Machine IP")
    port = fields.Char("Port Number")

        # Tester la  connexion avec la pointeuse
        # Se deconnecter apres une alerte de reussit

    def try_connection(self):
        for r in self:

            machine_ip = r.name
            port = int(r.port)
            zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, ommit_ping=False)
            conn = ''

            conn = zk.connect()
            pdb.set_trace()



            if conn:
                conn.disconnect()
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Connexion réussi',
                        'type': 'rainbow_man',
                    }
                }



