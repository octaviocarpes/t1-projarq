import datetime
from model.certificates_database import CertificatesDB


class CertificatesManager:
    def __init__(self):
        self.certificates = {}
        self.certificates_db = CertificatesDB()

    def get_certificate(self, username):
        if username in self.certificates:
            return self.certificates[username]
        else:
            certificate = self.certificates_db.get_certificate(username)
            if certificate is None:
                return None

            self.certificates[username] = certificate

            return certificate

    def get_certificates(self):
        return self.certificates_db.get_certificates()

    def generate_certificate(self, username, team_name):
        date = datetime.datetime.now()
        date_string = str(date.strftime('%d/%m/%Y %H:%M'))
        return self.certificates_db.generate_certificate(username, team_name, date_string)
