let currentImageIndex = 0;
let totalImages = 0;

document.addEventListener('DOMContentLoaded', async () => {
    const idTrabajo = localStorage.getItem('idTrabajoSeleccionado');
    if (!idTrabajo) {
        alert('No se ha seleccionado ningún trabajo.');
        window.location.href = 'servicios.html';
        return;
    }

    try {
        const res = await window.apiFetch(`/trabajo?id=${idTrabajo}`);
        if (!res || !res.ok) {
            alert('No se pudieron obtener los detalles del trabajo.');
            window.location.href = 'servicios.html';
            return;
        }

        const job = await res.json();
        
        document.getElementById('jobTitle').textContent = job.nombre;
        document.getElementById('jobDesc').textContent = job.descripcion;
        document.getElementById('jobLocation').textContent = 'Ubicación: ' + job.ubicacion;
        document.getElementById('jobPrice').textContent = 'Pago: $' + job.monto;
        document.getElementById('jobDate').textContent = job.fechaPublicacion;

        // Cargar imágenes
        const track = document.getElementById('carouselTrack');
        const btnPrev = document.getElementById('btnPrevImg');
        const btnNext = document.getElementById('btnNextImg');

        try {
            const resImg = await window.apiFetch(`/trabajo/${job.idTrabajo}/imagenes_info`);
            if (resImg && resImg.ok) {
                const info = await resImg.json();
                totalImages = info.count;
            }
        } catch(e) {
            console.error("No se pudo obtener la info de imagenes", e);
        }

        if (totalImages > 0) {
            for (let i = 0; i < totalImages; i++) {
                const imgEl = document.createElement('img');
                imgEl.src = `${window.API_BASE_URL}/trabajo/${job.idTrabajo}/imagen_index/${i}`;
                imgEl.onerror = () => { imgEl.src = "https://via.placeholder.com/300x180?text=Error"; };
                track.appendChild(imgEl);
            }
            if (totalImages > 1) {
                btnPrev.style.display = 'flex';
                btnNext.style.display = 'flex';
                
                btnNext.onclick = () => {
                    currentImageIndex = (currentImageIndex + 1) % totalImages;
                    track.style.transform = `translateX(-${currentImageIndex * 100}%)`;
                };
                btnPrev.onclick = () => {
                    currentImageIndex = (currentImageIndex - 1 + totalImages) % totalImages;
                    track.style.transform = `translateX(-${currentImageIndex * 100}%)`;
                };
            }
        } else {
            const imgEl = document.createElement('img');
            imgEl.src = "https://via.placeholder.com/300x180?text=Sin+Imagen";
            track.appendChild(imgEl);
        }

        const btnAceptar = document.getElementById('btnAceptar');
        const btnContactar = document.getElementById('btnContactar');
        const myId = localStorage.getItem('idAnimalLover');

        // Verificar si ya fue aceptado
        let yaAceptado = false;
        try {
            const resCheck = await window.apiFetch(`/trabajo-aceptado/check?idTrabajo=${job.idTrabajo}`);
            if (resCheck && resCheck.ok) {
                const checkData = await resCheck.json();
                yaAceptado = checkData.aceptado;
            }
        } catch(e) { console.error(e); }

        if (yaAceptado) {
            btnAceptar.textContent = '✓ Ya aceptado';
            btnAceptar.disabled = true;
            btnAceptar.style.opacity = '0.6';
            btnAceptar.style.cursor = 'not-allowed';

            btnContactar.textContent = 'No disponible';
            btnContactar.disabled = true;
            btnContactar.style.opacity = '0.6';
            btnContactar.style.cursor = 'not-allowed';
        } else {
            // Lógica de aceptar
            btnAceptar.addEventListener('click', async () => {
                if (String(job.idAnimalLoverPublicador) === String(myId)) {
                    alert("No puedes aceptar tu propio trabajo.");
                    return;
                }

                if (!confirm("¿Estás seguro de que quieres aceptar este trabajo?")) {
                    return;
                }

                try {
                    const resAceptar = await window.apiFetch('/trabajo-aceptado', {
                        method: 'POST',
                        body: JSON.stringify({
                            idTrabajo: job.idTrabajo,
                            idAnimalLoverTrabajador: parseInt(myId),
                            fechaAceptacion: window.getFormattedDateMX(),
                            estadoTrabajo: 'Pendiente'
                        })
                    });

                    if (resAceptar && resAceptar.ok) {
                        alert("¡Trabajo aceptado exitosamente! Puedes verlo en 'Trabajos Aceptados'.");
                        btnAceptar.textContent = '✓ Aceptado';
                        btnAceptar.disabled = true;
                        btnAceptar.style.opacity = '0.6';
                        
                        btnContactar.textContent = 'No disponible';
                        btnContactar.disabled = true;
                        btnContactar.style.opacity = '0.6';
                    } else if (resAceptar) {
                        const error = await resAceptar.json();
                        alert("No se pudo aceptar el trabajo: " + error.detail);
                    }
                } catch (err) {
                    console.error("Error aceptando trabajo:", err);
                    alert("Error de red al intentar aceptar el trabajo.");
                }
            });

            // Lógica de contacto
            btnContactar.addEventListener('click', () => {
                if (String(job.idAnimalLoverPublicador) === String(myId)) {
                    alert("No puedes contactarte a ti mismo.");
                    return;
                }
                window.location.href = `chat.html?idTrabajo=${job.idTrabajo}&receptor=${job.idAnimalLoverPublicador}`;
            });
        }

    } catch (e) {
        console.error("Error cargando el trabajo:", e);
        alert('Ocurrió un error al cargar la información.');
        window.location.href = 'servicios.html';
    }
});
