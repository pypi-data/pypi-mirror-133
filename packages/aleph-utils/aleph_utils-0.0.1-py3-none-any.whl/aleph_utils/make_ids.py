from slugify import slugify
import datetime
import numpy as np

def make_person_id(nom=None, prenom=None, date_naissance=None):
    """Fonction pour créer un ID de Person
    @param: nom: requis - nom de famille patronymique (pas le nom d'usage)
    @param: prenom: optionnel - premier prenom
    @param: date_naissance: optionnel - au format yyyy-mm ou yyyy-mm-dd

    Pas besoin de formatter nom et prenom, la fonction slugigy les deux: Étienne --> etienne
    Si vous n'avez pas le prénom ou la date de naissance, envoyez n'importe quoi qui évalue à False ex: "", None, 0
    Le cas échéant, ce champ sera remplacé par une chaine aléatoire

    Retourne nom_prenom_annee_mois
    """
    assert nom, "Le nom de la personne est requis pour créer l'ID"
    if not prenom:
        prenom = str(np.random.randint(10000000))
    if not date_naissance:
        naissance_id = str(np.random.randint(10000000))
    else:
        nb_tirets = len(date_naissance.split("-")) - 1
        if nb_tirets == 1:
            birthDate = datetime.datetime.strptime(date_naissance, "%Y-%m")
        elif nb_tirets == 2:
            birthDate = datetime.datetime.strptime(date_naissance, "%Y-%m-%d")
        else:
            raise AssertionError("La date de naissance n'est pas au format yyyy-mm ou yyyy-mm-dd")
        naissance_id = "{}_{}".format(birthDate.year, birthDate.month)
    id_ = "{}_{}_{}".format(slugify(nom), slugify(prenom), slugify(naissance_id))
    return id_


def make_company_id(siren=None):
    """
    Fonction pour créer un ID de Company
    @param: siren: requis - numéro de SIREN à 9 chiffres

    Retourne siren
    """
    assert siren and len(siren) == 9, "Un siren doit avoir 9 caractères"
    return siren


def make_organization_id(id_numerique=None, nom=None):
    """
        Fonction pour créer un ID de Organization
        @param: id_numerique: requis - le numéro de RNA quand il existe

        Retourne id_numerique (slugifié) s'il existe sinon le nom slugifié
        """
    assert id_numerique or nom, "Il faut fournir au moins un identifiant"
    if id_numerique:
        return slugify(id_numerique)
    return slugify(nom)

# def make_link_id(type_link=None):