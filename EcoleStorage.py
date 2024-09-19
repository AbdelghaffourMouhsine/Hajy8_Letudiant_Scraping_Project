import csv

class EcoleStorage:
    def __init__(self, file_path="results/ecoles_results_1"):
        self.file_path = f"{file_path}.csv"
        self.fieldnames = ['ecole_name','ecole_more_inf_url','ecole_voir_la_fiche_url','ecole_title','ecole_ville','ecole_phone','ecole_email','ecole_region', 'ecole_nb_etudiants','ecole_web_site_url','ecole_address','ecole_comment_contacter']
        
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8-sig')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        
        # Check if the file is empty, then write the header
        if self.file.tell() == 0:
            self.writer.writeheader()

    def insert_ecole(self, ecole):
        data = {
            'ecole_name' : ecole.ecole_name, 
            'ecole_more_inf_url' : ecole.ecole_more_inf_url, 
            'ecole_voir_la_fiche_url' : ecole.ecole_voir_la_fiche_url,
            'ecole_title' : ecole.ecole_title, 
            'ecole_ville' : ecole.ecole_ville, 
            'ecole_phone' : ecole.ecole_phone,
            'ecole_email' : ecole.ecole_email, 
            'ecole_region' : ecole.ecole_region, 
            'ecole_nb_etudiants' : ecole.ecole_nb_etudiants,
            'ecole_web_site_url' : ecole.ecole_web_site_url,
            'ecole_address' : ecole.ecole_address,
            'ecole_comment_contacter' : ecole.ecole_comment_contacter
        }
        self.writer.writerow(data)
        
    def insert_ecoles(self, ecoles):
        for ecole in ecoles:
            self.insert_ecole(ecole)
            
    def close_file(self):
        self.file.close()