from odoo import fields,models,api,exceptions
import requests
from datetime import datetime,timedelta,date
import locale


class Parcours(models.Model):
    _name = 'plateforme_pedagogique.parcours'

    id_parcours=fields.Char(string="id Parcours")
    hasUserLimit=fields.Boolean(string="limite")
    endDate= fields.Char(string="Date fin")
    programTemplate =fields.Char(string="id programTemplate")
    startDate=fields.Char(string="Date Début")
    groupe_id=fields.Many2one('plateforme_pedagogique.groupe',string='groupe')
    group_id_plateforme=fields.Char()
    name = fields.Char(string="Nom")
    programDuration=fields.Char(string="Durée du programme")
    programDurationType=fields.Char(string="Type de Programme")
    completed=fields.Char(string="Utilisateurs qui ont terminé la session de parcours ")
    registered=fields.Char(string="Utilisateurs enregistrés")
    attendees=fields.Char(string="Participants")
    etat=fields.Char(string="Etat de parcours")
    User_stats=fields.One2many('plateforme_pedagogique.user_stats','parcours_ids','Apprenants')



    #Récupérer la liste des parcours
    def getParcours(self):
        locale.setlocale(locale.LC_TIME, str(self.env.user.lang) + '.utf8')
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        resp_session_parcours=requests.get('https://app.360learning.com/api/v1/programs/sessions',params=params)
        sessions_parcours=resp_session_parcours.json()
        for session in sessions_parcours:
          id_session=session['_id']
          res_session = requests.get('https://app.360learning.com/api/v1/programs/sessions/'+id_session+'/stats',params=params)
          session_stat=res_session.json()
          session_name=session_stat['name']
          completed=session_stat['completed']
          registered=session_stat['registered']
          attendees=session_stat['attendees']
          start_date_str = str(session['startDate'])
          date_split = start_date_str[0:19]
          start_date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
          # new_format = '%d %B, %Y, %H:%M:%S'
          # start_date = date.strftime(new_format)

          #changer Forma  de date fin
          end_date = str(session['endDate'])
          date_split = end_date[0:19]
          date_end = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")

          #Chercher si parcours existant sur odoo ou non
          # un parcours identifié par son nom et son date debut
          find_parcours = self.env['plateforme_pedagogique.parcours'].sudo().search([('name', "=", session_name),
                                                                                     ('startDate', "=" , start_date)
                                                                                    ])
          #Si n'est pas sur odoo on l'ajoute , et dégager son état (fermé/ouvert) à partir de date fin
          if not (find_parcours):
              print(' not finnnnd', start_date, find_parcours.startDate)
              etat = ""
              today = datetime.today()
              print(today, date_end)
              if (date_end < today):
                  etat = "fermé"
              else:
                  etat = "ouvert"
              print('notfind',etat, today, end_date)
              print(find_parcours)
              find_parcours=self.env['plateforme_pedagogique.parcours'].create({
                  'name': session_name,
                  'completed': completed,
                  'registered': registered,
                  'attendees': attendees,
                  'endDate': date_end,
                  'startDate': start_date,

                  'etat':etat
              })
          #Si existant on change les valeurs existants .
          if (find_parcours):
              print('finnnnd', start_date, find_parcours.startDate)
              etat=""
              today = datetime.today()
              print(today, date_end)
              if ( date_end < today)  :
                   etat="fermé"
                   print(etat,today,date_end)
              else:
                   etat="ouvert"
              print('find',etat, today, end_date)
              find_parcours.sudo().write({
                   'completed':completed,
                   'registered':registered,
                   'attendees':attendees,
                   'endDate': date_end,

                   'startDate': start_date,
                   'etat': etat
              })

    #Récupérer les statistiques des utilisateurs de chaque parcours
    def getUser_Stats(self):
        locale.setlocale(locale.LC_TIME, str(self.env.user.lang) + '.utf8')

        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        resp_session_parcours = requests.get('https://app.360learning.com/api/v1/programs/sessions', params=params)
        sessions_parcours = resp_session_parcours.json()
        for session in sessions_parcours:
            id_session = session['_id']
            res_session = requests.get('https://app.360learning.com/api/v1/programs/sessions/' + id_session + '/stats',
                                       params=params)
            session_stat = res_session.json()
            session_name = session_stat['name']
            completed = session_stat['completed']
            registered = session_stat['registered']
            attendees = session_stat['attendees']
            start_date_str = str(session['startDate'])
            date_split = start_date_str[0:19]
            start_date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
            # new_format = '%d %B, %Y, %H:%M:%S'
            # start_date = date.strftime(new_format)

            # changer Forma  de date fin
            end_date = str(session['endDate'])
            date_split = end_date[0:19]
            date_end = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")

            #Chercher parcours sur odoo
            find_parcours = self.env['plateforme_pedagogique.parcours'].sudo().search([('name', "=", session_name),
                                                                                       ('startDate', "=", start_date)
                                                                                      ])
            if not(find_parcours):
                print('notfinddddddd')
            if (find_parcours):
                print('finnnnd', start_date,find_parcours.name, find_parcours.startDate)
                userStats = session_stat['usersStats']
                list=[]
                if userStats:
                    for userStat in userStats:
                        firstname = ""
                        if 'firstName' in userStat:
                            firstname = userStat['firstName']
                        lastname=''
                        if 'lastName' in userStat:
                            lastname=userStat['lastName']
                        enddate=''
                        if 'endTime' in userStat:
                         if userStat['endTime']:
                          endtime_str = str(userStat['endTime'])

                          date_split = str(endtime_str[0:18])
                          print(date_split,'dataaaa')
                          end_date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                          new_format = '%d %B, %Y'
                          enddate = str(end_date.strftime(new_format))
                        mail = userStat['mail']
                        total_time=''
                        time=0
                        if 'totalTimeSpentInSeconds' in userStat:
                            time = int(userStat['totalTimeSpentInSeconds'])
                        total_time =self.decoupe(time)
                        print('totallllll',total_time)
                        score=str(userStat['score'])+'%'
                        progress="0%"
                        if 'progress' in userStat:
                            progress= str(userStat['progress'])+"%"
                        startdate=''
                        if 'startTime' in userStat:
                         if userStat['startTime'] :
                          start_date_str=str(userStat['startTime'])
                          date_split = start_date_str[0:18]
                          start_date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                          new_format = '%d %B, %Y'
                          startdate = str(start_date.strftime(new_format))

                        exist = False
                        for user_statiq in  find_parcours.User_stats:
                            if (user_statiq.mail == mail):
                                exist=True
                                list.append(user_statiq.id)
                                print("existe",exist)
                        if not (exist):
                            print('not find', )
                            find_user = self.env['plateforme_pedagogique.user_stats'].sudo().search([('mail', "=", mail),
                                                                                                     ('parcours_ids','=',find_parcours.id)], limit=1)
                            if (find_user):
                                print('finduser,',find_user.mail)
                                find_user.sudo().write({
                                    'firstName': firstname,
                                    'lastName': lastname,
                                    'score': score,
                                    'mail': userStat['mail'],
                                    'totalTimeSpentInSeconds':total_time,
                                    'progress': progress,
                                    'endTime': enddate,
                                    'startTime': startdate,
                                    'deleted': userStat['deleted'],
                                    'parcours_ids': find_parcours.id,
                                })
                                list.append(find_user.id)
                            if not (find_user)   :
                                find_user=self.env['plateforme_pedagogique.user_stats'].sudo().create({
                                        'firstName':firstname,
                                        'lastName':lastname,
                                        'score':score,
                                        'mail':userStat['mail'],
                                        'totalTimeSpentInSeconds': total_time,
                                        'progress':progress,
                                        'endTime':enddate,
                                        'startTime':startdate,
                                        'deleted':userStat['deleted'],
                                        'parcours_ids':find_parcours.id,
                                    } )
                                list.append(find_user.id)
                # Remplacer la liste des statistique existantes par list récupéré
                find_parcours.sudo().write({
                        'User_stats': [(6,0, list)],
                           })

    #Découper le temps en seconde , minutes ,heures
    def decoupe( self ,seconde):
        heure=0
        minute=0
        heure = seconde // 3600
        seconde %= 3600
        minute = seconde // 60
        seconde %= 60
        if (heure==0 and minute!=0 and seconde!=0):
            return ( str(minute) +'min' + str(seconde) +'s')
        if (heure==0 and minute ==0 ):
            return ( str(seconde) +'s')
        if (heure != 0 and minute == 0 ):
            return (str(heure)+'h')
        if (heure != 0 and minute !=0 and seconde!=0):
            return (str(heure) +'h'+ str(minute) +'min'+ str(seconde) +'s')