# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, SUPERUSER_ID, _
from odoo.exceptions import UserError
from babel.dates import format_datetime, format_date, format_time

from datetime import datetime

import pytz
import time

from . import const
from .base import ZK

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging

_logger = logging.getLogger(__name__)


class zkMachine(models.Model):

    _name = 'zk.machine.demo.udp'

    name = fields.Char("Machine IP")
    port = fields.Integer("Port Number")

        # Tester la  connexion avec la pointeuse
        # Se deconnecter apres une alerte de reussite

    def try_connection(self):
        for r in self:

            machine_ip = r.name
            port = r.port
            zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, ommit_ping=False)
            conn = ''
            try:

                conn = zk.connect()

            except Exception as e:
                raise UserError('The connection has not been achieved')
            finally:
                if conn:
                    conn.disconnect()
                    return {
                        'effect': {
                            'fadeout': 'slow',
                            'message': 'Connexion réussi',
                            'type': 'rainbow_man',
                        }
                    }



class attendanceLog(models.Model):
    _name = 'attendance.log'
    _description = "Attendance ZK"
    name = fields.Char()
    status = fields.Char()
    date = fields.Date()
    checkin = fields.Char()
    checkout = fields.Char()

    # Afficher toutes les presences enregistre sur la pointeuse

    def download_data(self):
        for r in self:

            machine_ip = '192.168.1.201'
            port = 4370
            zk = ZK(machine_ip, port=port, timeout=10, password=0, force_udp=False, ommit_ping=False)
            conn = ''
            try:

                conn = zk.connect()
                users = conn.get_users()
                x = conn.get_attendance()

                username = ' '
                # Loop for all the attendance list
                for record in x:
                    RecordUser = []
                    dateone = record.timestamp.strftime('%Y%m%d')

                    # Second Loop for all the attendance
                    # Compare the users and dates
                    # The same users in the same date will be added in Record User list
                    # This methods is used because we can't know if the attendance is a check in ou out

                    for record2 in x:
                        datetwo = record2.timestamp.strftime('%Y%m%d')
                        if record.user_id == record2.user_id and datetwo == dateone:
                            RecordUser.append(record2)

                    # Test on the length of list RecordUser
                    # If we have more than one the list contains a check in and check out
                    # Variables am and pm each take a time
                    if len(RecordUser)>1:
                        itemone = RecordUser.__getitem__(0).timestamp
                        itemtwo = RecordUser.__getitem__(1).timestamp
                        am = datetime.strftime(itemone, "%X")
                        pm = datetime.strftime(itemtwo, "%X")

                    # If the list contains only one attendance
                    # Variable am contains the check in and pm a value of 0 until the next check out
                    else:
                        itemone = RecordUser.__getitem__(0).timestamp
                        am=datetime.strftime(itemone, "%X")
                        pm=0


                    # This loop To extract the names of the users in each attendance
                    # The attendance only have a user_id
                    for y in users:
                        if record.user_id == y.user_id:
                            username = y.name
                    values = {
                        "name": username,
                        "status": record.status,
                        "date": record.timestamp,
                        "checkin": str(am),
                        "checkout": str(pm)
                    }
                    self.env['attendance.log'].sudo().create(values)

                    # Both the attendance inserted need to be removed from the list
                    # The same thing will be done in the second two items
                    # Until the list is empty

                    if len(RecordUser)>1:
                        x.remove(RecordUser.__getitem__(0))
                        x.remove(RecordUser.__getitem__(1))
                    else:
                        x.remove(RecordUser.__getitem__(0))


            except Exception as e:
                raise UserError('The connection has not been achieved')
            finally:
                if conn:
                    conn.disconnect()
                    return {
                        'effect': {
                            'fadeout': 'slow',
                            'message': 'Téléchargement réussi',
                            'type': 'rainbow_man',
                        }
                    }
