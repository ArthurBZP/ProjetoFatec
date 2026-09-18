async function sendMessage() {
  const inputField = document.getElementById('user-input');
  const chatBox = document.getElementById('chat-box');
  const message = inputField.value.trim();

  if (!message) return;

  // 1. Adiciona a mensagem da usuária na tela
  chatBox.innerHTML += `<p class="chat-msg chat-msg--sent">${message}</p>`;
  inputField.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  // 2. Adiciona o indicador de "Ayla está digitando..."
  const typingId = "typing-" + Date.now();
  chatBox.innerHTML += `<p class="chat-msg chat-msg--received" id="${typingId}"><em>Ayla está digitando...</em></p>`;
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // 3. Remove o indicador visual de digitação
    const typingIndicator = document.getElementById(typingId);
    if (typingIndicator) typingIndicator.remove();

    // 4. Adiciona a resposta final do Gemini na tela
    if (data.response) {
        const formattedResponse = data.response.replace(/\n/g, '<br>');
        chatBox.innerHTML += `<p class="chat-msg chat-msg--received">${formattedResponse}</p>`;
    } else {
        chatBox.innerHTML += `<p class="chat-msg chat-msg--received" style="color: red;">Erro ao contatar servidor.</p>`;
    }
  } catch (error) {
    const typingIndicator = document.getElementById(typingId);
    if (typingIndicator) typingIndicator.remove();
    chatBox.innerHTML += `<p class="chat-msg chat-msg--received" style="color: red;">Erro de conexão com o servidor local.</p>`;
  }
  
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Permite enviar apertando Enter
function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}