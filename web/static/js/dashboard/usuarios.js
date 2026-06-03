import { createTableFilter } from "./core.js";

const rows = document.querySelectorAll(".usuario-fila");
const form = document.querySelector(".form-filter");

const inputs = {
    nombre_apellido: form.querySelector("#filter-nombre-apellido"),
    usuario_id: form.querySelector("#filter-usuario-id"),
    email: form.querySelector("#filter-usuario-email"),
    rol: form.querySelector("#filter-usuario-rol")
};

createTableFilter({
    inputs,
    rows,

    getRowData: (row) => ({
        nombre: row.querySelector(".usuario-nombre").textContent.toLowerCase(),
        apellido: row.querySelector(".usuario-apellido").textContent.toLowerCase(),
        usuario_id: row.querySelector(".usuario-id").textContent,
        email: row.querySelector(".usuario-email").textContent.toLowerCase(),
        rol: row.dataset.rol
    }),

    matchRow: (data) => {
        const nombre_apellido = inputs.nombre_apellido.value.toLowerCase().trim();
        const id = inputs.usuario_id.value.trim();
        const email = inputs.email.value.toLowerCase().trim();
        const rol = inputs.rol.value;

        return (
            (!nombre_apellido || data.nombre.includes(nombre_apellido) || data.apellido.includes(nombre_apellido)) &&
            (!id || data.usuario_id.includes(id)) &&
            (!email || data.email.includes(email)) &&
            (rol === "all" || rol === data.rol)
        );
    }
});


import { createModal } from "./core.js";

const addUserModal = createModal("modal-add-user");
const editUserRoleModal = createModal("modal-edit-user-role");

document
    .getElementById("btn-open-add-user")
    .addEventListener("click", () => addUserModal.open());

document.querySelectorAll(".btn-open-edit-user-role").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const rol = row.dataset.rol;

        document.querySelector("#edit-user-role").value = rol;

        editUserRoleModal.open();
    });
});
