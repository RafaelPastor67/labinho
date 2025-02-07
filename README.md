# Projetos II <br> Labinho

## 📋 Apresentação
O grupo desenvolveu um site para a matéria de Projetos II do curso Projeto Desenvolve Itabira para atender as demandas de um restaurante da cidade chamado Labinho. Diante disso, incorporamos no site um 
banco de dados para cadastro de clientes e produtos, hierarquia em cargos, uma interface dinâmica e atrativa e um carrinho para os usuários fazerem seus pedidos. 

## 🛠️ Projeto
Conheça a estrutura do nosso projeto

```
Labinho/
│
├── app/
│   ├── models/
│   │    └──models.py
│   ├── tabelas/
│   │    ├──cardapio.csv
│   │    └──users.csv
│   ├── templates/
│   ├── static/
│   │    ├── css/
│   │    ├── css_mobile/
│   │    ├── imagens/
│   │    └── javascript/
│   ├── __init__.py
│   ├── routes.py
│   └── alquimias.py
├── config.py
├── microblog.py
├── popular_db.py
└── requirements.txt
```

## 🌐 Site
O site possui uma database com três tabelas: usuários, cardápio e carrinho. A primeira armazena os usuários cadastrados no sistema do restaurante, sendo esses dividos em três cargos diferentes, podendo assumir funções diferente como cliente, funcionário ou gerente. <br>
Por exemplo, o cliente é o único que pode adicionar itens ao carrinho, o funcionário pode adicionar pratos ao cardápio e o gerente pode também alterar o cargo de usuários no site. Na tabela 'users.csv' existem alguns usuários já cadastrados que podem ser acessados após popular o banco de dados, possibilitando testar essa hierarquia de cargo presente no site.

| id  | username     | password      | email                  | cargo       | remember |
| --- | ------------ | ------------- | ---------------------- | ----------- | -------- |
| 1   | gerente      | gerente123    | gerente@gmail.com      | Gerente     | 0        |
| 2   | funcionario  | funcionario123| teste123@example.com   | Funcionário | 0        |
| 3   | cliente      | cliente123    | cliente@example.com    | Cliente     | 0        |

Caso deseje usar esse usuários, lembre-se de na página de login preencher os campos com as informações acima 

## 🏁 Começando
Como abrir o nosso projeto na web

1. Baixe o repósitorio 'Labinho' completo
2. Navegue ao diretório do projeto no terminnal
3. Crie um ambiente virtual no diretório 'flask_env' <br>
   ```
   python -m venv flask_env
   ```
5. Ative o ambiente <br>
   - Windows:
      ```
      flask_env\Scripts\activate
      ```
   - Linux:
      ```
      source ./flask_env/bin/activate
      ```
7. Baixe as bibliotecas <br>
   - Windows:
      ```
      pip install -r requirements.txt
      ```
   - Linux:
      ```
      python3 -m  pip install -r requirements.txt --break-system-packages
      ```

## ⚙️ Configurações
Antes de prosseguir, é necessário configurar o Flask no terminal

1. Abra o VsCode e no caminho raiz do projeto, no mesmo diretório que 'config.py', crie um arquivo chamado ".flaskenv" com sua chave secreta
   ```
   SECRET_KEY=3f9d0d8c17e544d99b27693d99fd845d
   ```
2. Agora, no terminal, ainda com o ambiente virtual ativado, digite os comandos para criar o banco de dados
   ```
   flask db init
   ```
   ```
   flask db migrate -m "Initial migration"
   ```
    ```
   flask db upgrade
   ```
   - Windows:
      ```
      set FLASK_APP=app.py
      ```
   - Linux:
      ```
      export FLASK_APP=app.py
      ```

## 💾 Popular o banco
Para ter uma experiência do site em funcionamento, popule o banco de dados para ter uma ideia de como ele ficaria em uma estrutura final hospedado em um servidor web

1. Execute popular_db.py no terminal
   - Windows:
      ```
      python popular_db.py
      ```
   - Linux:
      ```
      python3 popular_db.py
      ```
   
## 🖥️ Processando
Para finalizar, ative o flask para carregar o servidor web em sua máquina

1. No terminal, digite:
    ```
    flask run
    ```
    
Aproveite o site!

## 👨‍💻 Desenvolvedores
Membros do grupo responsáveis pela criação do projeto







      
