document.addEventListener('DOMContentLoaded', async () => {
    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }

    const emptyState = document.getElementById("emptyState");
    const jobList = document.getElementById("jobList");

    try {
        const response = await window.apiFetch('/trabajos');
        let trabajos = [];
        if (response && response.ok) {
            trabajos = await response.json();
        } else if (response && response.status === 404) {
            trabajos = [];
        }

        // Filtrar solo mis publicaciones
        const misTrabajos = trabajos.filter(t => String(t.idAnimalLoverPublicador) === String(myIdStr));

        if (misTrabajos.length === 0) {
            if(emptyState) emptyState.style.display = "block";
            if(jobList) jobList.style.display = "none";
        } else {
            if(emptyState) emptyState.style.display = "none";
            if(jobList) {
                jobList.style.display = "block";
                jobList.innerHTML = '';

                for (const job of misTrabajos) {
                    // Verificar si está completado usando trabajo_aceptado
                    let isCompleted = false;
                    try {
                        const resCheck = await window.apiFetch(`/trabajo-aceptado/check?idTrabajo=${job.idTrabajo}`);
                        if (resCheck && resCheck.ok) {
                            const checkData = await resCheck.json();
                            isCompleted = checkData.completado;
                        }
                    } catch(e) { console.error(e); }

                    const article = document.createElement('article');
                    article.className = 'job-card';
                    if (isCompleted) {
                        article.style.opacity = '0.7';
                    }
                    
                    const img = document.createElement('img');
                    img.src = `${window.API_BASE_URL}/trabajo/${job.idTrabajo}/imagen`;
                    img.className = 'job-image';
                    img.style.width = '100%';
                    img.style.height = '180px';
                    img.style.objectFit = 'cover';
                    img.style.borderRadius = '12px 12px 0 0';
                    img.onerror = () => { img.src = "https://via.placeholder.com/300x180?text=Sin+Imagen"; };

                    const details = document.createElement('div');
                    details.className = 'card-details';
                    details.style.padding = '15px';

                    const mainInfo = document.createElement('div');
                    mainInfo.className = 'main-info';

                    const estadoBadge = isCompleted 
                        ? `<span style="display:inline-block; background:#dcfce7; color:#15803d; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; margin-bottom:8px;">✓ Completado</span>`
                        : `<span style="display:inline-block; background:#fef3c7; color:#b45309; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; margin-bottom:8px;">● Activo</span>`;

                    mainInfo.innerHTML = `
                        ${estadoBadge}
                        <p style="font-size:1.1rem; margin-bottom:8px;"><strong>${job.nombre}</strong></p>
                        <p style="margin:4px 0; color:#555; font-size:0.9rem;">Tipo: <span>${job.tipoTrabajo}</span></p>
                        <p style="margin:4px 0; color:#555; font-size:0.9rem;">Pago: <span>$${job.monto}</span></p>
                        <p style="margin:4px 0; color:#555; font-size:0.9rem;">Publicado: <span>${job.fechaPublicacion}</span></p>
                    `;

                    const actions = document.createElement('div');
                    actions.className = 'actions';
                    actions.style.display = 'flex';
                    actions.style.gap = '10px';
                    actions.style.marginTop = '15px';

                    if (!isCompleted) {
                        // Botón Editar
                        const btnEdit = document.createElement('button');
                        btnEdit.className = 'btn btn-outline';
                        btnEdit.innerHTML = '<i class="fas fa-edit"></i> Editar';
                        btnEdit.style.flex = '1';
                        btnEdit.onclick = () => {
                            window.location.href = `publicar_trabajo.html?edit=${job.idTrabajo}`;
                        };

                        // Botón Completar
                        const btnComplete = document.createElement('button');
                        btnComplete.className = 'btn';
                        btnComplete.innerHTML = '<i class="fas fa-check"></i> Completar';
                        btnComplete.style.cssText = 'flex:1; background-color:#22c55e; color:#fff; border:none; border-radius:12px; padding:10px; font-weight:600; cursor:pointer;';
                        btnComplete.onclick = async () => {
                            if(confirm("¿Marcar esta publicación como completada? Ya no aparecerá en Servicios, pero se conservará en tu historial.")) {
                                try {
                                    const resComp = await window.apiFetch(`/trabajo-aceptado/completar?idTrabajo=${job.idTrabajo}`, {
                                        method: 'POST'
                                    });
                                    if (resComp && resComp.ok) {
                                        alert("Publicación marcada como completada.");
                                        location.reload();
                                    } else {
                                        const error = await resComp.json();
                                        alert("Error: " + error.detail);
                                    }
                                } catch(e) {
                                    console.error(e);
                                    alert("Error de red.");
                                }
                            }
                        };

                        // Botón Dar de baja
                        const btnBaja = document.createElement('button');
                        btnBaja.className = 'btn btn-deactivate';
                        btnBaja.innerHTML = '<i class="fas fa-trash"></i> Baja';
                        btnBaja.style.cssText = 'flex:1; background-color:#e74c3c; color:#fff; border:none; border-radius:12px; padding:10px; font-weight:600; cursor:pointer;';
                        btnBaja.onclick = async () => {
                            if(confirm("¿Estás seguro de que quieres eliminar esta publicación? Esto también borrará los chats e imágenes asociadas.")) {
                                try {
                                    const resDel = await window.apiFetch(`/trabajo?id=${job.idTrabajo}`, {
                                        method: 'DELETE'
                                    });
                                    if (resDel && resDel.ok) {
                                        alert("Publicación eliminada del sistema exitosamente.");
                                        location.reload();
                                    } else {
                                        const error = await resDel.json();
                                        alert("No se pudo eliminar: " + error.detail);
                                    }
                                } catch(e) {
                                    console.error(e);
                                    alert("Error de red.");
                                }
                            }
                        };

                        actions.appendChild(btnEdit);
                        actions.appendChild(btnComplete);
                        actions.appendChild(btnBaja);
                    } else {
                        // Completado: solo botón de eliminar del historial
                        const btnBaja = document.createElement('button');
                        btnBaja.className = 'btn btn-deactivate';
                        btnBaja.innerHTML = '<i class="fas fa-trash"></i> Eliminar del historial';
                        btnBaja.style.cssText = 'flex:1; background-color:#e74c3c; color:#fff; border:none; border-radius:12px; padding:10px; font-weight:600; cursor:pointer;';
                        btnBaja.onclick = async () => {
                            if(confirm("¿Eliminar esta publicación completada del historial? Esto no se puede deshacer.")) {
                                try {
                                    const resDel = await window.apiFetch(`/trabajo?id=${job.idTrabajo}`, {
                                        method: 'DELETE'
                                    });
                                    if (resDel && resDel.ok) {
                                        alert("Publicación eliminada del historial.");
                                        location.reload();
                                    } else {
                                        const error = await resDel.json();
                                        alert("No se pudo eliminar: " + error.detail);
                                    }
                                } catch(e) {
                                    console.error(e);
                                    alert("Error de red.");
                                }
                            }
                        };
                        actions.appendChild(btnBaja);
                    }

                    details.appendChild(mainInfo);
                    details.appendChild(actions);

                    article.style.backgroundColor = '#fff';
                    article.style.borderRadius = '12px';
                    article.style.boxShadow = '0 4px 10px rgba(0,0,0,0.05)';
                    article.style.marginBottom = '20px';
                    article.appendChild(img);
                    article.appendChild(details);

                    jobList.appendChild(article);
                }
            }
        }
    } catch (e) {
        console.error("Error obteniendo trabajos:", e);
        if(emptyState) {
            emptyState.style.display = "block";
            emptyState.querySelector('h2').textContent = "Error al cargar publicaciones.";
            emptyState.querySelector('p').textContent = "Inténtalo más tarde.";
        }
        if(jobList) jobList.style.display = "none";
    }
});