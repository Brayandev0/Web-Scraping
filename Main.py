from flask import Flask,render_template
from api_buscadora import app as Pagina_api 
app = Flask(__name__)

app.register_blueprint(Pagina_api,url_prefix="/api")

@app.route("/")
def Pagina_principal():
    return render_template("Documentacao.html")


app.run()