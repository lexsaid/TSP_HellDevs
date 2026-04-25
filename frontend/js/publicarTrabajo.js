const imageInput = document.getElementById('imageUpload');
const previewContainer = document.getElementById('previewContainer');
const pageTitle = document.getElementById('pageTitle');
const submitBtn = document.getElementById('submitBtn');
let allFiles = []; // Arreglo para acumular todos los archivos

// Params para Edit mode
const urlParams = new URLSearchParams(window.location.search);
const editId = urlParams.get('edit');
let isEditMode = !!editId;

document.addEventListener('DOMContentLoaded', async () => {
    if (isEditMode) {
        pageTitle.textContent = "🐾 Editar trabajo";
        submitBtn.textContent = "Actualizar trabajo";
        imageInput.required = false; // No obligar a subir imagen si está editando

        try {
            const res = await window.apiFetch(`/trabajo?id=${editId}`);
            if (res && res.ok) {
                const job = await res.json();
                document.getElementById('tituloTrabajo').value = job.nombre;
                document.getElementById('tipoTrabajo').value = job.tipoTrabajo;
                document.getElementById('descTrabajo').value = job.descripcion;
                document.getElementById('montoTrabajo').value = job.monto;
                document.getElementById('ubicacionTrabajo').value = job.ubicacion;
                // Informar que las imágenes anteriores se conservan
                previewContainer.innerHTML = '<p style="color:#666; font-size:0.9rem;">Dejar vacío para conservar imágenes originales, o subir nuevas para reemplazarlas (Opcional).</p>';
            } else {
                alert("No se pudo cargar la información del trabajo a editar.");
            }
        } catch (e) {
            console.error("Error cargando trabajo:", e);
        }
    }
});

imageInput.addEventListener('change', function () {
    const newFiles = Array.from(this.files);
    allFiles = [...allFiles, ...newFiles];
    redibujarVistaPrevia();
});

function eliminarImagen(indexToDelete) {
    allFiles.splice(indexToDelete, 1);
    redibujarVistaPrevia();
}

function redibujarVistaPrevia() {
    previewContainer.innerHTML = '';

    if (allFiles.length === 0 && isEditMode) {
        previewContainer.innerHTML = '<p style="color:#666; font-size:0.9rem;">Dejar vacío para conservar imágenes originales, o subir nuevas para reemplazarlas (Opcional).</p>';
        return;
    }

    allFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'preview-item';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'preview-img';

            const closeBtn = document.createElement('div');
            closeBtn.className = 'close-btn';
            closeBtn.innerHTML = '×';

            closeBtn.addEventListener('click', () => {
                eliminarImagen(index);
            });

            itemDiv.appendChild(img);
            itemDiv.appendChild(closeBtn);
            previewContainer.appendChild(itemDiv);
        };
        reader.readAsDataURL(file);
    });
}

document.getElementById('postForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (allFiles.length === 0 && !isEditMode) {
        if (!confirm("Aún no has agregado ninguna imagen. ¿Deseas publicar el trabajo de todas formas?")) {
            return;
        }
    }

    if (isEditMode) {
        if (!confirm("¿Deseas actualizar el trabajo con estos datos?")) {
            return;
        }
    }

    const titulo = document.getElementById('tituloTrabajo').value;
    const tipo = document.getElementById('tipoTrabajo').value;
    const desc = document.getElementById('descTrabajo').value;
    const montoStr = document.getElementById('montoTrabajo').value;
    const ubicacion = document.getElementById('ubicacionTrabajo').value;

    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        alert("Debes iniciar sesión primero");
        window.location.href = "login.html";
        return;
    }

    const trabajo = {
        nombre: titulo,
        ubicacion: ubicacion || 'Sin ubicación',
        fechaPublicacion: window.getFormattedDateMX(),
        monto: parseFloat(montoStr) || 0,
        descripcion: desc,
        idAnimalLoverPublicador: parseInt(myIdStr),
        tipoTrabajo: tipo,
        imagenesBase64: []
    };

    if (isEditMode) {
        trabajo.idTrabajo = parseInt(editId);
    }

    // Extraer base64 de las imágenes solo si subieron nuevas
    if (allFiles.length > 0) {
        const imgElements = previewContainer.querySelectorAll('.preview-img');
        imgElements.forEach(img => {
            trabajo.imagenesBase64.push(img.src);
        });
    }

    try {
        const url = '/trabajo';
        const method = isEditMode ? 'PUT' : 'POST';

        const res = await window.apiFetch(url, {
            method: method,
            body: JSON.stringify(trabajo)
        });

        if (res && res.ok) {
            alert(isEditMode ? "¡Trabajo actualizado con éxito!" : "¡Trabajo publicado con éxito!");
            window.location.href = isEditMode ? "mis_publicaciones.html" : "index.html";
        } else if (res) {
            const errorData = await res.json();
            alert("Error al guardar: " + errorData.detail);
        }
    } catch (error) {
        console.error("Error de red:", error);
        alert("Hubo un error al intentar guardar.");
    }
});