// Lógica del Temporizador
    document.querySelectorAll('.card').forEach(card => {
        let seconds = parseInt(card.getAttribute('data-seconds'));
        const display = card.querySelector('.timer-display');
        const statusSpan = card.querySelector('.status');
        const btnExtend = card.querySelector('.btn-extend');
        const timerBox = card.querySelector('.timer-box');

        const countdown = setInterval(() => {
            if (!statusSpan.classList.contains('active')) {
                clearInterval(countdown);
                return;
            }

            seconds--;
            
            let h = Math.floor(seconds / 3600).toString().padStart(2, '0');
            let m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
            let s = (seconds % 60).toString().padStart(2, '0');
            display.textContent = `${h}:${m}:${s}`;

            // Alerta visual si falta menos de 1 hora
            if (seconds < 3600 && seconds > 0) {
                timerBox.classList.add('timer-urgent');
                btnExtend.style.display = 'flex'; 
            }

            if (seconds <= 0) {
                clearInterval(countdown);
                autoExpire(card);
            }
        }, 1000);
    });

    function autoExpire(card) {
        const statusSpan = card.querySelector('.status');
        statusSpan.textContent = '○ Expirado';
        statusSpan.className = 'status inactive';
        card.querySelector('.timer-display').textContent = "00:00:00";
        disableButtons(card);
        
        if(confirm("El tiempo de una publicación ha terminado. ¿Deseas extenderlo?")) {
            location.reload();
        }
    }

    function disableButtons(card) {
        card.querySelectorAll('.btn:not(.btn-details, .btn-extend)').forEach(b => b.disabled = true);
    }

    // Acciones de botones
    document.querySelectorAll('.btn-complete').forEach(btn => {
        btn.addEventListener('click', () => {
            const card = btn.closest('.card');
            const st = card.querySelector('.status');
            st.textContent = '✓ Completado';
            st.className = 'status completed';
            disableButtons(card);
            alert("¡Felicidades por completar el trabajo!");
        });
    });

    document.querySelectorAll('.btn-deactivate').forEach(btn => {
        btn.addEventListener('click', () => {
            if(confirm("¿Estás seguro de que quieres eliminar esta publicación?")) {
                const card = btn.closest('.card');
                const st = card.querySelector('.status');
                st.textContent = '○ Eliminado';
                st.className = 'status inactive';
                disableButtons(card);
            }
        });
    });

    document.querySelectorAll('.btn-extend').forEach(btn => {
        btn.addEventListener('click', () => {
            alert("Solicitud enviada. El plazo se ha extendido 24 horas.");
            location.reload();
        });
    });