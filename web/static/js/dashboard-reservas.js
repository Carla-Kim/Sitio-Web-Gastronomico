const modal = document.getElementById('reserva-modal');
const openButton = document.getElementById('open-modal-button');
const closeButton = document.getElementById('close-modal-button');

openButton.addEventListener('click', () => {
    modal.classList.remove('hidden');
});

closeButton.addEventListener('click', () => {
    modal.classList.add('hidden');
});
