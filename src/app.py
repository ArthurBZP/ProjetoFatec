from flask import Flask, render_template

# Inicializa o Flask avisando que os arquivos estão dentro da pasta 'src'
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def home():
    # O Flask vai buscar o index.html automaticamente dentro de src/templates
    return render_template("index.html")

if __name__ == "__main__":
    # Roda o servidor local no modo de desenvolvimento (atualiza sozinho ao salvar)
    app.run(debug=True)
