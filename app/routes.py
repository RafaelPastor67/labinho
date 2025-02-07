''' Responsável pela criação das rotas de URL na aplicação '''

from flask import render_template, flash, session
from flask import request, redirect, url_for, render_template
from flask_login import login_required, login_user
from app import app
from app import db
from app import alquimias 
from app.models.models import Cardapio, Carrinho
from sqlalchemy import func

### --- INDEX --- ###

@app.route('/')
@app.route('/index')
def index():
    '''
    Renderiza a página index do site
    '''
    if 'username' in session:  # Verifica se o usuário está logado
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)  # Obtém o cargo do usuário
        user = {'username': username, 'cargo': cargo}  # Passa o cargo para o template
    else:
        user = None
        cargo = 'cliente'

    pagina = 'LABINHO PIZZARIA E RESTAURANTE'
    texto='A melhor parmegiana de Itabira!'
    fundo='background_image.png' 

    return render_template(
        'index.html', 
        title='Home', 
        fundo=fundo,
        pagina=pagina,
        texto=texto,
        user=user,
        cargo = cargo
    )


### --- LOGIN --- ###

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Renderiza a página de login do site para logar um usuário
    '''
    if 'username' in session: #realiza logout caso tenha algum usuário na sessão
        session.pop('username', None)  
        session.pop('cargo', None)
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password'].lower()

        if not alquimias.user_exists(username):
            flash('Usuário não encontrado')
            return redirect(url_for('login'))
        
        elif alquimias.validate_user_password(username, password):
            flash("Login bem-sucedido!")
            session['username'] = username
            session['cargo'] = alquimias.resgatar_cargo(username)  # Guarda o cargo na sessão

            return redirect(url_for('index'))  # Removido username=username, pois já está na sessão
        
        else:
            flash("Usuário ou senha inválidos")
            return redirect(url_for('login'))
    
    return render_template('login.html', title="Login")



###  --- REGISTRAR --- ###

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    '''
    Renderiza a página de registro do site para criar um novo usuário
    '''
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password'].lower()
        password2 = request.form['password2'].lower()

        if alquimias.user_exists(username):
            flash("Usuário já existe!")
            return redirect(url_for('login'))
        elif password != password2:
            flash("Senhas estão diferentes")
            return redirect(url_for('registro'))
        else:
            username = username
            email = request.form['email'].lower()
            password = request.form['password'].lower()

            alquimias.create_user(username, password, email)
            return redirect(url_for(f"login", username=username ))
        
    else:
        return render_template('registro.html', title=registro)

    
### --- CARGO --- ###
@app.route('/cadastro/user', methods=['GET', 'POST'])
def alterarCargo(): 
    '''
    Renderiza a página apenas para gerentes alterarem o cargo de algum usuário
    ''' 
    if 'username' not in session:
            user = None
            return redirect(url_for('index'))

    if 'username' in session:
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)
        user = {'username': username, 'cargo': cargo}

        if user['cargo'].lower() != 'gerente' and  user['cargo'].lower() != 'funcionario':
            return redirect(url_for('index'))

    if request.method == 'POST':
        adm = session['username']
        usuario = request.form['nome'].lower()
        novo_cargo = request.form['cargo']
        senha_adm = request.form['senha'].lower()

        if not all([adm, usuario, novo_cargo, senha_adm]):
            flash('Todos os campos são obrigatórios.')
            return redirect(url_for('alterarCargo'))

        resultado = alquimias.validar_adm_password(adm, senha_adm)

        if resultado:
            valido, mensagem = alquimias.atualiza_cargo(usuario, novo_cargo)

            if valido:
                flash(mensagem)
                return redirect(url_for('index'))
            else:
                flash(mensagem)
                return redirect(url_for('alterarCargo'))
        else:
            flash(f'senha inválida para {adm}')
            return redirect(url_for('alterarCargo'))

    return render_template('mudar_cargo.html', title='Atualização', user=user)



### --- EVENTOS --- ### 

@app.route('/eventos')
def pag_eventos():
    '''
    Renderiza a página do eventos do restaurante  
    '''
    if 'username' in session:  
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)  # Obtém o cargo do usuário
        user = {'username': username, 'cargo': cargo}  # Passa o cargo para o template
    else:
        user = None
        cargo = 'cliente'

    pagina = 'EVENTOS'
    texto = 'Agende um evento em nosso restaurante'
    fundo='festas-salao-transformed.png' 

    return render_template('eventos.html', title='Eventos', pagina=pagina, fundo=fundo, texto=texto, user=user)

### --- CARDAPIO --- ###

@app.route('/cardapio')
def cardapio():
    '''
    Renderiza a página do cardapio do restaurante  
    '''
    if 'username' in session:  # Verifica se o usuário está logado
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)  # Obtém o cargo do usuário
        user = {'username': username, 'cargo': cargo}  # Passa o cargo para o template
    else:
        user = None
        cargo = 'cliente'

    individuais = Cardapio.query.filter_by(tipo="Individual").limit(4).all()
    porcoes = Cardapio.query.filter_by(tipo="Porção").limit(4).all()
    bebidas = Cardapio.query.filter_by(tipo="Bebida").limit(4).all()

    pagina = 'MENU'
    texto = 'Conheça nossos pratos'
    fundo='background_image.png' 

    return render_template('cardapio.html', title='Menu', pagina=pagina, texto=texto, fundo=fundo, individuais=individuais, porcoes=porcoes, bebidas=bebidas, user=user)

@app.route('/cardapio/<tipo>')
def cardapioCompleto(tipo):
    '''
    Renderiza uma página de cardapio com um tipo específico entre bebidas, porções e individuais
    '''
    if 'username' in session:  # Verifica se o usuário está logado
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)  # Obtém o cargo do usuário
        user = {'username': username, 'cargo': cargo}  # Passa o cargo para o template
    else:
        user = None
        cargo = 'cliente'

    cardapio = Cardapio.query.filter_by(tipo=tipo).all()

    pagina = tipo.upper()
    texto = 'Conheça mais opções de pratos'
    fundo='background_image.png' 

    return render_template('cardapio_completo.html', pagina=pagina, fundo=fundo, texto=texto, title=tipo, user=user, cardapio=cardapio)

@app.route('/cadastro/cardapio', methods=['GET', 'POST'])
def registroCardapio():   
    '''
    Essa URL renderiza um formulário para cadastrar um novo produto
    '''
    if 'username' not in session:
            user = None
            return redirect(url_for('index'))

    if 'username' in session:
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)
        user = {'username': username, 'cargo': cargo}

        if user['cargo'].lower() != 'gerente' and  user['cargo'].lower() != 'funcionário':
            return redirect(url_for('index'))

    if request.method == 'POST':
        valido, mensagem = alquimias.valida_prato(request.form)
        
        if valido:
            nome = request.form['nome'].capitalize()
            tipo = request.form['tipo'].capitalize() 
            valor = request.form['valor'].capitalize() 
            descricao = request.form['descricao'].capitalize() 
            imagem = request.form['imagem'].capitalize()

            alquimias.create_prato(nome, tipo, valor, descricao, imagem)
            flash(f'Prato registrado com sucesso!')
            return redirect(url_for('cardapio'))
        else:
            flash(mensagem)

    return render_template('registrar_prato.html', title='Registro', user=user)

@app.route('/excluir_prato/<int:id>', methods=['POST'])
def excluirPrato(id):
    '''
    Essa URL resgata o id de algum prato no banco de dados e acessa uma query para exclui-lo
    '''
    if 'username' not in session:
            user = None
            return redirect(url_for('index'))

    if 'username' in session:
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)
        user = {'username': username, 'cargo': cargo}

        if user['cargo'].lower() != 'gerente' and  user['cargo'].lower() != 'funcionario':
            return redirect(url_for('index'))
        
    valido, mensagem = alquimias.excluir_prato(id)

    if valido:
        flash(mensagem)
        return redirect(url_for('index'))
    else:
        flash(mensagem)
        return redirect(url_for('cardapio'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editarPrato(id):
    '''
    Essa URL resgata o id de algum prato no banco de dados do cardapio e acessa uma query para edita-lo
    '''
    # Verifica se o usuário está logado na sessão
    if 'username' not in session:
        return redirect(url_for('index'))  # Se não estiver, redireciona para a página principal

    username = session['username']
    cargo = alquimias.resgatar_cargo(username)
    user = {'username': username, 'cargo': cargo}

    # Verifica se o usuário tem permissão (cargo 'gerente' ou 'funcionario')
    if user['cargo'].lower() not in ['gerente', 'funcionario']:
        return redirect(url_for('index'))  # Redireciona se o usuário não tiver permissão

    if request.method == 'POST':
        senha_adm = request.form.get('senha')  
        nome = request.form.get('nome', '').strip().capitalize()  
        tipo = request.form.get('tipo', '').strip().capitalize()
        valor = request.form.get('valor', '').strip()  
        descricao = request.form.get('descricao', '').strip().capitalize()
        imagem = request.form.get('imagem', '').strip().capitalize()

        # Valida se os campos obrigatórios estão presentes
        if not nome or not tipo or not valor or not descricao or not imagem or not senha_adm:
            flash('Todos os campos devem ser preenchidos!', 'error')
            return redirect(url_for('editarPrato', id=id))

        # Valida a senha do administrador
        adm = session['username']
        resultado = alquimias.validar_adm_password(adm, senha_adm.lower())

        if resultado:
            # Se a senha for válida, tenta editar o prato
            try:
                valor = float(valor)  # Tenta converter o valor para float
            except ValueError:
                flash('Valor inválido!', 'error')
                return redirect(url_for('editarPrato', id=id))

            # Chama a função para editar o prato no banco de dados
            query = alquimias.editar_prato(id, nome, tipo, valor, descricao, imagem)
            if query:
                flash(f'Prato "{nome}" editado com sucesso!')
                return redirect(url_for('cardapio'))
            else:
                flash('Falha ao editar prato no banco de dados', 'error')
                return redirect(url_for('cardapio'))
        else:
            flash('Senha de administrador incorreta', 'error')
            return redirect(url_for('cardapio'))

    # Resgata as informações atuais do prato
    res = alquimias.info_pratos(id)

    if res:
        # Se o prato for encontrado, renderiza a página de edição com os dados atuais
        return render_template('editar_prato.html', 
                               title='Editar', 
                               nome=res[0], 
                               descricao=res[1], 
                               tipo=res[2], 
                               valor=res[3], 
                               imagem=res[4], 
                               user=user)
    else:
        flash('Prato não encontrado', 'error')
        return redirect(url_for('index'))  # Se o prato não for encontrado, redireciona para o index


### --- CARRINHO --- ###

@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    '''
    Renderiza a página com o carrinho do usuário ao acessar a tabela relação entre user e cardapio
    '''
    if 'username' in session:  # Verifica se o usuário está logado
        username = session['username']
        cargo = alquimias.resgatar_cargo(username)
        user = {'username': username, 'cargo': cargo}
    else:
        return redirect(url_for('login'))

    id_user = alquimias.resgatar_id(username)

    #JOIN entre as tabelas Carrinho e Cardapio para buscar as informações do produto no carrinho
    carrinho = db.session.query(Carrinho, Cardapio.descricao, Cardapio.nome, Cardapio.imagem) \
        .join(Cardapio, Carrinho.produto_id == Cardapio.id) \
        .filter(Carrinho.user_id == id_user) \
        .all()

    # Consulta para obter o valor total somado de todos os itens no carrinho
    total = db.session.query(func.sum(Carrinho.quantidade * Cardapio.valor)) \
        .join(Cardapio, Carrinho.produto_id == Cardapio.id) \
        .filter(Carrinho.user_id == id_user) \
        .scalar()

    if total is None:
        total = 0

    return render_template(
        'carrinho.html', 
        title='Carrinho', 
        user=user,
        carrinho=carrinho,
        total=total
    )

@app.route('/adicionar/<int:id>', methods=['POST'])
def adicionarPrato(id):
    '''
    URL acionado por um botão para inserir o produto no carrinho do usuário, desse modo, ela precisa do id do produto e do usuário da sessão
    '''
    if 'username' not in session:
        user = None
        return redirect(url_for('login'))
    
    usuario = session['username']
    id_user = alquimias.resgatar_id(usuario)

    valido, mensagem = alquimias.adicionar_carrinho(id_user, id, quantidade=1)
    
    if valido:
        flash(mensagem)
        return redirect(url_for('cardapio'))
    else:
        flash(mensagem)
        return redirect(url_for('cardapio'))

@app.route('/excluir_pedido/<int:id>', methods=['POST'])
def excluirPedido(id):
    '''
    URL acionada por um botão para excluir um item do carrinho
    '''
    if 'username' not in session:
            user = None
            return redirect(url_for('index'))
        
    valido, mensagem = alquimias.excluir_pedido(id)

    if valido:
        flash(mensagem)
        return redirect(url_for('index'))
    else:
        flash(mensagem)
        return redirect(url_for('carrinho'))

@app.route('/aumentar/<int:id>', methods=['POST'])
def adicionar(id):
    '''
    URL que resgata o id do produto para acessa-lo no banco e adicionar à sua quantidade
    '''
    if 'username' not in session:
            user = None
            return redirect(url_for('index'))
    
    validar = alquimias.adicionar(id)

    if validar:
        return redirect(url_for('carrinho'))
    else:
        flash('Erro ao adicionar')
        return redirect(url_for('carrinho'))
@app.route('/reduzir/<int:id>', methods=['POST'])
def retirar(id):
    '''
    URL que resgata o id do produto para acessa-lo no banco e retirar um da sua quantidade
    '''
    if 'username' not in session:
            user = None
            return redirect(url_for('index'))
    
    validar = alquimias.retirar(id)

    if validar:
        return redirect(url_for('carrinho'))
    else:
        flash('Limite atingido')
        return redirect(url_for('carrinho'))