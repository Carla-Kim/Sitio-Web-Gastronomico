document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('reseña-modal'); 
    const confirmModal = document.getElementById('confirm-modal');
    const deleteForm = document.getElementById('delete-form');
    const confirmDeleteBox = document.getElementById('confirm-delete-box');
    
    let currentId = null; 

    document.querySelectorAll('.view-button').forEach(button => {
        button.addEventListener('click', () => {
            currentId = button.dataset.id;
            
            document.getElementById('modal-comentario').textContent = button.dataset.comentario;
            document.getElementById('modal-id').textContent = currentId;
            document.getElementById('modal-id-reserva').textContent = button.dataset.reserva;
            document.getElementById('modal-nombre').textContent = button.dataset.nombre;
            document.getElementById('modal-ambiente').textContent = button.dataset.ambiente;
            document.getElementById('modal-servicio').textContent = button.dataset.servicio;
            document.getElementById('modal-comida').textContent = button.dataset.comida;
            document.getElementById('modal-fecha').textContent = button.dataset.fecha;
            
            modal.classList.remove('hidden');
        });
    });

    document.getElementById('abrir-confirm-delete').addEventListener('click', () => {
        confirmModal.classList.remove('hidden');
        confirmDeleteBox.classList.remove('hidden');
    });

    document.getElementById('btn-confirm-delete').addEventListener('click', () => {
        if (currentId) {
            deleteForm.action = `/dashboard/reseñas?id_reseña=${currentId}`;
            
            if(!deleteForm.querySelector('input[name="id_reseña"]')){
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'id_reseña';
                input.value = currentId;
                deleteForm.appendChild(input);
            }
            deleteForm.submit(); 
        }
    });

    document.getElementById('close-modal-button').addEventListener('click', () => modal.classList.add('hidden'));
    document.getElementById('btn-cancel-delete').addEventListener('click', () => confirmModal.classList.add('hidden'));

    const filtros = {
        id: document.getElementById('input_id'),
        reserva: document.getElementById('input_id_reserva'),
        inicio: document.getElementById('fecha-inicio'),
        fin: document.getElementById('fecha-fin'),
        puntaje: document.getElementById('puntaje-filter')
    };

    const filas = document.querySelectorAll('.reseña-fila');

    function aplicarFiltros() {
        filas.forEach(fila => {
            const id = fila.querySelector('.reseña-id').textContent;
            const idReserva = fila.children[1].textContent; 
            const puntaje = fila.querySelector('.reseña-comida').textContent; 
            const fechaStr = fila.querySelector('.reseña-fecha').textContent;
            
            const [d, m, y] = fechaStr.split('/');
            const fechaFila = new Date(`${y}-${m}-${d}`);

            const coincideId = filtros.id.value === "" || id.includes(filtros.id.value);
            const coincideReserva = filtros.reserva.value === "" || idReserva.includes(filtros.reserva.value);
            const coincidePuntaje = filtros.puntaje.value === "all" || puntaje === filtros.puntaje.value;
            
            let coincideFecha = true;
            if (filtros.inicio.value && fechaFila < new Date(filtros.inicio.value)) coincideFecha = false;
            if (filtros.fin.value && fechaFila > new Date(filtros.fin.value)) coincideFecha = false;

            fila.style.display = (coincideId && coincideReserva && coincidePuntaje && coincideFecha) ? '' : 'none';
        });
    }

    Object.values(filtros).forEach(input => {
        input.addEventListener('input', aplicarFiltros);
    });
});