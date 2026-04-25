document.addEventListener('DOMContentLoaded', async () => {
    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }
    
    const emptyState = document.getElementById("emptyState");
    const jobList = document.getElementById("jobList");

    try {
        // Fetch trabajos aceptados for the user
        const resAceptados = await window.apiFetch(`/trabajo-aceptado?idAnimalLoverTrabajador=${myIdStr}`);
        let aceptados = [];
        if (resAceptados && resAceptados.ok) {
            aceptados = await resAceptados.json();
        }

        if (aceptados.length === 0) {
            if(emptyState) emptyState.style.display = "block";
            if(jobList) jobList.style.display = "none";
            return;
        }

        // Fetch all jobs to get full details
        const resTrabajos = await window.apiFetch('/trabajos');
        let todosTrabajos = [];
        if (resTrabajos && resTrabajos.ok) {
            todosTrabajos = await resTrabajos.json();
        }

        // Filter out the jobs that are in the aceptados list
        const trabajosAceptadosIds = aceptados.map(a => a.idTrabajo);
        const trabajosFiltrados = todosTrabajos.filter(t => trabajosAceptadosIds.includes(t.idTrabajo));

        if (trabajosFiltrados.length === 0) {
            if(emptyState) emptyState.style.display = "block";
            if(jobList) jobList.style.display = "none";
        } else {
            if(emptyState) emptyState.style.display = "none";
            if(jobList) {
                jobList.style.display = "block";
                jobList.innerHTML = '';

                trabajosFiltrados.forEach(job => {
                    // Find the state from the aceptados list
                    const acceptedInfo = aceptados.find(a => a.idTrabajo === job.idTrabajo);
                    const estado = acceptedInfo ? acceptedInfo.estadoTrabajo : 'Pendiente';

                    const article = document.createElement('article');
                    article.className = 'job-card';
                    // We reuse job-card styling from traAceptados but structure it like a clean card
                    
                    const img = document.createElement('img');
                    img.src = `${window.API_BASE_URL}/trabajo/${job.idTrabajo}/imagen`;
                    img.className = 'job-image';
                    img.onerror = () => { img.src = "https://via.placeholder.com/300x180?text=Sin+Imagen"; };

                    const details = document.createElement('div');
                    details.className = 'card-details';

                    const infoRow = document.createElement('div');
                    infoRow.className = 'info-row';

                    const mainInfo = document.createElement('div');
                    mainInfo.className = 'main-info';
                    mainInfo.innerHTML = `
                        <p><strong>${job.nombre}</strong> <span class="badge ${estado === 'Terminado' ? 'done' : 'pending'}">${estado}</span></p>
                        <p>Tipo: <span>${job.tipoTrabajo}</span></p>
                        <p>Pago: <span>$${job.monto}</span></p>
                        <p>Ubicación: <span>${job.ubicacion}</span></p>
                    `;

                    infoRow.appendChild(mainInfo);
                    
                    const btnContainer = document.createElement('div');
                    btnContainer.style.display = 'flex';
                    btnContainer.style.gap = '10px';
                    btnContainer.style.marginTop = '15px';

                    const btnVer = document.createElement('button');
                    btnVer.className = 'btn btn-outline';
                    btnVer.innerHTML = '<i class="fas fa-search"></i> Ver detalles';
                    btnVer.onclick = () => {
                        localStorage.setItem('idTrabajoSeleccionado', job.idTrabajo);
                        window.location.href = 'ver_trabajo_aceptado.html';
                    };

                    const btnBaja = document.createElement('button');
                    btnBaja.className = 'btn btn-primary';
                    btnBaja.style.backgroundColor = '#e74c3c'; // red color for cancel
                    btnBaja.innerHTML = '<i class="fas fa-times"></i> Dar de baja';
                    btnBaja.onclick = async () => {
                        if (confirm('¿Estás seguro de que quieres dar de baja este trabajo aceptado?')) {
                            try {
                                const resDel = await window.apiFetch(`/trabajo-aceptado?idTrabajo=${job.idTrabajo}&idAnimalLoverTrabajador=${myIdStr}`, {
                                    method: 'DELETE'
                                });
                                if (resDel && resDel.ok) {
                                    alert('Trabajo dado de baja exitosamente.');
                                    location.reload();
                                } else {
                                    const error = await resDel.json();
                                    alert('Error: ' + error.detail);
                                }
                            } catch (error) {
                                console.error('Error:', error);
                                alert('Error de red al intentar dar de baja el trabajo.');
                            }
                        }
                    };

                    btnContainer.appendChild(btnVer);
                    btnContainer.appendChild(btnBaja);

                    details.appendChild(infoRow);
                    details.appendChild(btnContainer);

                    article.appendChild(img);
                    article.appendChild(details);

                    jobList.appendChild(article);
                });
            }
        }

    } catch (e) {
        console.error("Error obteniendo trabajos aceptados:", e);
        if(emptyState) {
            emptyState.style.display = "block";
            emptyState.querySelector('h2').textContent = "Error al cargar trabajos.";
            emptyState.querySelector('p').textContent = "Inténtalo más tarde.";
        }
        if(jobList) jobList.style.display = "none";
    }
});