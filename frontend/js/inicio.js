document.addEventListener('DOMContentLoaded', () => {
    const openMenu = document.getElementById('openMenu');
    const sideMenu = document.getElementById('sideMenu');
    const overlay = document.getElementById('menuOverlay');
    const btnLogout = document.getElementById('btnLogout');

    // Función para abrir
    openMenu.addEventListener('click', () => {
        sideMenu.classList.add('active');
        overlay.classList.add('active');
    });

    // Función para cerrar (clic en la capa oscura)
    overlay.addEventListener('click', () => {
        sideMenu.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Cerrar Sesión
    btnLogout.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('idAnimalLover');
        localStorage.removeItem('nombre');
        window.location.href = "login.html";
    });

    // ==================== BUZÓN DE CHATS ====================
    const openMailbox = document.getElementById('openMailbox');
    const closeMailbox = document.getElementById('closeMailbox');
    const mailboxDrawer = document.getElementById('mailboxDrawer');
    const chatsContainer = document.getElementById('chatsContainer');

    // --- Notificación visual (badge en el ícono del buzón) ---
    const badge = document.createElement('span');
    badge.id = 'mailBadge';
    badge.style.cssText = 'display:none; position:absolute; top:-4px; right:-6px; width:12px; height:12px; background:#ef4444; border-radius:50%; border:2px solid #5e17eb; animation: pulse 1.5s infinite;';
    openMailbox.style.position = 'relative';
    openMailbox.appendChild(badge);

    // Inyectar animación pulse si no existe
    if (!document.getElementById('pulseStyle')) {
        const style = document.createElement('style');
        style.id = 'pulseStyle';
        style.textContent = `@keyframes pulse { 0%,100% { transform:scale(1); opacity:1; } 50% { transform:scale(1.3); opacity:0.7; } }`;
        document.head.appendChild(style);
    }

    // --- Polling ligero: solo pregunta si hay nuevos mensajes ---
    let notifInterval = null;
    let ultimoIdConocido = parseInt(localStorage.getItem('ultimoIdMensajeRecibido') || '0');

    async function checkNuevosMensajes() {
        const myId = localStorage.getItem('idAnimalLover');
        if (!myId) return;

        try {
            const res = await window.apiFetch(`/mensajes/hay-nuevos?idAnimalLover=${myId}&ultimoIdMensaje=${ultimoIdConocido}`);
            if (res && res.ok) {
                const data = await res.json();
                badge.style.display = data.hayNuevos ? 'block' : 'none';
            }
        } catch (e) {
            // Silencioso — no interrumpir la experiencia
        }
    }

    // Iniciar polling al cargar la página (cada 2 segundos)
    checkNuevosMensajes();
    notifInterval = setInterval(checkNuevosMensajes, 2000);

    // --- Renderizar chats (una sola vez al abrir) ---
    function renderChats(chats) {
        chatsContainer.innerHTML = '';

        if (chats.length === 0) {
            chatsContainer.innerHTML = '<p style="text-align:center; color:#64748b; margin-top:20px;">No tienes mensajes recientes.</p>';
            return;
        }

        chats.forEach(chat => {
            const chatRow = document.createElement('div');
            chatRow.style.cssText = "display:flex; align-items:center; padding:15px; border-bottom:1px solid #f1f5f9; cursor:pointer;";
            
            chatRow.addEventListener('click', () => {
                window.location.href = `chat.html?idTrabajo=${chat.idTrabajo}&receptor=${chat.idReceptor}`;
            });

            const img = document.createElement('img');
            img.src = `${window.API_BASE_URL}/trabajo/${chat.idTrabajo}/imagen_index/0`;
            img.style.cssText = "width:50px; height:50px; border-radius:50%; object-fit:cover; margin-right:15px; background:#e2e8f0;";
            img.onerror = () => { img.src = "https://via.placeholder.com/50?text=IMG"; };

            const textDiv = document.createElement('div');
            textDiv.style.cssText = "flex:1; overflow:hidden;";

            const nameRow = document.createElement('div');
            nameRow.style.cssText = "display:flex; justify-content:space-between; align-items:baseline;";
            const nameSpan = document.createElement('span');
            nameSpan.style.cssText = "font-weight:700; color:#1e293b; font-size:1.05rem;";
            nameSpan.textContent = chat.nombreUsuario;

            const dateSpan = document.createElement('span');
            dateSpan.style.cssText = "font-size:0.75rem; color:#94a3b8;";
            dateSpan.textContent = chat.fechaUltimoMensaje || '';
            
            nameRow.appendChild(nameSpan);
            nameRow.appendChild(dateSpan);

            const jobSpan = document.createElement('div');
            jobSpan.style.cssText = "font-size:0.85rem; color:#5e17eb; font-weight:600; margin-top:2px;";
            jobSpan.textContent = "📍 " + chat.tituloTrabajo;

            textDiv.appendChild(nameRow);
            textDiv.appendChild(jobSpan);

            chatRow.appendChild(img);
            chatRow.appendChild(textDiv);
            chatsContainer.appendChild(chatRow);
        });
    }

    openMailbox.addEventListener('click', async () => {
        mailboxDrawer.style.display = 'flex';
        chatsContainer.innerHTML = '<p style="text-align:center; color:#64748b; margin-top:20px;">Cargando chats...</p>';
        
        // Ocultar badge al abrir el buzón
        badge.style.display = 'none';

        const myId = localStorage.getItem('idAnimalLover');
        if (!myId) return;

        try {
            const res = await window.apiFetch(`/chats?idAnimalLover=${myId}`);
            if (res && res.ok) {
                const chats = await res.json();
                renderChats(chats);

                // Actualizar el último ID conocido para el polling
                // Usamos el endpoint de mensajes para obtener el ID más reciente recibido
                try {
                    const resAll = await window.apiFetch(`/mensajes/hay-nuevos?idAnimalLover=${myId}&ultimoIdMensaje=999999999`);
                    // No importa el resultado, lo que importa es que al abrir el buzón
                    // marcamos como "vistos" actualizando el ultimoIdConocido
                } catch(e) {}

                // Buscar el ID más alto de los mensajes recibidos para sincronizar
                for (const chat of chats) {
                    try {
                        const resMsg = await window.apiFetch(`/mensaje?idAnimalLover=${myId}&idOtroAnimalLover=${chat.idReceptor}&idTrabajo=${chat.idTrabajo}`);
                        if (resMsg && resMsg.ok) {
                            const mensajes = await resMsg.json();
                            if (mensajes.length > 0) {
                                const maxId = Math.max(...mensajes.map(m => m.idMensaje));
                                if (maxId > ultimoIdConocido) {
                                    ultimoIdConocido = maxId;
                                }
                            }
                        }
                    } catch(e) {}
                }
                localStorage.setItem('ultimoIdMensajeRecibido', String(ultimoIdConocido));

            } else {
                chatsContainer.innerHTML = '<p style="text-align:center; color:red; margin-top:20px;">Error al cargar chats.</p>';
            }
        } catch (e) {
            console.error(e);
            chatsContainer.innerHTML = '<p style="text-align:center; color:red; margin-top:20px;">Error de red.</p>';
        }
    });

    closeMailbox.addEventListener('click', () => {
        mailboxDrawer.style.display = 'none';
    });
});