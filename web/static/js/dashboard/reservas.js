import { createTableFilter } from "./core.js";

const rows = document.querySelectorAll(".reserva-fila");
const form = document.querySelector(".form-filter");

const inputs = {
    reserva_id: form.querySelector("#filter-reserva-id"),
    estado: form.querySelector("#filter-estado"),
    fecha: form.querySelector("#filter-fecha"),
};

createTableFilter({
    inputs,
    rows,

    getRowData: (row) => ({
        reserva_id: row.querySelector(".reserva-id").textContent,
        estado: row.querySelector(".reserva-estado").textContent.toLowerCase(),
        fecha: row.querySelector(".reserva-fecha").textContent.toLowerCase()
    }),

    matchRow: (data) => {
        const id = inputs.reserva_id.value.trim();
        const estado = inputs.estado.value.trim().toLowerCase();
        const fecha = inputs.fecha.value;

        return (
            (!id || data.reserva_id.includes(id)) &&
            (!estado || data.estado.includes(estado)) &&
            (!fecha || data.fecha === fecha)
        );
    }
});


import { createModal } from "./core.js";

const viewServicesModal = createModal("modal-view-services");
const addServiceModal = createModal("modal-add-service");
const editServiceModal = createModal("modal-edit-service");
const viewReservationModal = createModal("modal-view-reservation");

document
    .getElementById("btn-open-view-services")
    .addEventListener("click", () => viewServicesModal.open());

document
    .getElementById("btn-open-add-service")
    .addEventListener("click", () => addServiceModal.open());

document.querySelectorAll(".btn-open-edit-service").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");

        document.querySelector("#edit-service-name").value =
            row.querySelector(".serv-nombre").textContent.trim();

        editServiceModal.open();
    });
});

document.querySelectorAll(".btn-open-view-reservation").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const data = row.dataset;

        document.querySelector("#modal-reserva-id").textContent = data.id;
        document.querySelector("#modal-reserva-fecha").textContent = data.fecha;
        document.querySelector("#modal-reserva-email").textContent = data.email;
        document.querySelector("#modal-reserva-nombre-apellido").textContent = data.nombreApellido;
        document.querySelector("#modal-reserva-dni").textContent = data.dni;
        document.querySelector("#modal-reserva-telefono").textContent = data.telefono;
        document.querySelector("#modal-reserva-servicios").textContent = data.servicios;
        document.querySelector("#modal-reserva-cantidad").textContent = data.cantidad;
        document.querySelector("#modal-reserva-estado").textContent = data.estado;

        viewReservationModal.open();
    });
});
