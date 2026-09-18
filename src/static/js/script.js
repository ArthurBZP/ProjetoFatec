async function sendMessage() {
  const inputField = document.getElementById('user-input');
  const chatBox = document.getElementById('chat-box');
  const message = inputField.value.trim();

  if (!message) return;

  // 1. Adiciona a mensagem da usuária na tela
  chatBox.innerHTML += `<p class="chat-msg chat-msg--sent">${message}</p>`;
  inputField.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  // 2. Envia para o backend (Flask)
  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // 3. Adiciona a resposta do Gemini na tela
    if (data.response) {
        // Converte quebras de linha em <br> para manter a formatação do texto
        const formattedResponse = data.response.replace(/\n/g, '<br>');
        chatBox.innerHTML += `<p class="chat-msg chat-msg--received">${formattedResponse}</p>`;
    } else {
        chatBox.innerHTML += `<p class="chat-msg chat-msg--received" style="color: red;">Erro ao contatar servidor.</p>`;
    }
  } catch (error) {
    chatBox.innerHTML += `<p class="chat-msg chat-msg--received" style="color: red;">Erro de conexão.</p>`;
  }
  
  // Rola o chat para baixo novamente após receber a resposta
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Permite enviar apertando Enter
function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}