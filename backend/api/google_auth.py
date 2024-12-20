from google.oauth2 import service_account
from settings import AUTH_DIR
import os


class GoogleDriveAuth:
    #If modifying these scopes, delete the file token.json.
    SCOPES : list[str] = ["https://www.googleapis.com/auth/drive.readonly"]
    CREDENTIALS_PATH : str = os.path.join(AUTH_DIR, 'google_cloud_credentials.json')

    #Autenticación con cuenta de servicio
    @classmethod
    def authenticate(cls):
        credentials : service_account.Credentials = service_account.Credentials.from_service_account_file(cls.CREDENTIALS_PATH,scopes=cls.SCOPES)

        return credentials