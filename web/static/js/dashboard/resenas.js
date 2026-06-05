function parseDate(str) {
    const [day, month, year] = str.split("-").map(Number);
    return new Date(year, month - 1, day);
}


import { createTableFilter } from "./core.js";

const rows = document.querySelectorAll(".resena-fila");
const form = document.querySelector(".form-filter");

const inputs = {
    resena_id: form.querySelector("#filter-resena-id"),
    reserva_id: form.querySelector("#filter-resena-reserva-id"),
    fecha_desde: form.querySelector("#filter-fecha-desde"),
    fecha_hasta: form.querySelector("#filter-fecha-hasta"),
    ambiente: form.querySelector("#filter-resena-ambiente"),
    servicio: form.querySelector("#filter-resena-servicio"),
    comida: form.querySelector("#filter-resena-comida")
};

createTableFilter({
    inputs,
    rows,

    getRowData: (row) => {
        const raw = row.querySelector(".resena-fecha").textContent;

        return {
            resena_id: row.querySelector(".resena-id").textContent,
            reserva_id: row.querySelector(".resena-reserva-id").textContent,
            fecha: parseDate(raw),
            ambiente: row.querySelector(".resena-ambiente").textContent,
            servicio: row.querySelector(".resena-servicio").textContent,
            comida: row.querySelector(".resena-comida").textContent
        };
    },

    matchRow: (data) => {
        const resena_id = inputs.resena_id.value.trim();
        const reserva_id = inputs.reserva_id.value.trim();
        const fecha_desde = inputs.fecha_desde.value ? new Date(inputs.fecha_desde.value).getTime() : null;
        const fecha_hasta = inputs.fecha_hasta.value ? new Date(inputs.fecha_hasta.value).getTime() : null;
        const ambiente = inputs.ambiente.value;
        const servicio = inputs.servicio.value;
        const comida = inputs.comida.value;
        const rowDate = data.fecha.getTime();

        return (
            (!resena_id || data.resena_id.includes(resena_id)) &&
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
