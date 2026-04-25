document.addEventListener('DOMContentLoaded', () => {
    const registroForm = document.getElementById('registroForm');

    if (registroForm) {
        registroForm.addEventListener('submit', async (e) => {
            e.preventDefault(); 
            
            const formData = new FormData(registroForm);
            const data = Object.fromEntries(formData.entries());

            const animalLover = {
                nombre: data.nombre,
                apellido: data.apellido,
                email: data.email,
                telefono: data.telefono,
                contraseña: data.password
            };

            try {
                const res = await window.apiFetch('/animalLover', {
                    method: 'POST',
                    body: JSON.stringify(animalLover)
                });

                if (res && res.ok) {
                    alert("Usuario registrado correctamente");
                    window.location.href = "login.html";
                } else if (res) {
                    const error = await res.json();
                    alert(error.detail || "Error al registrar el usuario");
                }
            } catch (error) {
                console.error("Error al registrar:", error);
                alert("Error de red al intentar registrar.");
            }
        });
    }
});