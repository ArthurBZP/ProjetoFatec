async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const message = inputField.value.trim();

    if (!message) return;

    // 1. Adiciona a mensagem da utilizadora no ecrã
    chatBox.innerHTML += `<p class="chat-msg chat-msg--sent">${message}</p>`;
    inputField.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // 2. Cria o balão da Ayla vazio com um ID único para receber o texto em streaming
    const balaoId = "ayla-" + Date.now();
    chatBox.innerHTML += `<p class="chat-msg chat-msg--received" id="${balaoId}"></p>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    const balaoAyla = document.getElementById(balaoId);

    try {
        // 3. Faz o pedido ao backend (repare que a sua rota no app.py é /api/chat)
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                mensagem: message,
                historico: [] // Pode implementar o envio do histórico aqui no futuro
            })
        });

        // 4. Lê o streaming de dados recebido do backend
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let textoCompleto = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const pedacoTexto = decoder.decode(value, { stream: true });
            textoCompleto += pedacoTexto;

            // Formata as quebras de linha e atualiza o balão em tempo real
            balaoAyla.innerHTML = textoCompleto.replace(/\n/g, '<br>');
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (error) {
        console.error("Erro na comunicação com a API:", error);
        balaoAyla.innerHTML = '<span style="color: red;">Erro de ligação com o servidor local.</span>';
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Permite enviar a mensagem pressionando a tecla Enter
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}