document.addEventListener('DOMContentLoaded', async () => {
    const myIdStr = localStorage.getItem('idAnimalLover');
    if (!myIdStr) {
        window.location.href = 'login.html';
        return;
    }

    const emptyState = document.getElementById('emptyState');
    const perdidasList = document.getElementById('perdidasList');

    try {
        const res = await window.apiFetch(`/mascotas_perdidas/mis?idAnimalLover=${myIdStr}`);
        let publicaciones = [];
        if (res && res.ok) {
            publicaciones = await res.json();
        } else if (res && res.status === 404) {
            publicaciones = [];
        }

        if (!publicaciones || publicaciones.length === 0) {
            if (emptyState) emptyState.style.display = 'block';
            if (perdidasList) perdidasList.style.display = 'none';
            return;
        }

        if (emptyState) emptyState.style.display = 'none';
        if (perdidasList) {
            perdidasList.style.display = 'block';
            perdidasList.innerHTML = '';

            for (const item of publicaciones) {
                const data = item.mascotaPerdida;

                const article = document.createElement('article');
                article.className = 'job-card';

                const img = document.createElement('img');
                img.src = `${window.API_BASE_URL}/animal/${data.idAnimal}/imagen`;
                img.className = 'job-image';
                img.style.width = '100%';
                img.style.height = '180px';
                img.style.objectFit = 'cover';
                img.style.borderRadius = '12px 12px 0 0';
                img.onerror = () => { img.src = `https://via.placeholder.com/300x180?text=${data.nombre}`; };

                const details = document.createElement('div');
                details.className = 'card-details';
                details.style.padding = '15px';

                const mainInfo = document.createElement('div');
                mainInfo.className = 'main-info';

                const estado = data.estado || 'Activo';
                const badgeColor = estado === 'Localizado' ? '#22c55e' : '#f59e0b';
                const badgeLabel = estado === 'Localizado' ? '✓ Localizado' : '● Activo';

                mainInfo.innerHTML = `
                    <span style="display:inline-block; background:${badgeColor}; color:#fff; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; margin-bottom:8px;">${badgeLabel}</span>
                    <p style="font-size:1.1rem; margin-bottom:8px;"><strong>${data.nombre}</strong></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Tipo: <span>${data.tipoAnimal}</span></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Direccion: <span>${data.direccion}</span></p>
                    <p style="margin:4px 0; color:#555; font-size:0.9rem;">Recompensa: <span>$${data.recompensa}</span></p>
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
                    window.location.href = `pubMascotaPerdida.html?edit=${data.idAnimal}`;
                };

                const btnLocalizado = document.createElement('button');
                btnLocalizado.className = 'btn';
                btnLocalizado.innerHTML = '<i class="fas fa-check"></i> Localizado';
                btnLocalizado.style.cssText = 'flex:1; background-color:#22c55e; color:#fff; border:none; border-radius:12px; padding:10px; font-weight:600; cursor:pointer;';

                if (estado === 'Localizado') {
                    btnLocalizado.disabled = true;
                    btnLocalizado.style.opacity = '0.6';
                    btnLocalizado.style.cursor = 'not-allowed';
                }

                btnLocalizado.onclick = async () => {
                    if (!confirm('¿Marcar esta mascota como localizada?')) {
                        return;
                    }
                    try {
                        const resLocal = await window.apiFetch(`/mascotas_perdidas/localizado?id_animal=${data.idAnimal}`, {
                            method: 'POST'
                        });
                        if (resLocal && resLocal.ok) {
                            btnLocalizado.disabled = true;
                            btnLocalizado.style.opacity = '0.6';
                            btnLocalizado.style.cursor = 'not-allowed';
                            mainInfo.querySelector('span').style.background = '#22c55e';
                            mainInfo.querySelector('span').textContent = '✓ Localizado';
                        } else if (resLocal) {
                            const error = await resLocal.json();
                            alert('No se pudo marcar: ' + error.detail);
                        }
                    } catch (e) {
                        console.error(e);
                        alert('Error de red.');
                    }
                };

                const btnDelete = document.createElement('button');
                btnDelete.className = 'btn btn-deactivate';
                btnDelete.innerHTML = '<i class="fas fa-trash"></i> Eliminar';
                btnDelete.style.cssText = 'flex:1; background-color:#e74c3c; color:#fff; border:none; border-radius:12px; padding:10px; font-weight:600; cursor:pointer;';
                btnDelete.onclick = async () => {
                    if (!confirm('¿Eliminar esta publicacion? Esto borrara chats e imagenes asociadas.')) {
                        return;
                    }
                    try {
                        const resDel = await window.apiFetch(`/mascotas_perdidas?id_animal=${data.idAnimal}`, {
                            method: 'DELETE'
                        });
                        if (resDel && resDel.ok) {
                            article.remove();
                            if (perdidasList.children.length === 0 && emptyState) {
                                emptyState.style.display = 'block';
                                perdidasList.style.display = 'none';
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
                actions.appendChild(btnLocalizado);
                actions.appendChild(btnDelete);

                details.appendChild(mainInfo);
                details.appendChild(actions);

                article.style.backgroundColor = '#fff';
                article.style.borderRadius = '12px';
                article.style.boxShadow = '0 4px 10px rgba(0,0,0,0.05)';
                article.style.marginBottom = '20px';
                article.appendChild(img);
                article.appendChild(details);

                perdidasList.appendChild(article);
            }
        }
    } catch (e) {
        console.error('Error obteniendo mascotas perdidas:', e);
        if (emptyState) {
            emptyState.style.display = 'block';
            emptyState.querySelector('h2').textContent = 'Error al cargar publicaciones.';
            emptyState.querySelector('p').textContent = 'Intentalo mas tarde.';
        }
        if (perdidasList) perdidasList.style.display = 'none';
    }
});
