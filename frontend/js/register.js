document.addEventListener('DOMContentLoaded', () => {
    const registroForm = document.getElementById('registroForm');

    if (registroForm) {
        registroForm.addEventListener('submit', (e) => {
            // BLOQUEAMOS el envío por defecto para que no recargue la página
            e.preventDefault(); 
            
            // Aquí puedes agregar un mensaje opcional
            console.log("Validación exitosa, redirigiendo...");

            // REDIRECCIÓN: 
            // Si tu login.html está en la misma carpeta que register.html, usa "login.html"
            // Si está en una carpeta distinta, asegúrate de poner la ruta correcta.
            window.location.href = "login.html";
        });
    }
});