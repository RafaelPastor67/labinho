'''Arquivo onde está definida as classes que serão as tabelas do banco'''

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select
from flask_login import UserMixin
from app import db 
from app import login

### TABELA USER
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True , nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    cargo: Mapped[str] = mapped_column(nullable=False)
    remember: Mapped[bool] = mapped_column(default=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

### TABELA CARDAPIO
class Cardapio(db.Model):
    __tablename__ = 'cardapio'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID único
    nome = db.Column(db.String(100), nullable=False)  # Nome do prato
    descricao = db.Column(db.Text, nullable=True)  # Descrição do produto
    valor = db.Column(db.Numeric(10, 2), nullable=False)  # Valor do prato
    imagem = db.Column(db.String(255), nullable=True)  # URL da imagem
    tipo = db.Column(db.Enum('Porção', 'Individual', 'Bebida', name='tipo_enum'), nullable=False)  # Tipo do item


### TABELA CARRINHO
class Carrinho(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('cardapio.id'), nullable=False) 
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    data_pedido = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

