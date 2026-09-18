import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (sua API Key)
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Inicializa o Flask avisando que os arquivos estão dentro das pastas padrão
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuração do Comportamento do Bot
system_instruction = """Você é a assistente virtual do Coletivo Margarida.
Seu papel é oferecer escuta empática, acolhimento e orientações de proteção para mulheres em situação de vulnerabilidade ou violência.
Regras:
1. Mantenha um tom gentil, seguro, livre de julgamentos e focado na segurança da mulher.
2. Nunca exija dados pessoais ou endereço.
3. Se a usuária relatar risco iminente ou violência física acontecendo, oriente IMEDIATAMENTE a ligar para o 190 (Polícia) ou 180 (Central da Mulher) e a buscar um local seguro.
4. Responda de forma concisa e clara."""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)
# Mantém o histórico da conversa vivo na memória do servidor
chat = model.start_chat(history=[])

@app.route("/")
def home():
    # O Flask vai buscar o index.html automaticamente dentro de templates[cite: 1]
    return render_template("index.html")

# Nova rota para processar as mensagens do chat
@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    user_msg = data.get("message")
    
    if not user_msg:
        return jsonify({"error": "Mensagem vazia"}), 400
    
    try:
        response = chat.send_message(user_msg)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": "Desculpe, ocorreu um erro no sistema. Tente novamente ou ligue para 180."}), 500

if __name__ == "__main__":
    # Roda o servidor local no modo de desenvolvimento (atualiza sozinho ao salvar)[cite: 1]
    app.run(debug=True)