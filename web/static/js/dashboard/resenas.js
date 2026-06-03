function parseDate(str) {
    const [day, month, year] = str.split("-").map(Number);
    return new Date(year, month - 1, day);
}


import { createTableFilter } from "./core.js";

const rows = document.querySelectorAll(".reseña-fila");
const form = document.querySelector(".form-filter");

const inputs = {
    reseña_id: form.querySelector("#filter-reseña-id"),
    reserva_id: form.querySelector("#filter-reseña-reserva-id"),
    fecha_desde: form.querySelector("#filter-fecha-desde"),
    fecha_hasta: form.querySelector("#filter-fecha-hasta"),
    ambiente: form.querySelector("#filter-reseña-ambiente"),
    servicio: form.querySelector("#filter-reseña-servicio"),
    comida: form.querySelector("#filter-reseña-comida")
};

createTableFilter({
    inputs,
    rows,

    getRowData: (row) => {
        const raw = row.querySelector(".reseña-fecha").textContent;

        return {
            reseña_id: row.querySelector(".reseña-id").textContent,
            reserva_id: row.querySelector(".reseña-reserva-id").textContent,
            fecha: parseDate(raw),
            ambiente: row.querySelector(".reseña-ambiente").textContent,
            servicio: row.querySelector(".reseña-servicio").textContent,
            comida: row.querySelector(".reseña-comida").textContent
        };
    },

    matchRow: (data) => {
        const reseña_id = inputs.reseña_id.value.trim();
        const reserva_id = inputs.reserva_id.value.trim();
        const fecha_desde = inputs.fecha_desde.value ? new Date(inputs.fecha_desde.value).getTime() : null;
        const fecha_hasta = inputs.fecha_hasta.value ? new Date(inputs.fecha_hasta.value).getTime() : null;
        const ambiente = inputs.ambiente.value;
        const servicio = inputs.servicio.value;
        const comida = inputs.comida.value;
        const rowDate = data.fecha.getTime();

        return (
            (!reseña_id || data.reseña_id.includes(reseña_id)) &&
            (!reserva_id || data.reserva_id.includes(reserva_id)) &&
            (!fecha_desde || rowDate >= fecha_desde) &&
            (!fecha_hasta || rowDate <= fecha_hasta) &&
            (!ambiente || data.ambiente.includes(ambiente)) &&
            (!servicio || data.servicio.includes(servicio)) &&
            (!comida || data.comida.includes(comida))
        );
    }
});


import { createModal } from "./core.js";

const viewReviewModal = createModal("modal-view-review");
const deleteReviewModal = createModal("modal-delete-review");

let currentReviewId = null;

document.querySelectorAll(".btn-open-view-review").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const data = row.dataset;

        currentReviewId = data.reseñaId;

        document.querySelector("#delete-review-form").action = `/dashboard/reseñas/eliminar/${currentReviewId}`;

        document.querySelector("#modal-reseña-id").textContent = data.reseñaId;
        document.querySelector("#modal-reseña-nombre-apellido").textContent = data.nombreApellido;
        document.querySelector("#modal-reseña-reserva-id").textContent = data.reservaId;
        document.querySelector("#modal-reseña-fecha").textContent = data.fecha;
        document.querySelector("#modal-reseña-ambiente").textContent = data.ambiente;
        document.querySelector("#modal-reseña-servicio").textContent = data.servicio;
        document.querySelector("#modal-reseña-comida").textContent = data.comida;
        document.querySelector("#modal-reseña-comentario").textContent = data.comentario;

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
