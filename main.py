from flask import Flask, render_template, request, redirect, send_file
from flask_wtf import FlaskForm
from wtforms import FileField
from werkzeug.utils import secure_filename
from io import BytesIO
import os
from funcs import *
import sqlite3
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'manumeodeia'
upload_folder = 'static/uploads'
app.config['UPLOAD_FOLDER'] = upload_folder


extensions = ['png', 'jpg', 'jpeg', 'gif']


class UploadFileForm(FlaskForm):
    file = FileField("File")


def allowed_file(filename: str):
    return '.' in filename and filename.split('.')[1] in extensions


@app.route('/')
def home():
    return render_template('home.html', template_folder='templates')


@app.route('/eventos')
def eventos():
    return render_template('eventos.html', template_folder='templates')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html', template_folder='templates')


@app.route('/tylerthecreator')
def tyler():
    return render_template('tylerthecreator.html', template_folder='templates')


@app.route('/ogrilo')
def ogrilo():
    return render_template('ogrilo.html', template_folder='templates')


@app.route('/charliebrown')
def charliebrown():
    return render_template('charliebrown.html', template_folder='templates')


@app.route('/bmth')
def bmth():
    return render_template('bmth.html', template_folder='templates')


@app.route('/portfoliolucas')
def portfolioLucas():
    return render_template('LUCASPANUCCI_PORTFOLIO.html', template_folder='templates')


@app.route('/portfoliomey')
def portfoliomey():
    return render_template('Portfolio2.html', template_folder='templates')


@app.route('/sobremey')
def sobremey():
    return render_template('Sobremey.html', template_folder='templates')


@app.route('/comissoes')
def comissoes():
    return render_template('comissoes.html', template_folder='templates')


@app.route('/portfolio_arte')
def portfolioarte():
    return render_template('portfolio_arte.html', template_folder='templates')


@app.route('/portfolioEvandro')
def portfolioevandro():
    return render_template('portfolioevandro.html', template_folder='templates')


@app.route('/portfoliomatheus')
def portfoliomatheus():
    return render_template('portfoliomatheus.html', template_folder='templates')


@app.route('/portfolioenzo')
def portfolioenzo():
    return render_template('pag.html', template_folder='templates')


@app.route('/apagar')
def apagar():
    con = sqlite3.connect('static/eleventos.db')
    cur = con.cursor()
    params = request.args
    id = params['id']
    sql = "DELETE FROM artista WHERE art_id == " + str(id)
    cur.execute(sql)
    con.commit()

    return redirect('agendar')


@app.route('/agendar', methods=['GET', 'POST'])
def artistas():
    con = sqlite3.connect('static/eleventos.db')
    cur = con.cursor()
    titulo = 'Relação de artistas'

    params = request.form
    files = request.files


    if 'itNome' in params.keys():
        print(params.keys())
        nome = params['itNome']
        email = params['emailContato']
        integrantes = params['inIntegrantes']
        genero = params['sGenero']
        categoria = params['irCategoria']
        site = params['iuSite']
        file = files['ifFoto']
        foto = file.read()

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # salvando o arquivo no diretório certo
        cur.execute("""INSERT INTO artista VALUES (null, ?, ?, ?, ?, ?, ?, ?);""",
                    (nome, email, integrantes, genero, categoria, site, foto))
        con.commit()

    tabela = relatorio(cur=cur)

    return render_template('agendar.html', template_folder='templates', tabela=tabela, titulo=titulo)


@app.route('/mostrar_imagem/<int:id>')
def mostrar_imagem(id):
    con = sqlite3.connect("static/eleventos.db")
    cursor = con.cursor()

    cursor.execute("SELECT art_img FROM artista WHERE art_id=?", (id,))
    resultado = cursor.fetchone()

    if resultado:
        imagem = resultado[0]
        return send_file(BytesIO(imagem), mimetype='image/png')


@app.route('/alterar_imagem', methods=['GET', 'POST'])
def alterar_imagem():
    con = sqlite3.connect("static/eleventos.db")
    cursor = con.cursor()
    params = request.form
    print(request.form.keys())
    print(request.files.keys())
    id = params['art_id']
    file = request.files['ifFoto2']
    foto = file.read()


    sql = "UPDATE artista SET art_img = ? WHERE art_id = ?"
    cursor.execute(sql, (foto, id))

    con.commit()

    return redirect('agendar')


if __name__ == "__main__":
    app.run()
