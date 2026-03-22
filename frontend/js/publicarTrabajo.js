const imageInput = document.getElementById('imageUpload');
const previewContainer = document.getElementById('previewContainer');
let allFiles = []; // Arreglo para acumular todos los archivos

imageInput.addEventListener('change', function() {
    // Convertimos la lista de archivos actual en un arreglo y la sumamos a la anterior
    const newFiles = Array.from(this.files);
    allFiles = [...allFiles, ...newFiles]; 

    // Limpiamos la vista previa para redibujarla con TODAS las imágenes acumuladas
    previewContainer.innerHTML = '';

    allFiles.forEach((file, index) => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Creamos un contenedor (preview-item) para la imagen y el botón de "eliminar"
                const itemDiv = document.createElement('div');
                itemDiv.className = 'preview-item';

                // Imagen de vista previa
                const img = document.createElement('img');
                img.src = e.target.result;
                img.className = 'preview-img'; 
                
                // Botón de eliminar (X)
                const closeBtn = document.createElement('div');
                closeBtn.className = 'close-btn';
                closeBtn.innerHTML = '×'; // Símbolo de multiplicación (se ve más claro que una x)
                
                // Evento para eliminar esta imagen específica al hacer click
                closeBtn.addEventListener('click', () => {
                    eliminarImagen(index);
                });

                // Armamos la estructura
                itemDiv.appendChild(img);
                itemDiv.appendChild(closeBtn);
                previewContainer.appendChild(itemDiv);
            };
            reader.readAsDataURL(file);
        }
    });
});

// Función para eliminar la imagen del arreglo y redibujar la vista previa
function eliminarImagen(indexToDelete) {
    // Borramos el elemento del arreglo 'allFiles' usando 'splice'
    allFiles.splice(indexToDelete, 1);
    
    // Forzamos un evento 'change' en el input para que se vuelva a ejecutar la lógica y redibuje
    // Pero como 'allFiles' ya está actualizado, el redibujado será correcto.
    // Una forma más directa es llamar a una función que solo redibuje:
    redibujarVistaPrevia();
}

// Función auxiliar para redibujar la vista previa después de una eliminación
function redibujarVistaPrevia() {
    previewContainer.innerHTML = ''; // Limpiar el contenedor

    allFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
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

// Evento de envío del formulario
document.getElementById('postForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    console.log("Archivos finales a enviar:", allFiles);
    
    // Aquí validas si necesitas imágenes obligatorias
    if (allFiles.length === 0) {
        if(!confirm("Aún no has agregado ninguna imagen. ¿Deseas publicar el trabajo de todas formas?")) {
            return; // Cancela el envío si el usuario dice "No"
        }
    }
    
    window.location.href = "index.html";
});