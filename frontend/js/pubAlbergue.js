document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fotos');
    const imagePreviewContainer = document.getElementById('imagePreview');
    const postForm = document.getElementById('postAlbergueForm');

    // Manejo de la vista previa de las imágenes
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);
            
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
            if (imagePreviewContainer.children.length === 0) {
                alert('Debes subir por lo menos una imagen de las instalaciones.');
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
                alert('Debes iniciar sesión para dar de alta un albergue.');
                window.location.href = 'login.html';
                return;
            }

            const payload = {
                idAnimalLover: parseInt(idAnimalLover),
                nombre: document.getElementById('nombre').value.trim(),
                ubicacion: document.getElementById('ubicacion').value.trim(),
                capacidad: parseInt(document.getElementById('capacidad').value),
                preferencia: document.getElementById('preferencia').value,
                costoDiario: parseInt(document.getElementById('costo_diario').value),
                preRequisitos: document.getElementById('pre_requisitos').value.trim(),
                imagenesBase64: imagenesBase64
            };

            try {
                const response = await window.apiFetch('/albergues', {
                    method: 'POST',
                    body: JSON.stringify(payload)
                });

                if (response && response.ok) {
                    alert('¡Albergue dado de alta con éxito!');
                    postForm.reset();
                    if (imagePreviewContainer) {
                        imagePreviewContainer.innerHTML = '';
                    }
                    window.location.href = 'servicios.html';
                } else {
                    const errorData = await response.json();
                    alert('Error al registrar: ' + (errorData.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error al enviar albergue:', error);
                alert('Error de red al registrar el albergue. Inténtalo más tarde.');
            }
        });
    }
});
