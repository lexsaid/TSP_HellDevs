document.addEventListener('DOMContentLoaded', async () => {
    // 1. Validar sesión
    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }

    try {
        await window.apiFetch(`/animalLover?id=${myIdStr}`);
    } catch (e) {
        console.error("Error validando sesión:", e);
        // Si hay error de auth, el apiFetch redirigirá al login si está configurado así,
        // o podemos manejarlo aquí.
    }

    const filtroComunidad = document.getElementById('filtroComunidad');
    const feedComunidad = document.getElementById('feedComunidad');

    // Función para cargar publicaciones
    async function cargarPublicaciones() {
        const tipo = filtroComunidad.value; // 'perdidas' o 'adopcion'
        feedComunidad.innerHTML = '<p style="text-align:center; color:#64748b;">Cargando publicaciones...</p>';

        try {
            let endpoint = tipo === 'perdidas' ? '/mascotas_perdidas' : '/adopciones';
            const res = await window.apiFetch(endpoint);
            let publicaciones = [];
            if (res && res.ok) {
                publicaciones = await res.json();
            } else if (res && res.status === 404) {
                publicaciones = [];
            }

            if (!publicaciones || publicaciones.length === 0) {
                feedComunidad.innerHTML = `
                    <div style="text-align: center; color: #64748b; padding: 20px; background: white; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                        <i class="fas fa-search" style="font-size: 2rem; color: #e2e8f0; margin-bottom: 10px;"></i>
                        <p>No hay publicaciones de este tipo en este momento.</p>
                    </div>
                `;
                return;
            }

            feedComunidad.innerHTML = ''; // Limpiar

            publicaciones.forEach(pub => {
                const card = crearCardPublicacion(pub, tipo);
                feedComunidad.appendChild(card);
            });

        } catch (error) {
            console.error("Error al cargar publicaciones:", error);
            feedComunidad.innerHTML = '<p style="text-align:center; color: #850cc2;">De momeinto no hay publicaciones disponibles.</p>';
        }
    }

    function crearCardPublicacion(pub, tipo) {
        // En el backend, las respuestas vienen como MascotaPerdidaDetalle o AdopcionDetalle
        // que contienen { mascotaPerdida/adopcion: ..., dueño/publicador: ... }
        const data = tipo === 'perdidas' ? pub.mascotaPerdida : pub.adopcion;
        const autor = tipo === 'perdidas' ? pub.dueño : pub.publicador;

        const article = document.createElement('article');
        article.style.background = 'white';
        article.style.borderRadius = '20px';
        article.style.overflow = 'hidden';
        article.style.boxShadow = '0 10px 20px rgba(0,0,0,0.05)';
        article.style.display = 'flex';
        article.style.flexDirection = 'column';
        article.style.animation = 'fadeUp 0.5s ease forwards';

        // Imagen (Placeholder por ahora o implementar endpoint de imagen)
        const imgContainer = document.createElement('div');
        imgContainer.style.position = 'relative';
        imgContainer.style.height = '200px';
        imgContainer.style.width = '100%';

        const img = document.createElement('img');
        // Usar el endpoint real de imagen para el animal
        img.src = `${window.API_BASE_URL}/animal/${data.idAnimal}/imagen`;
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        img.onerror = () => {
            img.src = `https://via.placeholder.com/400x200?text=${data.nombre}`;
        };
        
        const badge = document.createElement('span');
        badge.style.position = 'absolute';
        badge.style.top = '15px';
        badge.style.right = '15px';
        badge.style.padding = '6px 12px';
        badge.style.borderRadius = '10px';
        badge.style.fontSize = '0.75rem';
        badge.style.fontWeight = '700';
        badge.style.color = 'white';
        
        if (tipo === 'perdidas') {
            badge.style.background = '#ef4444';
            badge.textContent = 'PERDIDO';
        } else {
            badge.style.background = '#10b981';
            badge.textContent = 'EN ADOPCIÓN';
        }

        imgContainer.appendChild(img);
        imgContainer.appendChild(badge);

        // Info
        const info = document.createElement('div');
        info.style.padding = '15px';

        const header = document.createElement('div');
        header.style.display = 'flex';
        header.style.justifyContent = 'space-between';
        header.style.alignItems = 'flex-start';
        header.style.marginBottom = '10px';

        header.innerHTML = `
            <div>
                <h3 style="margin:0; font-size:1.1rem; color:#1e293b;">${data.nombre}</h3>
                <p style="margin:2px 0 0; font-size:0.85rem; color:#64748b;"><i class="fas fa-map-marker-alt"></i> ${data.direccion}</p>
            </div>
            <div style="text-align:right;">
                <p style="margin:0; font-weight:700; color:#5e17eb; font-size:1rem;">${tipo === 'perdidas' ? '$' + data.recompensa : 'Gratis'}</p>
                <p style="margin:0; font-size:0.7rem; color:#94a3b8;">${tipo === 'perdidas' ? 'Recompensa' : 'Costo'}</p>
            </div>
        `;

        const detailsGrid = document.createElement('div');
        detailsGrid.style.display = 'grid';
        detailsGrid.style.gridTemplateColumns = '1fr 1fr';
        detailsGrid.style.gap = '8px';
        detailsGrid.style.marginBottom = '15px';
        detailsGrid.style.fontSize = '0.85rem';

        detailsGrid.innerHTML = `
            <div style="background:#f8fafc; padding:8px; border-radius:10px; color:#475569;">
                <strong>Tipo:</strong> ${data.tipoAnimal}
            </div>
            <div style="background:#f8fafc; padding:8px; border-radius:10px; color:#475569;">
                <strong>Tamaño:</strong> ${data.tamanio}
            </div>
            <div style="background:#f8fafc; padding:8px; border-radius:10px; color:#475569;">
                <strong>Edad:</strong> ${data.edad} meses
            </div>
            <div style="background:#f8fafc; padding:8px; border-radius:10px; color:#475569;">
                <strong>Color:</strong> ${data.color}
            </div>
            <div style="background:#f8fafc; padding:8px; border-radius:10px; color:#475569; grid-column: span 2;">
                <strong>Condición:</strong> ${data.discapacidad || 'Ninguna'}
            </div>
            ${tipo === 'adopcion' ? `
            <div style="background:#f8fafc; padding:8px; border-radius:10px; color:#475569; grid-column: span 2;">
                <strong>Vacunas:</strong> ${data.vacunas || 'No especificadas'}
            </div>
            ` : ''}
        `;

        const footer = document.createElement('div');
        footer.style.borderTop = '1.5px solid #f1f5f9';
        footer.style.paddingTop = '12px';
        footer.style.display = 'flex';
        footer.style.justifyContent = 'space-between';
        footer.style.alignItems = 'center';

        const autorInfo = document.createElement('div');
        autorInfo.style.display = 'flex';
        autorInfo.style.alignItems = 'center';
        autorInfo.style.gap = '8px';
        autorInfo.innerHTML = `
            <div style="width:30px; height:30px; background:#e2e8f0; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#64748b;">
                <i class="fas fa-user" style="font-size:0.8rem;"></i>
            </div>
            <span style="font-size:0.8rem; font-weight:600; color:#475569;">${autor.nombre}</span>
        `;

        const verMasBtn = document.createElement('button');
        verMasBtn.textContent = 'Ver mas';
        verMasBtn.style.background = '#5e17eb';
        verMasBtn.style.color = 'white';
        verMasBtn.style.border = 'none';
        verMasBtn.style.padding = '8px 16px';
        verMasBtn.style.borderRadius = '12px';
        verMasBtn.style.fontSize = '0.8rem';
        verMasBtn.style.fontWeight = '700';
        verMasBtn.style.cursor = 'pointer';

        verMasBtn.addEventListener('click', () => {
            if (tipo === 'perdidas') {
                window.location.href = `ver_mascota_perdida.html?idAnimal=${data.idAnimal}`;
            } else {
                window.location.href = `ver_adopcion.html?idAnimal=${data.idAnimal}`;
            }
        });

        footer.appendChild(autorInfo);
        footer.appendChild(verMasBtn);

        info.appendChild(header);
        info.appendChild(detailsGrid);
        info.appendChild(footer);

        article.appendChild(imgContainer);
        article.appendChild(info);

        return article;
    }

    // Event listener para el filtro
    filtroComunidad.addEventListener('change', cargarPublicaciones);

    // Botón añadir publicación
    const btnAddPost = document.getElementById('btnAddPost');
    if (btnAddPost) {
        btnAddPost.addEventListener('click', () => {
            if (filtroComunidad.value === 'perdidas') {
                window.location.href = 'pubMascotaPerdida.html';
            } else if (filtroComunidad.value === 'adopcion') {
                window.location.href = 'pubAdopcion.html';
            }
        });
    }

    // Carga inicial
    cargarPublicaciones();
});
