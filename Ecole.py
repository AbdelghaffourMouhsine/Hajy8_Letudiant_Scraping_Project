class Ecole:
    def __init__(self):
        self.ecole_name = None
        self.ecole_more_inf_url = None
        self.ecole_voir_la_fiche_url = None
        self.ecole_title = None
        self.ecole_ville = None
        self.ecole_phone = None
        self.ecole_email = None
        self.ecole_region = None
        self.ecole_nb_etudiants = None
        self.ecole_web_site_url = None
        self.ecole_address = None
        self.ecole_comment_contacter = None
        
    def init_from_dic(self, dic):
        self.ecole_name = dic['ecole_name']
        self.ecole_more_inf_url = dic['ecole_more_inf_url']
        self.ecole_voir_la_fiche_url = dic['ecole_voir_la_fiche_url']
        self.ecole_title = dic['ecole_title']
        self.ecole_ville = dic['ecole_ville']
        self.ecole_phone = dic['ecole_phone']
        self.ecole_email = dic['ecole_email']
        self.ecole_region = dic['ecole_region']
        self.ecole_nb_etudiants = dic['ecole_nb_etudiants']
        self.ecole_web_site_url = dic['ecole_web_site_url']
        self.ecole_address = dic['ecole_address']
        self.ecole_comment_contacter = dic['ecole_comment_contacter']
        
    def __str__(self):
        return f'ecole_name = {self.ecole_name}\necole_more_inf_url = {self.ecole_more_inf_url}\necole_voir_la_fiche_url = {self.ecole_voir_la_fiche_url}\necole_title = {self.ecole_title}\necole_ville = {self.ecole_ville}\necole_phone = {self.ecole_phone}\necole_email = {self.ecole_email}\necole_region = {self.ecole_region}\necole_nb_etudiants = {self.ecole_nb_etudiants}\necole_web_site_url = {self.ecole_web_site_url}\necole_address = {self.ecole_address}\necole_comment_contacter = {self.ecole_comment_contacter}\n'
