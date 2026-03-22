const msgsContainer = document.getElementById('msgs');
  const inputField = document.getElementById('txt');
  const sendButton = document.getElementById('sendBtn');
  const fileInput = document.getElementById('fileInput');

  function addMessage(text, type = 'me', isFile = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `msg ${type} ${isFile ? 'msg-file' : ''}`;
    
    if (isFile) {
      messageDiv.innerHTML = `📄 <span>${text}</span>`;
    } else {
      messageDiv.textContent = text;
    }

    msgsContainer.appendChild(messageDiv);
    msgsContainer.scrollTop = msgsContainer.scrollHeight;
  }

  function sendMessage() {
    let text = inputField.value.trim();
    if (text === "") return;
    addMessage(text, 'me');
    inputField.value = "";
  }

  // Manejar subida de archivos
  fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    for (let i = 0; i < files.length; i++) {
      addMessage(files[i].name, 'me', true);
    }
    // Limpiar el input para permitir subir el mismo archivo después
    fileInput.value = ""; 
  });

  sendButton.addEventListener('click', sendMessage);
  inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });