from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/manutencao'

db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = "Cliente"

    cpf = db.Column(db.INTEGER, primary_key=True)
    nomeCli = db.Column(db.VARCHAR(100))

    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nomeCli = nome

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
def excluirCliente():
    return

if(__name__ == '__main__'):
    app.run(debug=True)