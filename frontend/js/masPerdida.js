document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fotos');
    const imagePreviewContainer = document.getElementById('imagePreview');
    const postForm = document.getElementById('postForm');

    // Manejo de la vista previa de las imágenes
    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const files = Array.from(e.target.files);

            files.forEach(file => {
                if (!file.type.startsWith('image/')) return;

                const reader = new FileReader();

                reader.onload = function (event) {
                    const previewItem = document.createElement('div');
                    previewItem.className = 'preview-item';

                    const img = document.createElement('img');
                    img.className = 'preview-img';
                    img.src = event.target.result;

                    const closeBtn = document.createElement('div');
                    closeBtn.className = 'close-btn';
                    closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';

                    closeBtn.onclick = function () {
                        previewItem.remove();
                    };

                    previewItem.appendChild(img);
                    previewItem.appendChild(closeBtn);
                    imagePreviewContainer.appendChild(previewItem);
                };

                reader.readAsDataURL(file);
            });

            // Limpiar input para permitir seleccionar la misma imagen si fue borrada del preview
            fileInput.value = '';
        });
    }

    // Manejo del envío del formulario
    if (postForm) {
        postForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Validar campos requeridos para evitar puros espacios en blanco
            const requiredInputs = postForm.querySelectorAll('[required]');
            for (let input of requiredInputs) {
                if (input.value.trim() === '') {
                    alert('Por favor, completa todos los campos requeridos con información válida (no solo espacios).');
                    input.focus();
                    return;
                }
            }

            // Validar que se haya subido al menos una imagen
            if (imagePreviewContainer.children.length === 0) {
                alert('Debes subir por lo menos una imagen de la mascota.');
                return;
            }

            // Recolectar imágenes en base64 desde el preview
            const imagenesBase64 = [];
            const previewImgs = imagePreviewContainer.querySelectorAll('.preview-img');
            previewImgs.forEach(img => {
                imagenesBase64.push(img.src);
            });

            const idAnimalLover = localStorage.getItem('idAnimalLover');
            if (!idAnimalLover) {
                alert('Debes iniciar sesión para reportar una mascota perdida.');
                window.location.href = 'login.html';
                return;
            }

            const payload = {
                idAnimalLover: parseInt(idAnimalLover),
                nombre: document.getElementById('nombre').value.trim(),
                tipoAnimal: document.getElementById('tipo_animal').value,
                tamanio: document.getElementById('tamanio').value,
                color: document.getElementById('color').value.trim(),
                edad: parseInt(document.getElementById('edad').value),
                direccion: document.getElementById('direccion').value.trim(),
                discapacidad: document.getElementById('discapacidad').value.trim(),
                detallesAdicionales: document.getElementById('detalles_adicionales').value.trim(),
                recompensa: document.getElementById('recompensa').value.trim() || '0',
                imagenesBase64: imagenesBase64
            };

            try {
                const response = await window.apiFetch('/mascotas_perdidas', {
                    method: 'POST',
                    body: JSON.stringify(payload)
                });

                if (response && response.ok) {
                    alert('¡Reporte de mascota perdida publicado con éxito!');
                    postForm.reset();
                    if (imagePreviewContainer) {
                        imagePreviewContainer.innerHTML = '';
                    }
                    window.location.href = 'comunidad.html';
                } else {
                    const errorData = await response.json();
                    alert('Error al reportar: ' + (errorData.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error al enviar reporte:', error);
                alert('Error de red al enviar el reporte. Inténtalo más tarde.');
            }
        });
    }
});
