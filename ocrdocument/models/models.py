# -*- coding: utf-8 -*-

from odoo import models, fields, api
from cv2 import cv2
from pytesseract import pytesseract




class ocrdocument(models.Model):
    _name = 'ocrdocument.ocrdocument'
    _description = 'ocrdocument.ocrdocument'

    name = fields.Char()
    description = fields.Char(string="description")
# Extract text from image with open cv into text
    def trycv(self):
        cap = cv2.VideoCapture(0)

        # Check whether user selected camera is opened successfully.

        if not (cap.isOpened()):
            print('Could not open video device')

        cap.set(3, 640)
        cap.set(4, 480)
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
