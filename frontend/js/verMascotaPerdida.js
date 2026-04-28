let currentImageIndex = 0;
let totalImages = 0;

function getIdAnimal() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('idAnimal');
    return id ? parseInt(id) : null;
}

document.addEventListener('DOMContentLoaded', async () => {
    const idAnimal = getIdAnimal();
    if (!idAnimal) {
        alert('No se encontro la mascota.');
        window.location.href = 'comunidad.html';
        return;
    }

    let detalle;
    try {
        const res = await window.apiFetch(`/mascotas_perdidas/detalle?id_animal=${idAnimal}`);
        if (!res || !res.ok) {
            alert('No se pudieron obtener los detalles.');
            window.location.href = 'comunidad.html';
            return;
        }
        detalle = await res.json();
    } catch (e) {
        console.error(e);
        alert('Error al cargar la informacion.');
        window.location.href = 'comunidad.html';
        return;
    }

    const data = detalle.mascotaPerdida || {};
    const dueno = detalle.dueno || detalle.dueño;

    document.getElementById('perdidaNombre').textContent = data.nombre || 'Sin nombre';
    document.getElementById('perdidaDetalles').innerHTML = `
        <strong>Tipo:</strong> ${data.tipoAnimal || '--'}<br>
        <strong>Tamano:</strong> ${data.tamanio || '--'}<br>
        <strong>Color:</strong> ${data.color || '--'}<br>
        <strong>Detalles:</strong> ${data.detallesAdicionales || 'Sin detalles adicionales.'}
    `;
    document.getElementById('perdidaUbicacion').textContent = 'Ubicacion: ' + (data.direccion || '--');
    document.getElementById('perdidaRecompensa').textContent = `Recompensa: $${data.recompensa ?? '--'}`;
    document.getElementById('perdidaEdad').textContent = `Edad: ${data.edad ?? '--'} meses`;
    document.getElementById('perdidaExtra').textContent = `Condicion: ${data.discapacidad || 'Ninguna'}`;

    const track = document.getElementById('carouselTrack');
    const btnPrev = document.getElementById('btnPrevImg');
    const btnNext = document.getElementById('btnNextImg');

    try {
        const resImg = await window.apiFetch(`/animal/${idAnimal}/imagenes_info`);
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
            imgEl.src = `${window.API_BASE_URL}/animal/${idAnimal}/imagen_index/${i}`;
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

    const btnContactar = document.getElementById('btnContactar');
    const myId = localStorage.getItem('idAnimalLover');

    if (!dueno || !dueno.idAnimalLover) {
        btnContactar.textContent = 'Informacion de dueño no disponible';
        btnContactar.disabled = true;
        btnContactar.style.opacity = '0.6';
        btnContactar.style.cursor = 'not-allowed';
        return;
    }

    if (String(dueno.idAnimalLover) === String(myId)) {
        btnContactar.textContent = 'Esta es tu publicacion';
        btnContactar.disabled = true;
        btnContactar.style.opacity = '0.6';
        btnContactar.style.cursor = 'not-allowed';
        return;
    }

    btnContactar.addEventListener('click', () => {
        const idTrabajo = -(1000000 + idAnimal);
        window.location.href = `chat.html?idTrabajo=${idTrabajo}&receptor=${dueno.idAnimalLover}`;
    });
});
