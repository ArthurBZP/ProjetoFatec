"""Servidor local do Coletivo Margarida: Flask + RAG."""
from threading import Lock
from flask import Flask, Response, jsonify, render_template, request
from jinja2 import TemplateNotFound
from rag_backend import responder

app = Flask(__name__)
trava = Lock()

@app.get("/")
def inicio():
    try:
        return render_template("index.html")
    except TemplateNotFound:
        return "Coloque sua página em templates/index.html e recarregue.", 503

@app.post("/chat")
@app.post("/api/chat")
def chat():
    texto_puro = request.path == "/api/chat"

    def erro(mensagem, codigo):
        if texto_puro:
            return Response(mensagem, status=codigo, mimetype="text/plain")
        return jsonify({"error": mensagem}), codigo

    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro("Envie um objeto JSON com a mensagem.", 400)
    mensagem = dados.get("mensagem", dados.get("message"))
    if not isinstance(mensagem, str) or not mensagem.strip():
        return erro("Digite uma mensagem.", 400)
    if len(mensagem) > 2000:
        return erro("Use até 2.000 caracteres.", 400)
    if not trava.acquire(blocking=False):
        return erro("O modelo está ocupado. Tente novamente em instantes.", 503)
    try:
        resposta, fontes = responder(mensagem.strip())
        if texto_puro:
            # Compatível com leitura de texto/readable stream do frontend antigo.
            # A resposta chega completa; não há geração token a token.
            return Response(resposta, mimetype="text/plain")
        return jsonify({"response": resposta, "sources": fontes})
    except FileNotFoundError:
        return erro("Base ausente. Copie os arquivos do Colab para rag_store e reinicie.", 503)
    except Exception:
        app.logger.exception("Falha ao executar RAG")
        return erro("Não foi possível responder. Confira o terminal do servidor.", 500)
    finally:
        trava.release()

@app.route("/direitos")
def direitos():
    return render_template("direitos.html")


@app.route("/denuncia")
def denuncia():
    return render_template("denuncia.html")


@app.route("/emergencia")
def emergencia():
    return render_template("emergencia.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
