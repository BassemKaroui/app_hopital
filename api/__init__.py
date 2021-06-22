# set FLASK_APP=api
# set FLASK_ENV=development
# set FLASK_DEBUG=1
# flask run

from sqlalchemy import create_engine
import pandas as pd
import datetime
import numpy as np
import numpy as np

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

SQLACHEMY_DATABASE_URL = "sqlite:///instance/hopital.sqlite"
engine = create_engine(
    SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def create_app():

    app = Flask(__name__)

    # -------------------------------
    # Vues
    # -------------------------------

    @app.route('/')
    def accueil():
        return render_template('index.html')

    # -------------------------------
    # API
    # -------------------------------

    @app.route('/api/data')
    def data():

        response = {}
        timestamp = request.json
        timestamp = pd.Timestamp(timestamp['timestamp'])
        date = pd.Period(timestamp, freq='D')

        consultation_1 = pd.read_sql_query(
            f'select id, date_arrivee from consultation where date_arrivee >= date("{date-7}") and date_arrivee < date("{date-6}")', con=engine, index_col='date_arrivee', parse_dates=['date_arrivee'])
        consultation_2 = pd.read_sql_query(
            f'select id, date_arrivee from consultation where date_arrivee >= date("{date-14}") and date_arrivee < date("{date-13}")', con=engine, index_col='date_arrivee', parse_dates=['date_arrivee'])
        consultation_3 = pd.read_sql_query(
            f'select id, date_arrivee from consultation where date_arrivee >= date("{date-21}") and date_arrivee < date("{date-20}")', con=engine, index_col='date_arrivee', parse_dates=['date_arrivee'])

        consultation_1_hour = consultation_1.groupby(lambda x: x.hour)[
            'id'].count()
        consultation_2_hour = consultation_2.groupby(lambda x: x.hour)[
            'id'].count()
        consultation_3_hour = consultation_3.groupby(lambda x: x.hour)[
            'id'].count()

        consultation_mean_hour = (
            consultation_1_hour + consultation_2_hour + consultation_3_hour)/3

        response['consultation_mean_hour'] = consultation_mean_hour.to_dict()

        consultation_utilisateur_1 = pd.read_sql_query(f'select * from "(\'consultation_utilisateur\',)" where role==1 and id_consultation in {tuple(consultation_1.id.to_list())}',
                                                       con=engine,
                                                       parse_dates=['date_debut', 'date_fin'])
        consultation_utilisateur_2 = pd.read_sql_query(f'select * from "(\'consultation_utilisateur\',)" where role==1 and id_consultation in {tuple(consultation_2.id.to_list())}',
                                                       con=engine,
                                                       parse_dates=['date_debut', 'date_fin'])
        consultation_utilisateur_3 = pd.read_sql_query(f'select * from "(\'consultation_utilisateur\',)" where role==1 and id_consultation in {tuple(consultation_3.id.to_list())}',
                                                       con=engine,
                                                       parse_dates=['date_debut', 'date_fin'])

        df1 = consultation_utilisateur_1.merge(
            consultation_1.reset_index(), left_on='id_consultation', right_on='id')
        df2 = consultation_utilisateur_2.merge(
            consultation_2.reset_index(), left_on='id_consultation', right_on='id')
        df3 = consultation_utilisateur_3.merge(
            consultation_3.reset_index(), left_on='id_consultation', right_on='id')

        df1_infirmier = df1.groupby(['id_consultation']).agg(
            {'date_debut': np.min, 'date_arrivee': np.min})
        df2_infirmier = df2.groupby(['id_consultation']).agg(
            {'date_debut': np.min, 'date_arrivee': np.min})
        df3_infirmier = df3.groupby(['id_consultation']).agg(
            {'date_debut': np.min, 'date_arrivee': np.min})

        df1_infirmier['duree'] = df1_infirmier.apply(lambda x: (
            x['date_debut'] - x['date_arrivee']).seconds/60, axis=1)
        df2_infirmier['duree'] = df2_infirmier.apply(lambda x: (
            x['date_debut'] - x['date_arrivee']).seconds/60, axis=1)
        df3_infirmier['duree'] = df3_infirmier.apply(lambda x: (
            x['date_debut'] - x['date_arrivee']).seconds/60, axis=1)

        df1_infirmier = df1_infirmier.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_voir_infirmier=pd.NamedAgg(column='duree', aggfunc=np.mean))
        df2_infirmier = df2_infirmier.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_voir_infirmier=pd.NamedAgg(column='duree', aggfunc=np.mean))
        df3_infirmier = df3_infirmier.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_voir_infirmier=pd.NamedAgg(column='duree', aggfunc=np.mean))

        df_infirmier = (df1_infirmier+df2_infirmier+df3_infirmier)/3

        response.update(df_infirmier.to_dict())

        consultation_utilisateur_1_med = pd.read_sql_query(f'select * from "(\'consultation_utilisateur\',)" where role==2 and id_consultation in {tuple(consultation_1.id.to_list())}',
                                                           con=engine,
                                                           parse_dates=['date_debut', 'date_fin'])
        consultation_utilisateur_2_med = pd.read_sql_query(f'select * from "(\'consultation_utilisateur\',)" where role==2 and id_consultation in {tuple(consultation_2.id.to_list())}',
                                                           con=engine,
                                                           parse_dates=['date_debut', 'date_fin'])
        consultation_utilisateur_3_med = pd.read_sql_query(f'select * from "(\'consultation_utilisateur\',)" where role==2 and id_consultation in {tuple(consultation_3.id.to_list())}',
                                                           con=engine,
                                                           parse_dates=['date_debut', 'date_fin'])

        df1_med = consultation_utilisateur_1_med.merge(
            consultation_1.reset_index(), left_on='id_consultation', right_on='id')
        df2_med = consultation_utilisateur_2_med.merge(
            consultation_2.reset_index(), left_on='id_consultation', right_on='id')
        df3_med = consultation_utilisateur_3_med.merge(
            consultation_3.reset_index(), left_on='id_consultation', right_on='id')

        df1_med = df1_med.groupby(['id_consultation']).agg(
            {'date_debut': np.min, 'date_fin': np.max, 'date_arrivee': np.min})
        df2_med = df2_med.groupby(['id_consultation']).agg(
            {'date_debut': np.min, 'date_fin': np.max, 'date_arrivee': np.min})
        df3_med = df3_med.groupby(['id_consultation']).agg(
            {'date_debut': np.min, 'date_fin': np.max, 'date_arrivee': np.min})

        df1_med['duree_debut'] = df1_med.apply(lambda x: (
            x['date_debut'] - x['date_arrivee']).seconds/60, axis=1)
        df2_med['duree_debut'] = df2_med.apply(lambda x: (
            x['date_debut'] - x['date_arrivee']).seconds/60, axis=1)
        df3_med['duree_debut'] = df3_med.apply(lambda x: (
            x['date_debut'] - x['date_arrivee']).seconds/60, axis=1)
        df1_med['duree_fin'] = df1_med.apply(lambda x: (
            x['date_fin'] - x['date_arrivee']).seconds/60, axis=1)
        df2_med['duree_fin'] = df2_med.apply(lambda x: (
            x['date_fin'] - x['date_arrivee']).seconds/60, axis=1)
        df3_med['duree_fin'] = df3_med.apply(lambda x: (
            x['date_fin'] - x['date_arrivee']).seconds/60, axis=1)

        df1_med_debut = df1_med.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_voir_med=pd.NamedAgg(column='duree_debut', aggfunc=np.mean))
        df2_med_debut = df2_med.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_voir_med=pd.NamedAgg(column='duree_debut', aggfunc=np.mean))
        df3_med_debut = df3_med.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_voir_med=pd.NamedAgg(column='duree_debut', aggfunc=np.mean))

        df_med = (df1_med_debut+df2_med_debut+df3_med_debut)/3

        response.update(df_med.to_dict())

        df1_duree_totale = df1_med.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_totale=pd.NamedAgg(column='duree_fin', aggfunc=np.mean))
        df2_duree_totale = df2_med.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_totale=pd.NamedAgg(column='duree_fin', aggfunc=np.mean))
        df3_duree_totale = df3_med.set_index('date_arrivee').groupby(lambda x: x.hour).agg(
            duree_totale=pd.NamedAgg(column='duree_fin', aggfunc=np.mean))

        df_duree_totale = (
            df1_duree_totale+df2_duree_totale+df3_duree_totale)/3

        response.update(df_duree_totale.to_dict())

        response["duree_voir_infirmier_T"] = float(
            df_infirmier.iloc[timestamp.hour])
        response["duree_voir_med_T"] = float(df_med.iloc[timestamp.hour])
        response["duree_totale_T"] = float(
            df_duree_totale.iloc[timestamp.hour])

        return jsonify(response)

    return app
