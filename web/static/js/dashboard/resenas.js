import { createModal } from "./core.js";

const viewReviewModal = createModal("modal-view-review");
const deleteReviewModal = createModal("modal-delete-review");

let currentReviewId = null;

document.querySelectorAll(".btn-open-view-review").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const data = row.dataset;

        currentReviewId = data.resenaId;

        const inputHidden = document.querySelector("#input-delete-id-resena");
        if (inputHidden) {
            inputHidden.value = currentReviewId;
        }

        document.querySelector("#modal-resena-id").textContent = data.resenaId;
        document.querySelector("#modal-resena-nombre-apellido").textContent = data.nombreApellido;
        document.querySelector("#modal-resena-reserva-id").textContent = data.reservaId;
        document.querySelector("#modal-resena-fecha").textContent = data.fecha;
        document.querySelector("#modal-resena-ambiente").textContent = data.ambiente;
        document.querySelector("#modal-resena-servicio").textContent = data.servicio;
        document.querySelector("#modal-resena-comida").textContent = data.comida;
        document.querySelector("#modal-resena-comentario").textContent = data.comentario;

        viewReviewModal.open();
    });
});

document
    .getElementById("btn-open-delete-review")
    .addEventListener("click", () => {
        deleteReviewModal.open();
    });

document
    .getElementById("btn-cancel-delete-review")
    .addEventListener("click", () => {
        deleteReviewModal.close();
    });
