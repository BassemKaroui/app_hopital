from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  # orm = object relational mapping


# Chemin de la base de données
SQLACHEMY_DATABASE_URL = "sqlite:///instance/hopital.sqlite"


# Moteur SQL se connectant à la base de donnée
engine = create_engine(
    SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Création d'une session avec une portée globale
# SessionSQLGlobale sera accessible partout dans le code
SessionSQLAlchemyGlobale = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# La nouvelle classe de base sera dotée d'une métaclasse qui produit les objets Table appropriés
# et effectue les appels mapper() appropriés en fonction des informations fournies de manière déclarative
# dans la classe et dans toute sous-classe de la classe.
# C'est le générateur de Mapping : BDD <-> Objets et sous objets
Base = declarative_base()
