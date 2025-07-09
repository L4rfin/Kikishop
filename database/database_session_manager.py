
from sqlalchemy.orm import sessionmaker

from database.database_connection import engine


class SessionManager:
    # Tworzymy fabrykę sesji
    Session = sessionmaker(bind=engine)

    def __init__(self):
        """ Inicjalizacja nowej sesji """
        self.session = self.Session()

    def close(self):
        """ Zamknięcie sesji """
        self.session.close()

    def commit(self):
        """ Zatwierdzenie zmian w bazie """
        self.session.commit()

    def rollback(self):
        """ Cofnięcie zmian w razie błędu """
        self.session.rollback()