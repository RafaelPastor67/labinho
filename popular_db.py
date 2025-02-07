import csv
from app import app, db, User, Cardapio  # Importe seu app e modelos

#Popular Cardapio
with app.app_context():
    with open('app\\tabelas\\cardapio.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            prato_existente = Cardapio.query.filter_by(nome=row['nome']).first()

            if not prato_existente:
                prato = Cardapio(
                    nome =row['nome'],
                    descricao =row['descricao'],
                    valor =row['valor'],
                    imagem =row['imagem'],
                    tipo = row['tipo']
                )
                db.session.add(prato)

        db.session.commit()

    print('Banco de dados populados com sucesso!')

#Popular usuários
with app.app_context():
    with open('app\\tabelas\\users.csv', mode='r',  encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:

            user_existe = User.query.filter_by(username=row['username']).first()

            if not user_existe:
                user = User(
                    email =row['email'],
                    cargo =row['cargo'],
                    username =row['username'],
                    password =row['password'],
                    remember = 0 
                )
                db.session.add(user)
        db.session.commit()

    print('Banco de dados populados com sucesso!')