document.addEventListener('DOMContentLoaded', async () => {
    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }

    // Validar sesión
    try {
        await window.apiFetch(`/animalLover?id=${myIdStr}`);
    } catch (e) {
        console.error("Error validando sesión:", e);
    }

    const filtroServicios = document.getElementById('filtroServicios');
    const jobList = document.getElementById("jobList");
    const emptyState = document.getElementById("emptyState");

    async function cargarServicios() {
        const tipo = filtroServicios ? filtroServicios.value : 'trabajos'; 
        jobList.innerHTML = '<p style="text-align:center; color:#64748b; padding:20px;">Cargando...</p>';
        
        try {
            if (tipo === 'trabajos') {
                const response = await window.apiFetch('/trabajos');
                const trabajos = (response && response.ok) ? await response.json() : [];

                // Filtrar trabajos completados
                const trabajosVisibles = [];
                for (const job of trabajos) {
                    try {
                        const checkRes = await window.apiFetch(`/trabajo-aceptado/check?idTrabajo=${job.idTrabajo}`);
                        const checkData = (checkRes && checkRes.ok) ? await checkRes.json() : null;
                        
                        if (checkData && checkData.completado) continue; 
                        job._yaAceptado = checkData ? checkData.aceptado : false;
                    } catch(e) { console.error(e); }
                    trabajosVisibles.push(job);
                }

                if (trabajosVisibles.length === 0) {
                    mostrarEstadoVacio();
                } else {
                    renderizarTrabajos(trabajosVisibles);
                }
            } else {
                // Cargar Albergues
                const resAlb = await window.apiFetch('/albergues');
                const albergues = (resAlb && resAlb.ok) ? await resAlb.json() : [];
                
                if (!albergues || albergues.length === 0) {
                    mostrarEstadoVacio();
                } else {
                    renderizarAlbergues(albergues);
                }
            }
        } catch (e) {
            console.error("Error obteniendo servicios:", e);
            mostrarEstadoVacio(true);
        }
    }

    function mostrarEstadoVacio(error = false) {
        if(emptyState) {
            emptyState.style.display = "block";
            if(error) {
                emptyState.querySelector('h2').textContent = "Error al cargar servicios.";
            } else {
                emptyState.querySelector('h2').textContent = "No hay servicios disponibles.";
            }
        }
        if(jobList) jobList.style.display = "none";
    }

    function renderizarTrabajos(trabajos) {
        if(emptyState) emptyState.style.display = "none";
        jobList.style.display = "flex";
        jobList.innerHTML = '';

        for (const job of trabajos) {
            const article = crearCardTrabajo(job);
            jobList.appendChild(article);
        }
    }

    function crearCardTrabajo(job) {
        const article = document.createElement('article');
        article.className = 'job-card';

        const img = document.createElement('img');
        img.src = `${window.API_BASE_URL}/trabajo/${job.idTrabajo}/imagen`;
        img.className = 'job-image';
        img.onerror = () => {
            img.src = "https://via.placeholder.com/300x180?text=Sin+Imagen";
        };

        const details = document.createElement('div');
        details.className = 'card-details';

        const infoRow = document.createElement('div');
        infoRow.className = 'info-row';

        const mainInfo = document.createElement('div');
        mainInfo.className = 'main-info';
        mainInfo.innerHTML = `
            <p><strong>${job.nombre}</strong></p>
            <p>Tipo: <span>${job.tipoTrabajo}</span></p>
            <p>Pago: <span>$${job.monto}</span></p>
            <p>Ubicación: <span>${job.ubicacion}</span></p>
        `;

        const expiryTimer = document.createElement('div');
        expiryTimer.className = 'expiry-timer';
        expiryTimer.innerHTML = `Publicado:<br><span class="time-left">${job.fechaPublicacion}</span>`;

        infoRow.appendChild(mainInfo);
        infoRow.appendChild(expiryTimer);
        
        const btn = document.createElement('button');

        if (String(job.idAnimalLoverPublicador) === String(myIdStr)) {
            btn.className = 'btn-more disabled-btn';
            btn.textContent = 'Publicación propia';
            btn.disabled = true;
            btn.style.background = '#cbd5e1';
        } else if (job._yaAceptado) {
            btn.className = 'btn-more disabled-btn';
            btn.textContent = '✓ Ya aceptado';
            btn.disabled = true;
            btn.style.background = '#22c55e';
            btn.style.color = 'white';
        } else {
            btn.className = 'btn-more';
            btn.textContent = 'Ver más';
            btn.onclick = () => {
                localStorage.setItem('idTrabajoSeleccionado', job.idTrabajo);
                window.location.href = 'ver_trabajo_del_otro.html';
            };
        }

        details.appendChild(infoRow);
        details.appendChild(btn);
        article.appendChild(img);
        article.appendChild(details);
        return article;
    }

    function renderizarAlbergues(albergues) {
        if(emptyState) emptyState.style.display = "none";
        jobList.style.display = "flex";
        jobList.innerHTML = '';

        for (const item of albergues) {
            const alb = item.albergue;

            const article = document.createElement('article');
            article.className = 'job-card';

            const img = document.createElement('img');
            img.src = `${window.API_BASE_URL}/albergue/${alb.idAlbergue}/imagen`;
            img.className = 'job-image';
            img.onerror = () => {
                img.src = "https://via.placeholder.com/300x180?text=Albergue";
            };

            const details = document.createElement('div');
            details.className = 'card-details';

            details.innerHTML = `
                <div style="margin-bottom:10px;">
                    <p><strong>${alb.nombre}</strong></p>
                    <p style="font-size:0.85rem; color:#64748b;"><i class="fas fa-map-marker-alt"></i> ${alb.ubicacion}</p>
                    <p style="font-size:0.85rem; color:#475569; margin-top:5px;">
                        Capacidad: ${alb.capacidad} | Preferencia: ${alb.preferencia}
                    </p>
                    <p style="font-size:0.85rem; color:#5e17eb; font-weight:700;">
                        Costo: $${alb.costoDiario} / día
                    </p>
                </div>
            `;

            const btnContactarAlb = document.createElement('button');
            if (String(alb.idAnimalLover) === String(myIdStr)) {
                btnContactarAlb.className = 'btn-more disabled-btn';
                btnContactarAlb.textContent = 'Publicación propia';
                btnContactarAlb.disabled = true;
                btnContactarAlb.style.background = '#cbd5e1';
            } else {
                btnContactarAlb.className = 'btn-more';
                btnContactarAlb.textContent = 'Ver más';
                btnContactarAlb.onclick = () => {
                    localStorage.setItem('albergueSeleccionado', JSON.stringify(item));
                    window.location.href = 'ver_albergue.html';
                };
            }
            details.appendChild(btnContactarAlb);

            article.appendChild(img);
            article.appendChild(details);
            jobList.appendChild(article);
        }
    }

    // Listener para el filtro
    if(filtroServicios) filtroServicios.addEventListener('change', cargarServicios);

    // Carga inicial
    cargarServicios();
});