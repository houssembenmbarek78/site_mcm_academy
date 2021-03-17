# -*- coding: utf-8 -*-
from struct import pack  # , unpack


class Attendance(object):
    encoding = 'UTF-8'

    def __init__(self, user_id, timestamp, status, punch=0, uid=0):
        self.uid = uid  # not really used any more
        self.user_id = user_id
        self.timestamp = timestamp
        self.status = status
        self.punch = punch

    @staticmethod
    def json_unpack(json):
        # validate?
        return Attendance(
            uid=json['uid'],
            status=json['status'],
            timestamp=json['timestamp'],
            punch=json['punch'],
            card=json['card']
        )

    def repack29(self):  # with 02 for zk6 (size 29)
        return pack("<BHB5s8sIxBhI", 2, self.uid, self.state,
                    self.timestamp.encode(Attendance.encoding, errors='ignore'),
                    self.space.encode(Attendance.encoding, errors='ignore'), self.card)

    def repack73(self):  # with 02 for zk8 (size73)
        # password 6s + 0x00 + 0x77
        # 0,0 => 7sx group id, timezone?
        return pack("<BHB8s24sIB7sx24s", 2, self.uid, self.state,
                    self.timestamp.encode(Attendance.encoding, errors='ignore'),
                    self.space.encode(Attendance.encoding, errors='ignore'), self.card, 1)

    def __str__(self):
        return '<Attendance>: {} : {} ({}, {})'.format(self.user_id, self.timestamp, self.status, self.punch)

    def __repr__(self):
        return '<Attendance>: {} : {} ({}, {})'.format(self.user_id, self.timestamp, self.status, self.punch)
