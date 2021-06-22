# DAO = Data Access Object

from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, DateTime, Date
# from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime

# IMPORT DU MAPPER (Dans la litterature vous trouverez le nom de Base)
from .database import Base


class ConsultationUtilisateur(Base):
    __tablename__ = 'consultation_utilisateur',
    id_consultation = Column(Integer, ForeignKey(
        'consultation.id'), primary_key=True)
    id_utilisation = Column(Integer, ForeignKey(
        'utilisateur.id'), primary_key=True)
    role = Column(Integer)
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    consultation = relationship('Consultation', back_populates="soignants")
    utilisateur = relationship('Utilisateur', back_populates="consultations")


class Utilisateur(Base):
    __tablename__ = "utilisateur"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    role = Column(Integer)
    email = Column(String)
    password = Column(String)
    consultations = relationship(
        "ConsultationUtilisateur", back_populates='utilisateur')


class DossierPatient(Base):
    __tablename__ = "dossier_patient"
    id = Column(Integer, primary_key=True)
    ssn = Column(String)  # social security number
    nom = Column(String)
    prenom = Column(String)
    date_naissance = Column(Date)
    age = Column(Integer)
    sexe = Column(String)
    adresse = relationship('Adresse', backref='dossier_patient',
                           lazy=True, cascade="all, delete, delete-orphan")
    consultation = relationship(
        'Consultation', backref='dossier_patient', lazy=True, cascade="all, delete, delete-orphan")


consultation_acte_medical = Table('consultation_acte_medical', Base.metadata, Column(
    'consultation.id', Integer, ForeignKey('consultation.id')), Column('acte_medical.id', Integer, ForeignKey('acte_medical.id')))


class ModeTransport(Base):
    __tablename__ = 'mode_transport'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)
    consultation = relationship(
        'Consultation', backref='mode_transport', lazy=True)


class MotifRecours(Base):
    __tablename__ = "motif_recours"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    consultation = relationship(
        'Consultation', backref='motif_recours', lazy=True)


class Consultation(Base):
    __tablename__ = "consultation"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, default="Consultation urgences")
    status = Column(String, default="ouvert")
    date_arrivee = Column(DateTime, default=datetime.datetime.utcnow)
    anamnese = Column(String(1000))
    gravite = Column(String)
    id_motif = Column(Integer, ForeignKey('motif_recours.id'))
    id_transport = Column(Integer, ForeignKey('mode_transport.id'))
    id_dossier_patient = Column(Integer, ForeignKey('dossier_patient.id'))
    acte_medicaux = relationship(
        "ActeMedical", secondary=consultation_acte_medical, backref="consultation")
    soignants = relationship("ConsultationUtilisateur",
                             back_populates="consultation")


class Adresse(Base):
    __tablename__ = 'adresse'
    id = Column(Integer, primary_key=True)
    num = Column(Integer)
    rue = Column(String)
    ville = Column(String)
    region = Column(String)
    code_postal = Column(Integer)
    id_dossier_patient = Column(Integer, ForeignKey('dossier_patient.id'))


class ActeMedical(Base):
    __tablename__ = 'acte_medical'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    description = Column(String)
    tarification = Column(Float)
