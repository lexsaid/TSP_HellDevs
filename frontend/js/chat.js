document.addEventListener('DOMContentLoaded', async () => {
    const msgsContainer = document.getElementById('msgs');
    const inputField = document.getElementById('txt');
    const sendButton = document.getElementById('sendBtn');
    const fileInput = document.getElementById('fileInput');

    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }
    const myId = parseInt(myIdStr);

    const urlParams = new URLSearchParams(window.location.search);
    const idTrabajoStr = urlParams.get('idTrabajo');
    const idReceptorStr = urlParams.get('receptor');

    if (!idTrabajoStr || !idReceptorStr) {
        console.warn("Faltan parámetros en la URL (idTrabajo, receptor). Usando valores de prueba 1 y 2 por defecto.");
        // alert("Faltan parámetros en la URL (idTrabajo, receptor).");
        // return;
    }

    const idTrabajo = idTrabajoStr ? parseInt(idTrabajoStr) : 1;
    const idReceptor = idReceptorStr ? parseInt(idReceptorStr) : 2;

    // Cargar detalles del trabajo (para el banner)
    try {
        const resTrabajo = await window.apiFetch(`/trabajo?id=${idTrabajo}`);
        if (resTrabajo && resTrabajo.ok) {
            const trabajo = await resTrabajo.json();
            document.getElementById('jobName').textContent = trabajo.nombre;
            document.getElementById('jobPrice').textContent = `$${trabajo.monto}`;
            document.getElementById('chatTitle').textContent = `Chat: ${trabajo.nombre}`;

            const btnVer = document.getElementById('btnVerTrabajo');
            if (btnVer) {
                btnVer.addEventListener('click', () => {
                    localStorage.setItem('idTrabajoSeleccionado', idTrabajo);
                    window.location.href = 'ver_trabajo_del_otro.html';
                });
            }
        } else {
            document.getElementById('jobName').textContent = "Trabajo no encontrado";
        }
    } catch (e) {
        console.error("Error al cargar trabajo", e);
    }

    let loadedMessageIds = new Set();

    function renderMessage(msg) {
        if (loadedMessageIds.has(msg.idMensaje)) return;
        loadedMessageIds.add(msg.idMensaje);

        const type = (msg.idRemitente === myId) ? 'me' : 'other';
        const messageDiv = document.createElement('div');
        messageDiv.className = `msg ${type}`;

        const textSpan = document.createElement('span');
        textSpan.textContent = msg.contenido;

        const dateSpan = document.createElement('span');
        dateSpan.className = 'msg-date';
        dateSpan.textContent = msg.fechaMensaje || '';

        messageDiv.appendChild(textSpan);
        messageDiv.appendChild(dateSpan);

        msgsContainer.appendChild(messageDiv);
        msgsContainer.scrollTop = msgsContainer.scrollHeight;
    }

    async function fetchMessages() {
        try {
            const res = await window.apiFetch(`/mensaje?idAnimalLover=${myId}&idOtroAnimalLover=${idReceptor}&idTrabajo=${idTrabajo}`);
            if (res && res.ok) {
                const mensajes = await res.json();
                mensajes.forEach(renderMessage);
            }
        } catch (e) {
            console.error("Error al obtener mensajes", e);
        }
    }

    async function sendMessage() {
        let text = inputField.value.trim();
        if (text === "") return;

        // Limpiar para que el usuario sienta respuesta inmediata
        const oldText = text;
        inputField.value = "";

        // Mostramos el mensaje en local antes de que el servidor responda (Optimistic UI)
        // Pero para no duplicar si el polling gana, no le asignamos id.
        const tempMsgDiv = document.createElement('div');
        tempMsgDiv.className = `msg me temp-msg`;
        tempMsgDiv.textContent = oldText;
        tempMsgDiv.style.opacity = '0.6';
        msgsContainer.appendChild(tempMsgDiv);
        msgsContainer.scrollTop = msgsContainer.scrollHeight;

        const dateStr = window.getFormattedDateMX();

        const newMsg = {
            idAnimalLoverEmisor: myId,
            idAnimalLoverReceptor: idReceptor,
            idTrabajo: idTrabajo,
            contenido: oldText,
            fechaMensaje: dateStr
        };

        try {
            const res = await window.apiFetch('/mensaje', {
                method: 'POST',
                body: JSON.stringify(newMsg)
            });

            if (res && res.ok) {
                tempMsgDiv.remove();
                await fetchMessages(); // Refrescar para mostrar mensaje real y dar id
            } else {
                tempMsgDiv.style.color = "red";
                console.error("Error al enviar", await res.text());
                alert("No se pudo enviar el mensaje");
            }
        } catch (e) {
            tempMsgDiv.style.color = "red";
            console.error("Error de red enviando mensaje", e);
        }
    }

    sendButton.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Manejar subida de archivos (visual solamente)
    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        for (let i = 0; i < files.length; i++) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `msg me msg-file`;
            messageDiv.innerHTML = `📄 <span>${files[i].name}</span>`;
            msgsContainer.appendChild(messageDiv);
            msgsContainer.scrollTop = msgsContainer.scrollHeight;
        }
        fileInput.value = "";
    });

    // Polling cada segundo
    fetchMessages();
    setInterval(fetchMessages, 1000);
});