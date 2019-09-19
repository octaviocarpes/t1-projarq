from model.certificate import Certificate
from model.certificates_database import CertificatesDB


class CertificatesManager:
    def __init__(self):
        self.certificates = {}
        self.certificates_db = CertificatesDB()

