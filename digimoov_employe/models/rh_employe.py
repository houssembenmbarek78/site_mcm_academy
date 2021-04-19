# -*- coding: utf-8 -*-

from odoo import models, fields, api



class rh_employe(models.Model):
    _inherit = ['hr.employee']
    date_embauche = fields.Date(string="Date d'embauche")
    #To remove the fields we don't need in employee model
    invisible_field = fields.Char(string="Invisible Field")
    cin = fields.Char(string="CIN")
    cnss = fields.Char(string="CNSS")
    numero_compte_bancaire = fields.Char(string="Numéro de compte bancaire")
    ville = fields.Char(string="Ville")
    permis_de_travail = fields.Selection([('oui', 'Oui'), ('non', 'Non')])


# Sent a notification for the HR Manager
class rappel_embauche(models.Model):
    _name = 'digimoov.employe.rappelembauche'
    _description = 'An email will be sent automatically'

    # Cron method to verify and compare today date with the hire date
    def rappeltest(self):
        # Get all the employees
        employees = self.env['hr.employee'].search([])
       # Loop to extract the hire date for each company
        for i in employees:
            variable = i['date_embauche']
            # Hire date could be false if it's not mentioned in the employee profil
            if variable != False:
                JourEmbauche = variable.day
                MoisEmbauche = variable.month
                JourNow = fields.Datetime.now().day
                MoisNow = fields.Datetime.now().month
                # Check if it's we are in the same month and day as the hire date
                # Sent and email notification before a day
                if JourEmbauche == JourNow-1 and MoisNow == MoisEmbauche:
                    # email_template = self.env.ref('custom_attendance_2.email_template')
                    # if email_template:
                        print('print if')
                        # email_template.send_mail(i.work_email, force_send=True)

