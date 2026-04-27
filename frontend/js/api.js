const API_BASE_URL = 'https://api.mizcuin.online';

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // Agregar el token si existe
    if (token) {
        headers['Authorization'] = token;
    }

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        if (response.status === 401) {
            console.warn('Sesión inválida o expirada. Redirigiendo a login...');
            // Limpiar caché
            localStorage.removeItem('token');
            localStorage.removeItem('idAnimalLover');
            localStorage.removeItem('nombre');
            
            // Redirigir al login
            // Determinamos la ruta de login.html basándonos en si estamos en html/ o en la raíz
            if (window.location.pathname.includes('/html/')) {
                window.location.href = 'login.html';
            } else {
                window.location.href = 'html/login.html';
            }
            return null;
        }

        return response;
    } catch (error) {
        console.error('Error en la petición API:', error);
        throw error;
    }
}

// Exponer de manera global
window.apiFetch = apiFetch;
window.API_BASE_URL = API_BASE_URL;

window.getFormattedDateMX = function() {
    const formatter = new Intl.DateTimeFormat('es-MX', {
        timeZone: 'America/Mexico_City',
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour12: false
    });
    
    // Formato devuelto por es-MX suele ser DD/MM/AAAA, HH:MM
    // Lo parsearemos manualmente para asegurar "HH:MM - DD/MM/AAAA"
    const parts = formatter.formatToParts(new Date());
    const map = {};
    parts.forEach(p => map[p.type] = p.value);
    
    return `${map.hour}:${map.minute} - ${map.day}/${map.month}/${map.year}`;
};