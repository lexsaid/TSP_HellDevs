document.addEventListener('DOMContentLoaded', async () => {
    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }

    const emptyState = document.getElementById('emptyState');
    const albergueList = document.getElementById('albergueList');

    try {
        const response = await window.apiFetch('/albergues');
        let albergues = [];
        if (response && response.ok) {
            albergues = await response.json();
        } else if (response && response.status === 404) {
            albergues = [];
        }

        const misAlbergues = albergues.filter(item => {
            const alb = item.albergue;
            return String(alb.idAnimalLover) === String(myIdStr);
        });

        if (misAlbergues.length === 0) {
            if (emptyState) emptyState.style.display = 'block';
            if (albergueList) albergueList.style.display = 'none';
            return;
        }

        if (emptyState) emptyState.style.display = 'none';
        if (albergueList) {
            albergueList.style.display = 'block';
            albergueList.innerHTML = '';

            for (const item of misAlbergues) {
                const alb = item.albergue;

                const article = document.createElement('article');
                article.className = 'job-card';

                const img = document.createElement('img');
                img.src = `${window.API_BASE_URL}/albergue/${alb.idAlbergue}/imagen`;
                img.className = 'job-image';
                img.style.width = '100%';
                img.style.height = '180px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = '12px 12px 0 0';
                img.onerror = () => { img.src = 'https://via.placeholder.com/300x180?text=Albergue'; };

                const details = document.createElement('div');
                details.className = 'card-details';
                details.style.padding = '15px';

                const mainInfo = document.createElement('div');
                mainInfo.className = 'main-info';
                mainInfo.innerHTML = `
                    <p style="font-size:1.1rem; margin-bottom:8px;"><strong>${alb.nombre}</strong></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Ubicacion: <span>${alb.ubicacion}</span></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Capacidad: <span>${alb.capacidad}</span></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Preferencia: <span>${alb.preferencia}</span></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Costo diario: <span>$${alb.costoDiario}</span></p>
                `;

                const actions = document.createElement('div');
                actions.className = 'actions';
                actions.style.display = 'flex';
                actions.style.gap = '10px';
                actions.style.marginTop = '15px';

                const btnEdit = document.createElement('button');
                btnEdit.className = 'btn btn-outline';
                btnEdit.innerHTML = '<i class="fas fa-edit"></i> Editar';
                btnEdit.style.flex = '1';
                btnEdit.onclick = () => {
                    window.location.href = `pubAlbergue.html?edit=${alb.idAlbergue}`;
                };

                const btnDelete = document.createElement('button');
                btnDelete.className = 'btn btn-deactivate';
                btnDelete.innerHTML = '<i class="fas fa-trash"></i> Borrar';
                btnDelete.style.cssText = 'flex:1; background-color:#e74c3c; color:#fff; border:none; border-radius:12px; padding:10px; font-weight:600; cursor:pointer;';
                btnDelete.onclick = async () => {
                    if (!confirm('¿Eliminar este albergue? Esto tambien borrara los chats asociados.')) {
                        return;
                    }

                    try {
                        const resDel = await window.apiFetch(`/albergues?id_albergue=${alb.idAlbergue}`, {
                            method: 'DELETE'
                        });
                        if (resDel && resDel.ok) {
                            article.remove();
                            if (albergueList.children.length === 0 && emptyState) {
                                emptyState.style.display = 'block';
                                albergueList.style.display = 'none';
                            }
                        } else if (resDel) {
                            const error = await resDel.json();
                            alert('No se pudo eliminar: ' + error.detail);
                        }
                    } catch (e) {
                        console.error(e);
                        alert('Error de red.');
                    }
                };

                actions.appendChild(btnEdit);
                actions.appendChild(btnDelete);

                details.appendChild(mainInfo);
                details.appendChild(actions);

                article.style.backgroundColor = '#fff';
                article.style.borderRadius = '12px';
                article.style.boxShadow = '0 4px 10px rgba(0,0,0,0.05)';
                article.style.marginBottom = '20px';
                article.appendChild(img);
                article.appendChild(details);

                albergueList.appendChild(article);
            }
        }
    } catch (e) {
        console.error('Error obteniendo albergues:', e);
        if (emptyState) {
            emptyState.style.display = 'block';
            emptyState.querySelector('h2').textContent = 'Error al cargar albergues.';
            emptyState.querySelector('p').textContent = 'Intentalo mas tarde.';
        }
        if (albergueList) albergueList.style.display = 'none';
    }
});
