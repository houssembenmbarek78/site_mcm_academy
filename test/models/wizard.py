from odoo import models,fields,api

class wizard(models.TransientModel):
    _name ='test.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    # session_id=fields.Many2one('test.session',
    #                             string="Session", required=True)
    attendee_ids= fields.Many2many('res.partner', string='Participants')
    session_ids = fields.Many2many('test.session', string='Sessions',required=True)

    # def _default_session(self):
    #
    #       return self.env['test.session'].browse(self._context.get('active_id'))

    def _default_sessions(self):
        x=self.env['test.session'].browse(self._context.get('active_ids'))
        print(x)
        return self.env['test.session'].browse(self._context.get('active_ids'))

    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}








































































































