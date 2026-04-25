let currentImageIndex = 0;
let totalImages = 0;

document.addEventListener('DOMContentLoaded', async () => {
    const idTrabajo = localStorage.getItem('idTrabajoSeleccionado');
    if (!idTrabajo) {
        alert('No se ha seleccionado ningún trabajo.');
        window.location.href = 'trabajos_aceptados.html';
        return;
    }

    try {
        const res = await window.apiFetch(`/trabajo?id=${idTrabajo}`);
        if (!res || !res.ok) {
            alert('No se pudieron obtener los detalles del trabajo.');
            window.location.href = 'trabajos_aceptados.html';
            return;
        }

        const job = await res.json();
        
        // Asignar los datos a los elementos del DOM
        document.getElementById('jobTitle').textContent = job.nombre;
        document.getElementById('jobDesc').textContent = job.descripcion;
        document.getElementById('jobLocation').textContent = 'Ubicación: ' + job.ubicacion;
        document.getElementById('jobPrice').textContent = 'Pago: $' + job.monto;
        document.getElementById('jobDate').textContent = job.fechaPublicacion; // Ya viene con el formato correcto

        // Intentar cargar las imágenes
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
            // Fallback si no hay imágenes
            const imgEl = document.createElement('img');
            imgEl.src = "https://via.placeholder.com/300x180?text=Sin+Imagen";
            track.appendChild(imgEl);
        }

    } catch (e) {
        console.error("Error cargando el trabajo:", e);
        alert('Ocurrió un error al cargar la información.');
        window.location.href = 'trabajos_aceptados.html';
    }
});
