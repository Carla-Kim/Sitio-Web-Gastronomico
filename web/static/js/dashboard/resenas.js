import { createModal, createTableFilter } from "./core.js";

const viewReviewModal = createModal("modal-view-review");
const ocultarReviewModal = createModal("modal-ocultar-review");

let currentReviewId = null;
let currentStatusId = null;

document.querySelectorAll(".btn-open-view-review").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const data = row.dataset;

        currentReviewId = data.resenaId;
        currentStatusId = data.estado;

        const inputHidden = document.querySelector("#input-ocultar-id-resena");
        if (inputHidden) {
            inputHidden.value = currentReviewId;
        }

        const inputEstado = document.querySelector("#input-estado");
        if (inputEstado) {
            inputEstado.value = currentStatusId;
        }

        document.querySelector("#modal-resena-id").textContent = data.resenaId;
        document.querySelector("#modal-resena-nombre-apellido").textContent = data.nombreApellido;
        document.querySelector("#modal-resena-reserva-id").textContent = data.reservaId;
        document.querySelector("#modal-resena-fecha").textContent = data.fecha;
        document.querySelector("#modal-resena-ambiente").textContent = data.ambiente;
        document.querySelector("#modal-resena-servicio").textContent = data.servicio;
        document.querySelector("#modal-resena-comida").textContent = data.comida;
        document.querySelector("#modal-resena-comentario").textContent = data.comentario;
        document.querySelector("#modal-resena-estado").textContent = data.estado;

        viewReviewModal.open();
    });
});

document
    .getElementById("btn-open-ocultar-review")
    .addEventListener("click", () => {
        ocultarReviewModal.open();
    });

document
    .getElementById("btn-cancel-ocultar-review")
    .addEventListener("click", () => {
        ocultarReviewModal.close();
    });

createTableFilter({
    inputs: {
        ambiente: document.getElementById("filter-ambiente"),
        servicio: document.getElementById("filter-servicio"),
        comida: document.getElementById("filter-comida")
    },
    rows: document.querySelectorAll(".resena-fila"),
    getRowData: (row) => ({
        ambiente: row.dataset.ambiente,
        servicio: row.dataset.servicio,
        comida: row.dataset.comida
    }),
    matchRow: (data) => {
        const fAmb = document.getElementById("filter-ambiente").value;
        const fServ = document.getElementById("filter-servicio").value;
        const fCom = document.getElementById("filter-comida").value;

        if (fAmb && data.ambiente !== fAmb) return false;
        if (fServ && data.servicio !== fServ) return false;
        if (fCom && data.comida !== fCom) return false;
        return true;
    }
});