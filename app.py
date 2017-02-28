from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/manutencao'

db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = "Cliente"

    cpf = db.Column(db.VARCHAR(50), primary_key=True)
    nomeCli = db.Column(db.VARCHAR(200))

    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nomeCli = nome

class Computador(db.Model):
    __tablename__ = "Computador"

    numSerie = db.Column(db.VARCHAR(50), primary_key=True)
    modelo = db.Column(db.VARCHAR(50))
    cpfCli = db.Column(db.VARCHAR(50), ForeignKey("Cliente.cpf"))

    cpf = relationship("Cliente", foreign_keys=[cpfCli])

    def __init__(self, numeroSerie, modeloComputador, cpfCliente):
        self.numSerie = numeroSerie
        self.modelo = modeloComputador
        self.cpfCli = cpfCliente

db.create_all()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrarCliente")
def cadastrarCliente():
    return render_template("cadastroCliente.html")

@app.route("/cadastroCliente", methods=["GET", "POST"])
def cadastroCliente():
    if(request.method == "POST"):
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")

        if(nome and cpf):
            c = Cliente(cpf, nome)
            db.session.add(c)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/listaClientes")
def listaClientes():
    clientes = Cliente.query.all()
    return render_template("listaClientes.html", clientes=clientes)

@app.route("/excluirCliente/<int:cpf>")
def excluirCliente(cpf):
    cliente  = Cliente.query.filter_by(cpf=cpf).first()
    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("listaClientes"))

@app.route("/editarCliente/<int:cpf>", methods=["GET", "POST"])
def editarCliente(cpf):
    cliente = Cliente.query.filter_by(cpf=cpf).first()

    if (request.method == "POST"):
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")

        if (nome and cpf):
            cliente.cpf = cpf
            cliente.nomeCli = nome

            db.session.commit()

            return redirect(url_for("listaClientes"))

    return render_template("editarCliente.html", cliente=cliente)

@app.route("/cadastrarComputador")
def cadastrarComputador():
    return render_template("cadastroComputador.html")

@app.route("/cadastroComputador", methods=["GET", "POST"])
def cadastroComputador():
    if(request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        modeloComp = request.form.get("modelo-comp")
        cpfCliente = request.form.get("cpf-cliente")

        if(numeroSerie and modeloComp and cpfCliente):
            c = Computador(numeroSerie, modeloComp, cpfCliente)
            db.session.add(c)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/listaComputadores")
def listaComputadores():
    computadores = Computador.query.all()
    return render_template("listaComputadores.html", computadores=computadores)

@app.route("/excluirComputador/<string:numSerie>")
def excluirComputador(numSerie):
    computador = Computador.query.filter_by(numSerie=numSerie).first()
    db.session.delete(computador)
    db.session.commit()

    return redirect(url_for("listaComputadores"))

@app.route("/editarComputador/<string:numSerie>", methods=["GET", "POST"])
def editarComputador(numSerie):
    computador = Computador.query.filter_by(numSerie=numSerie).first()

    if (request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        modelo = request.form.get("modelo-comp")
        cpfCli = request.form.get("cpf-cliente")

        if (numeroSerie and modelo and cpfCli):
            computador.numSerie = numeroSerie
            computador.modelo = modelo
            computador.cpfCli = cpfCli

            db.session.commit()

            return redirect(url_for("listaComputadores"))

    return render_template("editarComputador.html", computador=computador)

if(__name__ == '__main__'):
    app.run(debug=True)