

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
        const id = row.dataset.id;
        const nombre = row.querySelector(".serv-nombre").textContent.trim();

        document.querySelector("#edit-service-id").value = id;
        document.querySelector("#edit-service-name").value = nombre;

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
        document.querySelector("#modal-reserva-nombre-apellido").textContent = data.nombrecompleto;
        document.querySelector("#modal-reserva-dni").textContent = data.dni;
        document.querySelector("#modal-reserva-telefono").textContent = data.telefono;
        document.querySelector("#modal-reserva-servicios").textContent = data.servicios;
        document.querySelector("#modal-reserva-cantidad").textContent = data.cantidad;
        document.querySelector("#modal-reserva-estado").textContent = data.estado;
        document.querySelector("#hidden-id-reserva").value = data.id;
        document.querySelector("#hidden-id-reserva-ingreso").value = data.id; 

        viewReservationModal.open();
    });
});
