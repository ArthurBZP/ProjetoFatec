import os
from flask import Flask, request, Response, render_template
from dotenv import load_dotenv
from google import genai # Importação da nova biblioteca

# Carrega as variáveis do ficheiro .env
load_dotenv()
chave = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

# Nova forma de inicializar o cliente do Gemini
client = genai.Client(api_key=chave)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    dados = request.json
    mensagem_usuario = dados.get('mensagem')

    def gerar_resposta_stream():
        try:
            # Nova forma de solicitar respostas em fluxo (streaming)
            resposta = client.models.generate_content_stream(
                model='gemini-3.6-flash',
                contents=mensagem_usuario
            )
            for chunk in resposta:
                yield chunk.text
        except Exception as e:
            # Se falhar, exibe o erro no ecrã da plataforma
            erro_str = f"\n[Falha na API: {str(e)}]"
            print(erro_str)
            yield erro_str

    return Response(gerar_resposta_stream(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5001)