''' Responsável pela inicialização da aplicação '''
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv


app = Flask(__name__) #inicia a aplicação
app.config['DEBUG'] = True

if __name__ == "__main__":
    app.run()

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

login = LoginManager(app)
login.login_view = 'login' 

#Configurando o banco
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite+pysqlite:///labinho.db"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Importações dos módulos
from app import routes
from app.models import models

with app.app_context():
    from app.models.models import Cardapio, User, Carrinho
    from datetime import datetime
    from sqlalchemy import select
    from app import db

