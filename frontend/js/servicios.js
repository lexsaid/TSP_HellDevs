document.addEventListener('DOMContentLoaded', async () => {
    // const myIdStr = localStorage.getItem('idAnimalLover');
    // if (!myIdStr) {
    //     window.location.href = 'login.html';
    //     return;
    // }

    // // Validar sesión
    // try {
    //     await window.apiFetch(`/animalLover?id=${myIdStr}`);
    // } catch (e) {
    //     console.error("Error validando sesión:", e);
    // }

    const emptyState = document.getElementById("emptyState");
    const jobList = document.getElementById("jobList");

    try {
        const response = await window.apiFetch('/trabajos');
        let trabajos = [];
        if (response && response.ok) {
            trabajos = await response.json();
        }

        // Filtrar trabajos completados usando /trabajo-aceptado/check
        const trabajosVisibles = [];
        for (const job of trabajos) {
            try {
                const resCheck = await window.apiFetch(`/trabajo-aceptado/check?idTrabajo=${job.idTrabajo}`);
                if (resCheck && resCheck.ok) {
                    const checkData = await resCheck.json();
                    if (checkData.completado) continue; // No mostrar completados
                    job._yaAceptado = checkData.aceptado;
                }
            } catch(e) { console.error(e); }
            trabajosVisibles.push(job);
        }

        if (trabajosVisibles.length === 0) {
            if(emptyState) emptyState.style.display = "block";
            if(jobList) jobList.style.display = "none";
        } else {
            if(emptyState) emptyState.style.display = "none";
            if(jobList) {
                jobList.style.display = "block";
                jobList.innerHTML = '';

                for (const job of trabajosVisibles) {
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
                        btn.style.cursor = 'not-allowed';
                        btn.style.boxShadow = 'none';
                    } else if (job._yaAceptado) {
                        btn.className = 'btn-more disabled-btn';
                        btn.textContent = '✓ Ya aceptado';
                        btn.disabled = true;
                        btn.style.background = '#22c55e';
                        btn.style.color = 'white';
                        btn.style.cursor = 'not-allowed';
                        btn.style.boxShadow = 'none';
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

                    jobList.appendChild(article);
                }
            }
        }
    } catch (e) {
        console.error("Error obteniendo trabajos:", e);
        if(emptyState) {
            emptyState.style.display = "block";
            emptyState.querySelector('h2').textContent = "Error al cargar servicios.";
            emptyState.querySelector('p').textContent = "Inténtalo más tarde.";
        }
        if(jobList) jobList.style.display = "none";
    }
});