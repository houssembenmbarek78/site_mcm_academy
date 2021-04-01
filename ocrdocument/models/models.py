# -*- coding: utf-8 -*-

from odoo import models, fields, api
from cv2 import cv2
import logging
import pdb
from odoo.exceptions import UserError,ValidationError
from pytesseract import pytesseract


logger = logging.getLogger(__name__)

class ocrdocument(models.Model):
    _name = 'ocrdocument.ocrdocument'
    _description = 'ocrdocument.ocrdocument'

    name = fields.Char()
    description = fields.Char(string="description")
    documents = fields.Binary(string="Documents")
# Extract text from image with open cv into text
    def trycv(self):
        # cap = cv2.VideoCapture(0;)
        #
        # # Check whether user selected camera is opened successfully.
        #
        # if cap.isOpened():
        #     return {
        #         'warning': {
        #             'title': 'Erreur',
        #             'message': 'Erreur video non ouverte'
        #         },
        #     }
        #
        # cap.set(3, 1280)
        # cap.set(4, 720)
        # while (True):
        #     # Capture frame-by-frame
        #
        #     ret, frame = cap.read()
        #
        #     # Display the resulting frame
        #     if not ret:  # exit loop if there was problem to get frame to display
        #         break
        #     cv2.imshow('preview', frame)
        #
        #     # Waits for a user input to quit the application
        #
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # # When everything done, release the capture
        #
        # cap.release()
        #
        # cv2.destroyAllWindows()

        try:
            cap = cv2.VideoCapture(0)
            cap.set(3, 1280)
            cap.set(4, 720)
            # logger.info("%s: %s", cap)
            # pdb.set_trace()
            while (True):
                # Capture frame-by-frame

                ret, frame = cap.read()

                # Display the resulting frame
                if not ret:  # exit loop if there was problem to get frame to display
                    break
                cv2.imshow('preview', frame)

                # Waits for a user input to quit the application

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # When everything done, release the capture

            cap.release()

            cv2.destroyAllWindows()
        except Exception as e:
            logger.exception("Fail to display new window")

    def trytesseract(self):
        image = pytesseract.image_to_string('/ocrdocument/static/img/image.png')
        raise ValidationError(image)