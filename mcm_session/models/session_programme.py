# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.tools.float_utils import float_round

class Programme(models.Model):
    _name = 'mcmacademy.programme'

    name=fields.Char('Titre de programme')
    sous_titre=fields.Char('Sous titre')
    code=fields.Char('',default='PR1728365290')
    formation_type=fields.Selection(selection=[
        ('presentielle', 'FORMATION PRÉSENTIELLE'),
        ('mixte', 'FORMATION mixte'),
        ('distance', 'FORMATION à distance'),
    ], string='Type de formation')
    handicap_acces=fields.Char('Accès handicapé')
    effectif_limit=fields.Boolean("Limites d'effectif")
    action_id=fields.Many2one('mcmacademy.action',"Type d'action de formation")
    domain_id=fields.Many2one('mcmacademy.domain',"Domaine de formation")
    diplome_vise=fields.Selection(selection=[
        ('aucun', 'Aucun'),
        ('cqp_without_rncp', 'Certificat de qualification professionnelle (CQP) sans niveau de qualification enregistré au RNCP'),
        ('cqp_without_rs', 'CQP non enregistré au RNCP ou au RS'),
        ('niveau2', 'Niveau II'),
        ('niveau3', 'Niveau III (BEP, CAP)'),
        ('niveau4', 'Niveau IV (BAC professionnel, BT, BP, BM)'),
        ('niveau5', 'Niveau V (BTS, DUT, écoles de formation sanitaire et sociale)'),
        ('niveau6', 'Niveau VI à VIII (Licence, Master, diplôme d’ingénieur, Doctorat)'),
        ('cqp_rs', '(Formations anciennes) Formations visant une certification et/ou une habilitation inscrite à l’inventaire de la CNCP'),
    ], string='Diplôme visé par la formation',default='aucun')
    nom_titre_vise=fields.Char('Nom du titre visé')
    bloc_competance=fields.Boolean('Bloc de compétence')
    description=fields.Text('Description de programme')
    objectifs=fields.One2many('mcmacademy.programme.objectif','programme_id','OBJECTIFS PÉDAGOGIQUES')
    clients_potentiels=fields.One2many('mcmacademy.programme.clientpotentiel','programme_id','Clients potentiels')
    prerequis=fields.One2many('mcmacademy.programme.prerequis','programme_id','Pré-Requis')
    description_pedagogique=fields.Char("Description de l'équipe pédagogique")
    suivi_execution=fields.One2many('mcmacademy.suiviexecution','programme_id',"Suivi de l'exécution et évaluation des résultats")
    ressources_pedagogique=fields.One2many('mcmacademy.ressources','programme_id','Ressources pédagogiques')
    resultat_attendu=fields.Char("Résultats attendus à l'issue de la formation")
    modalite_obtention=fields.Char("Modalités d'obtention")
    details_certification=fields.Char("Détails dur la certification")
    duree_validite=fields.Char("Durée de validité")
    indicateur_resultat=fields.Char("Indicateurs de résultats")
    code_de_produit=fields.Char("Code de produit en Comptabilité")
    code_de_produit_pour_financeurs=fields.Char("Code de produit en Comptabilité pour financeurs (optionel)")
    code_comptabilite_analytique=fields.Char("Code comptabilite analytique")
    type_parcours_formation=fields.Selection(selection=[
        ('collectif', 'COLLECTIF'),
        ('individualise', 'INDIVIDUALISÉ'),
        ('modulaire', 'MODULAIRE'),
        ('mixte', 'Mixte(parcours individualisé et modularisé)'),
    ], string='Type de parcours de formation',default='collectif')
    niveau_entree = fields.Selection(selection=[
        ('sans_niveau', 'SANS NIVEAU'),
        ('niveau_6','niveau VI (illettrisme, analphabétisme)'),
        ('niveau_5_bis', 'niveau V bis (préqualification)'),
        ('niveau_5', 'niveau V (CAP, BEP, CFPA du premier degré)'),
        ('niveau4', 'niveau IV (BP, BT, baccalauréat professionnel)'),
        ('niveau3', 'niveau III (BTS, DUT)'),
        ('niveau2', 'niveau II (licence ou maîtrise universitaire)'),
        ('niveau1', 'niveau I (supérieur à la maîtrise)'),
        ('information_nom_communique', 'information non communiquée'),
    ], string="Niveau d'entrée", default='sans_niveau')
    niveau_entree_obligatoire=fields.Boolean("Niveau d'entrée obligatoire")
    niveau_sortie = fields.Selection(selection=[
        ('sans_niveau', 'SANS NIVEAU'),
        ('niveau_6','niveau VI (illettrisme, analphabétisme)'),
        ('niveau_5_bis', 'niveau V bis (préqualification)'),
        ('niveau_5', 'niveau V (CAP, BEP, CFPA du premier degré)'),
        ('niveau4', 'niveau IV (BP, BT, baccalauréat professionnel)'),
        ('niveau3', 'niveau III (BTS, DUT)'),
        ('niveau2', 'niveau II (licence ou maîtrise universitaire)'),
        ('niveau1', 'niveau I (supérieur à la maîtrise)'),
        ('information_nom_communique', 'information non communiquée'),
    ], string="Niveau de sortie", default='sans_niveau')
    rythme_formation = fields.Selection(selection=[
        ('journee', 'En journée'),
        ('soiree','En soirée'),
        ('semaine', 'En semaine'),
        ('weekend', 'Le week-end'),
        ('temps_plein', 'Temps plein'),
        ('partiel', 'Temps partiel'),
        ('rythmes', 'Plusieurs rythmes'),
    ], string="Rythme de la formation", default='journee')
    modalite_entree_sortie=fields.Selection(selection=[
        ('date_fixe', 'A dates fixes'),
        ('permanentes','Permanentes (Sans dates fixes)'),
    ], string="Modalité entrée sortie", default='date_fixe')
    lang=fields.Many2one('res.lang','Langue',domain=['|',('active','=',True),('active','=',False)],default=lambda self: self.env['res.lang'].search([('code','=','fr_FR')]))
    modalite_admission = fields.Selection(selection=[
        ('disposition_particuliere', 'Admission sans disposition particulière'),
        ('sur_dossier','Admission sur dossier'),
        ('sur_concours', 'Admission sur concours'),
        ('apres_entretien', 'Admission après entretien'),
        ('apres_test', 'Admission après test'),
        ('apres_visite_medical', 'Admission après visite médical'),
        ('plusieurs_modalites', 'Plusieurs modalités possibles'),
    ], string="Modalité d'admission", default='disposition_particuliere')

    consctruction_forfaitaire = fields.Selection(selection=[
        ('forfaitaire', 'Forfait: Calcul formaitaire'),
        ('assiduité', 'Assiduité: Calcul en heures,demi-journée,jour'),
    ], string="Construction forfaitaire", default='forfaitaire')
    certif_inclus=fields.Boolean('Certification inclus dans les frais annexes')
    code_certif=fields.Char('Code Certif Info')
    objectif_general=fields.Selection(selection=[
        ('perfectionnement', 'Perfectionnement, élargissement des compétences'),
        ('creation_entreprise',"Création d'entreprise"),
        ('remise_certification', 'Remise de certification'),
        ('certification', 'Certification'),
        ('professionnalisation', 'Professionnalisation'),
        ('preparation_a_la_qualification', 'Préparation à la qualification'),
        ('remobilisation', "(Re)mobilisation, aide à l'élaboration de projet professionnel"),
    ], string="Objectif général", default='perfectionnement')
    module_id=fields.Many2one('mcmacademy.module')
    description_client_prerequis=fields.Html('',compute='get_description')
    description_modalite_certification=fields.Html('',compute='get_description')
    description_qualite=fields.Html('',compute='get_description')
    duree_heure=fields.Char('')
    duree_jours=fields.Char('')
    min_limit=fields.Integer('Min')
    max_limit=fields.Integer('Max')
    prix_normal = fields.Monetary('Prix Particulier')
    prix_chpf = fields.Monetary('Prix CHPF')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    def get_description(self):
        for rec in self:
            rec.description_client_prerequis='<div class="tip"><p><strong class="main">A qui allez-vous vous adresser&nbsp;?</strong></p><p><strong>Qui sont vos stagiaires&nbsp;?</strong></p><p>Exemples:</p><ul class="examples"><li>“Experts comptables.”</li><li>“Cadres des services techniques municipaux.”</li></ul><p><strong class="main">Quel niveau vos stagiaires ont-ils ?</strong></p><p><strong>Précisez leurs niveaux de connaissances, de savoir-faire et d’expériences professionnelles.</strong></p><p>Les nouvelles connaissances  que vont acquérir vos stagiaires au cours de votre formation sont dans la continuité de ce qu’ils ont déjà acquis</p><p>Exemples:</p><ul class="examples"><li>“Maitrise de la première version du logiciel SCM.”</li></ul><br></br><br></br><br></br><br></br></div>'
            rec.description_modalite_certification="<div class='tip'><p><strong class='main'>Résultats attendus à l'issue de la formation</strong></p><p>Ils matérialisent le passage en formation et en précisent les modalités de reconnaissance ou de validation.</p><p><strong class='main'>Modalités d'obtention</strong></p><ul class='examples'><li>“Obtentions par certification.”</li><li>“Délivrance d'une attestation.”</li></ul><p><strong class='main'>Détails sur la certification</strong></p><p>Informations sur les équivalences, passerelles, suites de parcours et les débouchés.</p><p><strong class='main'>Durée de validité</strong></p><p>Optionelle, par défaut il n'y a pas de limite de validité.</p><p>À utiliser dans le cadre du « recyclages » ou revalorisation des compétences acquises quand les conditions d’exercice de certaines activités changent (ex :dans le domaine du sport) et / ou que le contenu de son référentiel est appelé à évoluer.</p></div>"
            rec.description_qualite="<div class='tip'><p><strong class='main'>Indicateurs de résultats</strong></p><p>Donner une information chiffrée sur le niveau de performance et d’accomplissement de la prestation.</p><ul class='examples'><li>Taux de satisfaction des stagiaires.</li><li>Nombre de stagiaires.</li><li>Taux et causes des abandons.</li><li>Taux de retour des enquêtes.</li><li>Taux d'interruption en cours de prestation.</li><li>Taux de rupture des contrats d’alternance.</li><li>Taux d'insertion dans l'emploi.</li></ul></div>"

    @api.model
    def default_get(self, fields):
        suivi_execution = self.env['mcmacademy.suiviexecution']
        ids = []
        suivi = {'sequence': 1, 'name': 'Feuilles de présence.'}  # dict for fields and their values
        sr = suivi_execution.create(suivi)
        ids.append(sr.id)
        suivi = {'sequence': 2, 'name': 'Questions orales ou écrites (QCM).'}  # dict for fields and their values
        sr = suivi_execution.create(suivi)
        ids.append(sr.id)
        suivi = {'sequence': 3, 'name': 'Mises en situation.'}  # dict for fields and their values
        sr = suivi_execution.create(suivi)
        ids.append(sr.id)
        suivi = {'sequence': 4, 'name': "Formulaires d'évaluation de la formation."}  # dict for fields and their values
        sr = suivi_execution.create(suivi)
        ids.append(sr.id)
        self = self.with_context(
            default_suivi_execution=ids,
        )

        suivi_execution = self.env['mcmacademy.ressources']
        ids = []
        ressource = {'sequence': 1, 'name': 'Accueil des stagiaires dans une salle dédiée à la formation.'}  # dict for fields and their values
        sr = suivi_execution.create(ressource)
        ids.append(sr.id)
        ressource = {'sequence': 2, 'name': 'Documents supports de formation projetés.'}  # dict for fields and their values
        sr = suivi_execution.create(ressource)
        ids.append(sr.id)
        ressource = {'sequence': 3, 'name': 'Exposés théoriques'}  # dict for fields and their values
        sr = suivi_execution.create(ressource)
        ids.append(sr.id)
        ressource = {'sequence': 4, 'name': "Etude de cas concrets"}  # dict for fields and their values
        sr = suivi_execution.create(ressource)
        ids.append(sr.id)
        ressource = {'sequence': 5, 'name': "Quiz en salle"}  # dict for fields and their values
        sr = suivi_execution.create(ressource)
        ids.append(sr.id)
        ressource = {'sequence': 6, 'name': "Mise à disposition en ligne de documents supports à la suite de la formation."}  # dict for fields and their values
        sr = suivi_execution.create(ressource)
        ids.append(sr.id)
        self = self.with_context(
            default_ressources_pedagogique=ids,
        )

        self = self.with_context(
            default_description_client_prerequis='<div class="tip"><p><strong class="main">A qui allez-vous vous adresser&nbsp;?</strong></p><p><strong>Qui sont vos stagiaires&nbsp;?</strong></p><p>Exemples:</p><ul class="examples"><li>“Experts comptables.”</li><li>“Cadres des services techniques municipaux.”</li></ul><p><strong class="main">Quel niveau vos stagiaires ont-ils ?</strong></p><p><strong>Précisez leurs niveaux de connaissances, de savoir-faire et d’expériences professionnelles.</strong></p><p>Les nouvelles connaissances  que vont acquérir vos stagiaires au cours de votre formation sont dans la continuité de ce qu’ils ont déjà acquis</p><p>Exemples:</p><ul class="examples"><li>“Maitrise de la première version du logiciel SCM.”</li></ul><br></br><br></br><br></br><br></br></div>',
            default_description_modalite_certification="<div class='tip'><p><strong class='main'>Résultats attendus à l'issue de la formation</strong></p><p>Ils matérialisent le passage en formation et en précisent les modalités de reconnaissance ou de validation.</p><p><strong class='main'>Modalités d'obtention</strong></p><ul class='examples'><li>“Obtentions par certification.”</li><li>“Délivrance d'une attestation.”</li></ul><p><strong class='main'>Détails sur la certification</strong></p><p>Informations sur les équivalences, passerelles, suites de parcours et les débouchés.</p><p><strong class='main'>Durée de validité</strong></p><p>Optionelle, par défaut il n'y a pas de limite de validité.</p><p>À utiliser dans le cadre du « recyclages » ou revalorisation des compétences acquises quand les conditions d’exercice de certaines activités changent (ex :dans le domaine du sport) et / ou que le contenu de son référentiel est appelé à évoluer.</p></div>",
            default_description_qualite="<div class='tip'><p><strong class='main'>Indicateurs de résultats</strong></p><p>Donner une information chiffrée sur le niveau de performance et d’accomplissement de la prestation.</p><ul class='examples'><li>Taux de satisfaction des stagiaires.</li><li>Nombre de stagiaires.</li><li>Taux et causes des abandons.</li><li>Taux de retour des enquêtes.</li><li>Taux d'interruption en cours de prestation.</li><li>Taux de rupture des contrats d’alternance.</li><li>Taux d'insertion dans l'emploi.</li></ul></div>",
        )



        return super(Programme,self).default_get(fields)


class Objectif(models.Model):
    _name = 'mcmacademy.programme.objectif'

    name=fields.Char('Objectif')
    sequence=fields.Integer('',default=1)
    programme_id=fields.Many2one('mcmacademy.programme')

class ClientPotentiel(models.Model):
    _name = 'mcmacademy.programme.clientpotentiel'

    name=fields.Char('Client')
    sequence=fields.Integer('',default=1)
    programme_id=fields.Many2one('mcmacademy.programme')

class Prerequis(models.Model):
    _name = 'mcmacademy.programme.prerequis'

    name=fields.Char('Pré-Requis')
    sequence=fields.Integer('',default=1)
    programme_id=fields.Many2one('mcmacademy.programme')

class SuiviExecution(models.Model):
    _name = 'mcmacademy.suiviexecution'

    name=fields.Char('Nom')
    sequence=fields.Integer('',default=1)
    programme_id=fields.Many2one('mcmacademy.programme')

class Ressources(models.Model):
    _name = 'mcmacademy.ressources'

    name=fields.Char('Nom')
    sequence=fields.Integer('',default=1)
    programme_id = fields.Many2one('mcmacademy.programme')


