document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fotos');
    const imagePreviewContainer = document.getElementById('imagePreview');
    const postForm = document.getElementById('postAdopcionForm');
    const pageTitle = document.querySelector('h2');
    const submitButton = postForm ? postForm.querySelector('button[type="submit"]') : null;

    const urlParams = new URLSearchParams(window.location.search);
    const editId = urlParams.get('edit');
    const isEditMode = Boolean(editId);
    let hasNewImages = false;
    let currentEstado = 'Activo';

    // Manejo de la vista previa de las imágenes
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);

            if (files.length > 0) {
                hasNewImages = true;
            }
            
            files.forEach(file => {
                if (!file.type.startsWith('image/')) return;

                const reader = new FileReader();
                
                reader.onload = function(event) {
                    const previewItem = document.createElement('div');
                    previewItem.className = 'preview-item';
                    
                    const img = document.createElement('img');
                    img.className = 'preview-img';
                    img.src = event.target.result;
                    
                    const closeBtn = document.createElement('div');
                    closeBtn.className = 'close-btn';
                    closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
                    
                    closeBtn.onclick = function() {
                        previewItem.remove();
                    };
                    
                    previewItem.appendChild(img);
                    previewItem.appendChild(closeBtn);
                    imagePreviewContainer.appendChild(previewItem);
                };
                
                reader.readAsDataURL(file);
            });
            
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
            if (!isEditMode && imagePreviewContainer.children.length === 0) {
                alert('Debes subir por lo menos una imagen de la mascota.');
                return;
            }

            // Recolectar imágenes en base64 desde el preview
            const imagenesBase64 = [];
            if (hasNewImages) {
                const previewImgs = imagePreviewContainer.querySelectorAll('.preview-img');
                previewImgs.forEach(img => {
                    imagenesBase64.push(img.src);
                });
            }

            const idAnimalLover = localStorage.getItem('idAnimalLover');
            if (!idAnimalLover) {
                alert('Debes iniciar sesión para publicar una adopción.');
                window.location.href = 'login.html';
                return;
            }

            const payload = {
                idAnimal: isEditMode ? parseInt(editId) : undefined,
                idAnimalLover: parseInt(idAnimalLover),
                nombre: document.getElementById('nombre').value.trim(),
                tipoAnimal: document.getElementById('tipo_animal').value,
                tamanio: document.getElementById('tamanio').value,
                color: document.getElementById('color').value.trim(),
                edad: parseInt(document.getElementById('edad').value) || 0,
                direccion: document.getElementById('direccion').value.trim(),
                discapacidad: document.getElementById('discapacidad').value.trim(),
                detallesAdicionales: document.getElementById('detalles_adicionales').value.trim(),
                vacunas: document.getElementById('vacunas').value.trim(),
                imagenesBase64: imagenesBase64,
                estado: currentEstado
            };

            try {
                const response = await window.apiFetch('/adopciones', {
                    method: isEditMode ? 'PUT' : 'POST',
                    body: JSON.stringify(payload)
                });

                if (response && response.ok) {
                    alert(isEditMode ? 'Adopción actualizada con éxito.' : '¡Adopción publicada con éxito!');
                    if (isEditMode) {
                        window.location.href = 'mis_adopciones.html';
                        return;
                    }
                    postForm.reset();
                    if (imagePreviewContainer) {
                        imagePreviewContainer.innerHTML = '';
                    }
                    window.location.href = 'comunidad.html';
                } else {
                    const errorData = await response.json();
                    alert('Error al publicar: ' + (errorData.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error al enviar adopción:', error);
                alert('Error de red al publicar la adopción. Inténtalo más tarde.');
            }
        });
    }

    async function cargarDatosEdicion() {
        if (!isEditMode) return;

        if (pageTitle) {
            pageTitle.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Editar Adopción';
        }
        if (submitButton) {
            submitButton.textContent = 'Actualizar Adopción';
        }

        try {
            const res = await window.apiFetch(`/adopciones/detalle?id_animal=${editId}`);
            if (!res || !res.ok) {
                alert('No se pudo cargar la informacion de la adopción.');
                return;
            }
            const detalle = await res.json();
            const data = detalle.adopcion || {};
            currentEstado = data.estado || 'Activo';

            document.getElementById('nombre').value = data.nombre || '';
            document.getElementById('tipo_animal').value = data.tipoAnimal || '';
            document.getElementById('tamanio').value = data.tamanio || '';
            document.getElementById('color').value = data.color || '';
            document.getElementById('edad').value = data.edad ?? '';
            document.getElementById('direccion').value = data.direccion || '';
            document.getElementById('discapacidad').value = data.discapacidad || '';
            document.getElementById('vacunas').value = data.vacunas || '';
            document.getElementById('detalles_adicionales').value = data.detallesAdicionales || '';
        } catch (e) {
            console.error('Error cargando datos de edicion:', e);
        }
    }

    cargarDatosEdicion();
});
