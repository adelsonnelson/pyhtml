from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
from database import db
from flask_migrate import Migrate
from models import Inventario
app.config['SECRET_KEY'] = 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e'

# drive://usuario:senha@servidor/banco_de_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/flask"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>')
@app.route('/aula/<nome>/<curso>/<ano>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = 'Carlos', curso = 'Informática', ano = 2):
    dados = {'nome': nome, 'curso': curso, 'ano': ano}
    return render_template('aula.html', dados_curso = dados)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dados',methods=['POST'])
def dados():
    flash('Dados enviados!!!')
    dados = request.form
    return render_template('dados.html', dados=dados)

@app.route('/inventario')
def inventario():
    u = Inventario.query.all()
    return render_template('inventario_lista.html', dados = u)

@app.route('/inventario/add')
def inventario_add():
    return render_template('inventario_add.html')

@app.route('/inventario/save', methods=['POST'])
def inventario_save():
    nome = request.form.get('nome')
    quantidade = request.form.get('quantidade')
    localizacao = request.form.get('localizacao')
    if nome and quantidade and localizacao:
        inventario = Inventario(nome, quantidade, localizacao)
        db.session.add(inventario)
        db.session.commit()
        flash('Inventário cadastrado com sucesso!!!')
        return redirect('/inventario')
    else:
        flash('Preencha todos os campos!!!')
        return redirect('/inventario/add')
    
@app.route('/inventario/remove/<int:id>')
def inventario_remove(id):
    inventario = Inventario.query.get(id)
    if id > 0:
        db.session.delete(inventario)
        db.session.commit()
        flash('Inventário removido com sucesso!!!')
        return redirect('/inventario')
    else:
        flash('Caminho incorreto!!!')
        return redirect('/inventario')

@app.route('/inventario/edita/<int:id>')
def inventario_edita(id):
    inventario = Inventario.query.get(id)
    return render_template('inventario_edita.html', dados = inventario)

@app.route('/inventario/editasave', methods=['POST'])
def inventario_editasave():
    nome = request.form.get('nome')
    quantidade = request.form.get('quantidade')
    localizacao = request.form.get('localizacao')
    id = request.form.get('id')
    if id and nome and quantidade and localizacao:
        inventario = Inventario.query.get('id')
        inventario.nome = nome
        inventario.quantidade = quantidade
        inventario.localizacao = localizacao
        db.session.commit()
        flash('Dados atualizados com sucesso!!!')
        return redirect('/inventario')
    else: 
        flash('Faltando dados!!!')
        return redirect('/inventario')


if __name__ == '__main__':
    app.run()
