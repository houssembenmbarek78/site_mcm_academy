from odoo import models,fields,api

class Users(models.Model):
  _inherit = "res.users"

  password360= fields.Char(string="password360")
  """Héritage de methode _set_password pour recuperer le mot de passe apres 
   l'inscription et avant le cryptagem """
  def _set_password(self):
     for user in self:
       user.password360=user.password
     return super(Users, self)._set_password()






