# Flask == 1.0.2
# Flask-Login == 0.4.1
# Flask-Session == 0.3.1
# Flask_SocketIO
# itsdangerous == 1.1.0
# Jinja2 == 2.10
# MarkupSafe == 1.1.0
# python-engineio
# python-socketio
# six == 1.11.0
# Werkzeug == 0.14.1
#
# set FLASK_APP=respirateur
# set FLASK_ENV=development
# set FLASK_DEBUG=1
# flask run

# ---------------------------------
# LIBRAIRIES
# ---------------------------------

import datetime

# FLASK et OS
import sys

from flask import Flask
import os
from flask import render_template

# JSON
import json
from flask import jsonify

# COMMUNICATION
from flask import request

# ---------------------------------
# MODELES
# ---------------------------------


# --------------------------------
# SECURISATION
# --------------------------------


# ---------------------------------
# BASES DE DONNEES
# ---------------------------------


# ---------------------------------
# SOCKET THREADING RESPIRATEUR
# ---------------------------------
from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
import numpy as np
import random


# ---------------------------------------------------------------------
# INITIALISATION DE L'APPLICATION
# ----------------------------------------------------------------------

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# Instanciation du Framework Flask -> Application
app = Flask(__name__)

# ---------------------------------
# SOCKET THREADING RESPIRATEUR
# ---------------------------------
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
count = 0

# On s'assure que le fichier d'instance est bien créé (Sinon pas de possibilité de créer la BDD)
try:
    os.makedirs(app.instance_path)
    print("Repertoire cree")  # uniquement aprés rechargement de la page
except OSError:
    pass

# Securisation API : On créé un utilisateur et on récupere son Token
# Ce token et généralement stocké en base de donnée pour chacun des utilisateurs
# Le token doit être communiqué au client pour qu'il puisse l'utiliser dans son application

# -------------------------------------------------
# SECURISATION DE L'APPLICATION WEB
# -------------------------------------------------

# Securisation de l'application
app.config.from_mapping(
    # Clé secrète pour la session
    # A noter que cette clé secrete peut aussi etre utilisée pour les apis.
    SECRET_KEY='hopital_app'
)

# ---------------------------------------------------------------------
# VUES (PAGES HTML)
# ----------------------------------------------------------------------

# Creation d'une premiere route


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/respirateur')
def respirateur():
    return render_template('respirateur.html', async_mode=socketio.async_mode)


# ---------------------------------------------------------------------
# SOCKET THREADING RESPIRATEUR
# ----------------------------------------------------------------------

def background_thread():
    while True:
        socketio.sleep(0.1)
        x = np.arange(0, 2*np.pi+np.pi/10, 2*np.pi/20)
        y = np.sin(x) + (random.random()-0.5)*0.3
        global count
        count += 1
        socketio.emit('my_response', {'data': y[count % 20], 'count': count})


@socketio.event
def connect():
    global thread
    with thread_lock:
        thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


# ---------------------------------------------------------------------
# APIs
# ----------------------------------------------------------------------


if __name__ == '__main__':
    socketio.run(app)
