document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            // Evitamos que la página se recargue automáticamente
            e.preventDefault();

            const email = loginForm.querySelector('input[type="email"]').value;
            const password = loginForm.querySelector('input[type="password"]').value;

            try {
                // Hacemos el llamado a la API real
                const response = await fetch(`${window.API_BASE_URL}/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email: email, contraseña: password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Guardar los datos en el localStorage
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('idAnimalLover', data.idAnimalLover);
                    localStorage.setItem('nombre', data.nombre);
                    
                    // Redireccionamos al index.html
                    window.location.href = "index.html";
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Error al iniciar sesión. Verifica tus credenciales.');
                }
            } catch (error) {
                console.error("Error:", error);
                alert('Error de red al intentar iniciar sesión.');
            }
        });
    }
});