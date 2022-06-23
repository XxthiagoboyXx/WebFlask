from flask import Flask, request, render_template, redirect,  url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blog.sqlite3' #o nome do banco de dado será "blog"

#class User(db.Model): #criando o Model do author no banco de dados
#    id = db.Column(db.Integer(), primary_key=True)
#    username = db.Column(db.String())
#    password = db.Column(db.String())

class Publicacao(db.Model): #criando o Model da publicacao no banco de dados
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    author = db.Column(db.String())

@app.route("/") #criando uma rota para a pagina inicial
def home():
    #nome = request.args.get("user") #recebendo parametro por GET
    #return "<h1>Hello {}</h1>".format(nome) #inseguro, poist retorna o parametro de forma crua
    publi = Publicacao.query.all() #faz uma consulta no banco de dados e retorna para a var publi
    return render_template("index.html", posts=publi) #template padrão para receber trabalhar com parametros enviados pelo usuario de maneira segura

@app.route("/publi/add", methods=["POST"]) #o methods=Post faz permitir o envio do formulário, sem isso ocorre um erro de permissão
def add_post():
    try:
        form = request.form #por padrao quando uma requisicao POST é realizada, os dados são enviados oara o atributo form
        publi = Publicacao(title=form["title"], content=form["content"], author=form["author"]) #instanciando um objeto da classe Publicacao passando os argumentos necessarios
        db.session.add(publi) #adiciona no banco de dados
        db.session.commit() #salva definitivamente no banco de dados
    except Exception as e:
        print("Error ", e)

    return redirect(url_for("home")) #quando é feito o post o usuário é redirecionado para a View Home


@app.route("/publi/<id>/del") #como o argumento já está no link, não é necessário permitir o método POST | é passado o id correspondente ao post que será deletado, esse id também é passado como pararâmetro da função
def delete_post(id):
    try:
        publi = Publicacao.query.get(id) #pega o id da publicação específica
        db.session.delete(publi) #adiciona no banco de dados
        db.session.commit() #salva definitivamente no banco de dados
    except Exception as e:
        print("Error ",e)

    return redirect(url_for("home")) #quando é feito o post o usuário é redirecionado para a View Home


@app.route("/publi/<id>/edit", methods=["POST", "GET"]) #o methods=Post e GET faz permitir o envio do formulário e a visualização do conteúdo respectivamente, sem isso ocorre um erro de permissão
def edit_post(id):
    if request.method == "POST":
        try:
            publi = Publicacao.query.get(id)
            form = request.form
            publi.title = form["title"]
            publi.author = form["author"]
            publi.content = form["content"]
            db.session.commit() #salva definitivamente no banco de dados
        except Exception as e:
            print("Error ",e)

        return redirect(url_for("home")) #quando é feito o post o usuário é redirecionado para a View Home
    else:
        try:
            publi = Publicacao.query.get(id)
            return render_template("edit.html", publi=publi)
        except Exception as e:
            print("Error ", e)

    return  redirect(url_for("home"))
db.create_all()
app.run(debug=True) #para edição em tempo real, o debug é setado True