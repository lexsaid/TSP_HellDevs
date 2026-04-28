let currentImageIndex = 0;
let totalImages = 0;

document.addEventListener('DOMContentLoaded', async () => {
    // Recuperar datos del albergue guardados desde servicios.js
    const albDataRaw = localStorage.getItem('albergueSeleccionado');
    if (!albDataRaw) {
        alert('No se ha seleccionado ningún albergue.');
        window.location.href = 'servicios.html';
        return;
    }

    let albData;
    try {
        albData = JSON.parse(albDataRaw);
    } catch (e) {
        alert('Error al leer los datos del albergue.');
        window.location.href = 'servicios.html';
        return;
    }

    const alb = albData.albergue;
    const dueno = albData.dueño || albData.dueno;

    // Rellenar la información
    document.getElementById('albNombre').textContent = alb.nombre || 'Sin nombre';
    document.getElementById('albPreRequisitos').textContent =
        alb.preRequisitos ? `Pre-requisitos: ${alb.preRequisitos}` : 'Sin pre-requisitos especificados.';
    document.getElementById('albUbicacion').textContent = 'Ubicación: ' + (alb.ubicacion || '--');
    document.getElementById('albCosto').textContent = `Costo: $${alb.costoDiario ?? '--'} / día`;
    document.getElementById('albCapacidad').textContent = `Capacidad: ${alb.capacidad ?? '--'}`;
    document.getElementById('albPreferencia').textContent = `Preferencia: ${alb.preferencia || '--'}`;

    // Cargar imagenes del albergue
    const track = document.getElementById('carouselTrack');
    const btnPrev = document.getElementById('btnPrevImg');
    const btnNext = document.getElementById('btnNextImg');

    try {
        const resImg = await window.apiFetch(`/albergue/${alb.idAlbergue}/imagenes_info`);
        if (resImg && resImg.ok) {
            const info = await resImg.json();
            totalImages = info.count;
        }
    } catch (e) {
        console.error('No se pudo obtener la info de imagenes', e);
    }

    if (totalImages > 0) {
        for (let i = 0; i < totalImages; i++) {
            const imgEl = document.createElement('img');
            imgEl.src = `${window.API_BASE_URL}/albergue/${alb.idAlbergue}/imagen_index/${i}`;
            imgEl.onerror = () => { imgEl.src = 'https://via.placeholder.com/300x180?text=Error'; };
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
        imgEl.src = 'https://via.placeholder.com/300x180?text=Sin+Imagen';
        track.appendChild(imgEl);
    }

    // Lógica del botón Contactar
    const btnContactar = document.getElementById('btnContactar');
    const myId = localStorage.getItem('idAnimalLover');

    if (!dueno || !dueno.idAnimalLover) {
        btnContactar.textContent = 'Información de dueño no disponible';
        btnContactar.disabled = true;
        btnContactar.style.opacity = '0.6';
        btnContactar.style.cursor = 'not-allowed';
        return;
    }

    if (String(dueno.idAnimalLover) === String(myId)) {
        btnContactar.textContent = 'Esta es tu publicación';
        btnContactar.disabled = true;
        btnContactar.style.opacity = '0.6';
        btnContactar.style.cursor = 'not-allowed';
        return;
    }

    btnContactar.addEventListener('click', () => {
        // Convención: idTrabajo negativo indica contexto de albergue.
        // El backend y el chat.js detectan esto para mostrar los datos correctos.
        const idTrabajoAlbergue = -(alb.idAlbergue);
        window.location.href = `chat.html?idTrabajo=${idTrabajoAlbergue}&receptor=${dueno.idAnimalLover}`;
    });
});
