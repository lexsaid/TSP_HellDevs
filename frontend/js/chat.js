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

    const btnVer = document.getElementById('btnVerTrabajo');
    const jobNameEl = document.getElementById('jobName');
    const jobPriceEl = document.getElementById('jobPrice');

    function setBannerNoDisponible(texto) {
        jobNameEl.textContent = texto;
        jobPriceEl.textContent = '';
        if (btnVer) {
            btnVer.disabled = true;
            btnVer.style.opacity = '0.6';
            btnVer.style.cursor = 'not-allowed';
        }
    }

    function setBannerInfo({
        titulo,
        subtexto,
        botonTexto,
        onClick,
        chatTitulo
    }) {
        jobNameEl.textContent = titulo;
        jobPriceEl.textContent = subtexto || '';
        if (chatTitulo) {
            document.getElementById('chatTitle').textContent = chatTitulo;
        }
        if (btnVer && botonTexto && onClick) {
            btnVer.textContent = botonTexto;
            btnVer.addEventListener('click', onClick);
        }
    }

    // Cargar detalles del trabajo/albergue/mascota (para el banner)
    try {
        if (idTrabajo < 0) {
            if (idTrabajo <= -2000000) {
                const idAnimal = -idTrabajo - 2000000;
                const resAdop = await window.apiFetch(`/adopciones/detalle?id_animal=${idAnimal}`);
                if (resAdop && resAdop.ok) {
                    const detalle = await resAdop.json();
                    const adopcion = detalle.adopcion || {};
                    setBannerInfo({
                        titulo: adopcion.nombre || 'Adopcion sin nombre',
                        subtexto: 'En adopcion',
                        botonTexto: 'Ver adopcion',
                        chatTitulo: `Chat: ${adopcion.nombre || 'Adopcion'}`,
                        onClick: () => {
                            window.location.href = `ver_adopcion.html?idAnimal=${idAnimal}`;
                        }
                    });
                } else {
                    setBannerNoDisponible('Adopcion no encontrada');
                }
            } else if (idTrabajo <= -1000000) {
                const idAnimal = -idTrabajo - 1000000;
                const resPerd = await window.apiFetch(`/mascotas_perdidas/detalle?id_animal=${idAnimal}`);
                if (resPerd && resPerd.ok) {
                    const detalle = await resPerd.json();
                    const perdida = detalle.mascotaPerdida || {};
                    setBannerInfo({
                        titulo: perdida.nombre || 'Mascota sin nombre',
                        subtexto: 'Mascota perdida',
                        botonTexto: 'Ver reporte',
                        chatTitulo: `Chat: ${perdida.nombre || 'Mascota perdida'}`,
                        onClick: () => {
                            window.location.href = `ver_mascota_perdida.html?idAnimal=${idAnimal}`;
                        }
                    });
                } else {
                    setBannerNoDisponible('Mascota no encontrada');
                }
            } else {
                const idAlbergue = Math.abs(idTrabajo);
                const resAlbergue = await window.apiFetch(`/albergue?id=${idAlbergue}`);
                if (resAlbergue && resAlbergue.ok) {
                    const detalle = await resAlbergue.json();
                    const albergue = detalle.albergue || {};
                    setBannerInfo({
                        titulo: albergue.nombre || 'Albergue sin nombre',
                        subtexto: `$${albergue.costoDiario ?? '--'} / dia`,
                        botonTexto: 'Ver albergue',
                        chatTitulo: `Chat: ${albergue.nombre || 'Albergue'}`,
                        onClick: () => {
                            localStorage.setItem('albergueSeleccionado', JSON.stringify(detalle));
                            window.location.href = 'ver_albergue.html';
                        }
                    });
                } else {
                    setBannerNoDisponible('Albergue no encontrado');
                }
            }
        } else {
            const resTrabajo = await window.apiFetch(`/trabajo?id=${idTrabajo}`);
            if (resTrabajo && resTrabajo.ok) {
                const trabajo = await resTrabajo.json();
                setBannerInfo({
                    titulo: trabajo.nombre,
                    subtexto: `$${trabajo.monto}`,
                    botonTexto: 'Ver publicacion',
                    chatTitulo: `Chat: ${trabajo.nombre}`,
                    onClick: () => {
                        localStorage.setItem('idTrabajoSeleccionado', idTrabajo);
                        window.location.href = 'ver_trabajo_del_otro.html';
                    }
                });
            } else {
                setBannerNoDisponible('Trabajo no encontrado');
            }
        }
    } catch (e) {
        console.error('Error al cargar detalles', e);
        if (idTrabajo < 0) {
            setBannerNoDisponible('Publicacion no encontrada');
        } else {
            setBannerNoDisponible('Trabajo no encontrado');
        }
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