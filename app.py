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

class Peca(db.Model):
    __tablename__ = "Peca"

    codPeca = db.Column(db.VARCHAR(50), primary_key=True)
    descricao = db.Column(db.VARCHAR(200))

    def __init__(self, cod, descr):
        self.codPeca = cod
        self.descricao = descr

class UpgradeRevisao(db.Model):
    __tablename__ = "Upgrade_Revisao"

    numSerieComputador = db.Column(db.VARCHAR(50), ForeignKey("Computador.numSerie"), primary_key=True)
    dataProgramada = db.Column(db.VARCHAR(50), primary_key=True)
    dataUltimoUpgrade = db.Column(db.VARCHAR(50))
    dataExecutada = db.Column(db.VARCHAR(50))

    numSerie = relationship("Computador", foreign_keys=[numSerieComputador])

    def __init__(self, numSerie, dataProg, dataUlti, dataExec):
        self.numSerieComputador = numSerie
        self.dataProgramada = dataProg
        self.dataUltimoUpgrade = dataUlti
        self.dataExecutada = dataExec

class PecaUpgradeRevisao(db.Model):
    __tablename__ = "Peca_Upgrade_Revisao"

    numSerieMaquina = db.Column(db.VARCHAR(50), ForeignKey("Upgrade_Revisao.numSerieComputador"), primary_key=True)
    dataProgramadaServico = db.Column(db.VARCHAR(50), ForeignKey("Upgrade_Revisao.dataProgramada"), primary_key=True)
    codPecaServico = db.Column(db.VARCHAR(50), ForeignKey("Peca.codPeca"), primary_key=True)
    quantidade = db.Column(db.INTEGER)

    numSerieComputador = relationship("UpgradeRevisao", foreign_keys=[numSerieMaquina])
    dataProgramada = relationship("UpgradeRevisao", foreign_keys=[dataProgramadaServico])
    codPeca = relationship("Peca", foreign_keys=[codPecaServico])

    def __init__(self, numSerie, dataProg, codPecServ, quant):
        self.numSerieMaquina = numSerie
        self.dataProgramadaServico = dataProg
        self.codPecaServico = codPecServ
        self.quantidade = quant

db.create_all()


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/cadastrarCliente")
def cadastrarCliente():
    return render_template("cadastroCliente.html")


@app.route("/cadastroCliente", methods=["GET", "POST"])
def cadastroCliente():
    if (request.method == "POST"):
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")

        if (nome and cpf):
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
    cliente = Cliente.query.filter_by(cpf=cpf).first()
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
    if (request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        modeloComp = request.form.get("modelo-comp")
        cpfCliente = request.form.get("cpf-cliente")

        if (numeroSerie and modeloComp and cpfCliente):
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

@app.route("/cadastrarPeca")
def cadastrarPeca():
    return render_template("cadastroPeca.html")

@app.route("/cadastroPeca", methods=["GET", "POST"])
def cadastroPeca():
    if (request.method == "POST"):
        codPeca = request.form.get("cod-peca")
        descricao = request.form.get("descricao")

        if (codPeca and descricao):
            peca = Peca(codPeca, descricao)
            db.session.add(peca)
            db.session.commit()

    return redirect(url_for("index"))

@app.route("/listaPecas")
def listaPecas():
    pecas = Peca.query.all()
    return render_template("listaPecas.html", pecas=pecas)


@app.route("/excluirPeca/<string:codPeca>")
def excluirPeca(codPeca):
    peca = Peca.query.filter_by(codPeca=codPeca).first()
    db.session.delete(peca)
    db.session.commit()

    return redirect(url_for("listaPecas"))


@app.route("/editarPeca/<string:codPeca>", methods=["GET", "POST"])
def editarPeca(codPeca):
    peca = Peca.query.filter_by(codPeca=codPeca).first()

    if (request.method == "POST"):
        codPeca = request.form.get("cod-peca")
        descricao = request.form.get("descricao")

        if (codPeca and descricao):
            peca.codPeca = codPeca
            peca.descricao = descricao

            db.session.commit()

            return redirect(url_for("listaPecas"))

    return render_template("editarPeca.html", peca=peca)


@app.route("/cadastrarUpgradeRevisao")
def cadastrarUpgradeRevisao():
    return render_template("cadastroUpgradeRevisao.html")


@app.route("/cadastroUpgradeRevisao", methods=["GET", "POST"])
def cadastroUpgradeRevisao():
    if (request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        dataProg = request.form.get("data-prog")
        dataUlti = request.form.get("data-ulti")
        dataExec = request.form.get("data-exec")

        if (numeroSerie and dataProg):
            ur = UpgradeRevisao(numeroSerie, dataProg, dataUlti, dataExec)
            db.session.add(ur)
            db.session.commit()

    return redirect(url_for("index"))


@app.route("/listaUpgradeRevisao")
def listaUpgradeRevisao():
    servicos = UpgradeRevisao.query.all()
    return render_template("listaUpgradeRevisao.html", servicos=servicos)


@app.route("/excluirUpgradeRevisao/<string:numSerie>/<string:dataProg>")
def excluirUpgradeRevisao(numSerie, dataProg):
    servico = UpgradeRevisao.query.filter_by(numSerieComputador=numSerie).filter_by(dataProgramada=dataProg).first()
    db.session.delete(servico)
    db.session.commit()

    return redirect(url_for("listaUpgradeRevisao"))


@app.route("/editarUpgradeRevisao/<string:numSerie>/<string:dataProg>", methods=["GET", "POST"])
def editarUpgradeRevisao(numSerie, dataProg):
    servico = UpgradeRevisao.query.filter_by(numSerieComputador=numSerie).filter_by(dataProgramada=dataProg).first()

    if (request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        dataProg = request.form.get("data-prog")
        dataUlti = request.form.get("data-ulti")
        dataExec = request.form.get("data-exec")

        if (numeroSerie and dataProg):
            servico.numSerieComputador = numeroSerie
            servico.dataProgramada = dataProg
            servico.dataUltimoUpgrade = dataUlti
            servico.dataExecutada = dataExec

            db.session.commit()

            return redirect(url_for("listaUpgradeRevisao"))

    return render_template("editarUpgradeRevisao.html", servico=servico)

@app.route("/cadastrarPecaUpgradeRevisao")
def cadastrarPecaUpgradeRevisao():
    return render_template("cadastroPecaUpgradeRevisao.html")


@app.route("/cadastroPecaUpgradeRevisao", methods=["GET", "POST"])
def cadastroPecaUpgradeRevisao():
    if (request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        dataProg = request.form.get("data-prog")
        codPeca = request.form.get("cod-peca")
        quant = request.form.get("quant")

        if (numeroSerie and dataProg and codPeca and quant):
            pecaServico = PecaUpgradeRevisao(numeroSerie, dataProg, codPeca, quant)
            db.session.add(pecaServico)
            db.session.commit()

    return redirect(url_for("index"))


@app.route("/listaPecaUpgradeRevisao")
def listaPecaUpgradeRevisao():
    pecasServico = PecaUpgradeRevisao.query.all()
    return render_template("listaPecaUpgradeRevisao.html", pecasServico=pecasServico)


@app.route("/excluirPecaUpgradeRevisao/<string:numSerie>/<string:dataProg>/<string:codPeca>")
def excluirPecaUpgradeRevisao(numSerie, dataProg, codPeca):
    pecaServico = PecaUpgradeRevisao.query.filter_by(numSerieMaquina=numSerie).filter_by(
        dataProgramadaServico=dataProg).filter_by(codPecaServico=codPeca).first()
    db.session.delete(pecaServico)
    db.session.commit()

    return redirect(url_for("listaPecaUpgradeRevisao"))


@app.route("/editarPecaUpgradeRevisao/<string:numSerie>/<string:dataProg>/<string:codPeca>", methods=["GET", "POST"])
def editarPecaUpgradeRevisao(numSerie, dataProg, codPeca):
    pecaServico = PecaUpgradeRevisao.query.filter_by(numSerieMaquina=numSerie).filter_by(
        dataProgramadaServico=dataProg).filter_by(codPecaServico=codPeca).first()

    if (request.method == "POST"):
        numeroSerie = request.form.get("num-serie")
        dataProg = request.form.get("data-prog")
        codPeca = request.form.get("cod-peca")
        quant = request.form.get("quant")

        if (numeroSerie and dataProg and codPeca and quant):
            pecaServico.numSerieMaquina = numeroSerie
            pecaServico.dataProgramadaServico = dataProg
            pecaServico.codPecaServico = codPeca
            pecaServico.quantidade = quant

            db.session.commit()

            return redirect(url_for("listaPecaUpgradeRevisao"))

    return render_template("editarPecaUpgradeRevisao.html", pecaServico=pecaServico)

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error("Unhadled exception: %s" % (e))
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)
