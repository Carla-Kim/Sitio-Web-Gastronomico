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
            (!rol || rol === data.rol)
        );
    }
});


import { createModal } from "./core.js";

const addUserModal = createModal("modal-add-user");
const editUserParcialModal = createModal("modal-edit-user-parcial");
const editUserCompletoModal = createModal("modal-edit-user-completo");
const viewCredentialsModal = createModal("modal-view-credentials");

document
    .getElementById("btn-open-add-user")
    .addEventListener("click", () => addUserModal.open());

document.querySelectorAll(".btn-open-edit-user-role").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const id = row.dataset.usuarioId;

        document.querySelector("#input-edit-id-usuario").value = id;

        editUserParcialModal.open();
    });
});

document.querySelectorAll(".btn-open-edit-completo").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        
        document.querySelector("#input-full-id").value = row.dataset.usuarioId;
        document.querySelector("#input-full-username").value = row.dataset.usuarioUsuario;
        document.querySelector("#input-full-nombre").value = row.dataset.nombre;
        document.querySelector("#input-full-apellido").value = row.dataset.apellido;
        document.querySelector("#input-full-rol").value = row.dataset.rol;
        document.querySelector("#input-full-email").value = row.dataset.email;
        document.querySelector("#input-full-password").value = row.dataset.password;
        
        editUserCompletoModal.open();
    });
});

const formDelete = document.getElementById('form-delete-usuario');
const inputDeleteId = document.getElementById('delete-id-usuario');

document.querySelectorAll('.btn-open-edit-user-role, .btn-open-edit-completo').forEach(btn => {
    btn.addEventListener('click', (event) => {
        const row = event.currentTarget.closest("tr");
        const id = row.dataset.usuarioId;

        let modal;
        if (event.currentTarget.classList.contains('btn-open-edit-user-role')) {
            modal = document.getElementById('modal-edit-user-parcial');
        } else {
            modal = document.getElementById('modal-edit-user-completo');
        }
        
        const deleteBtn = modal.querySelector('.btn-delete-user-modal');
        if (deleteBtn) {
            deleteBtn.dataset.id = id;
        }
    });
});

document.querySelectorAll('.btn-delete-user-modal').forEach(btn => {
    btn.addEventListener('click', (event) => {
        const id = event.currentTarget.dataset.id;
        
        if (confirm("¿Estás seguro de que deseas eliminar este usuario?")) {
            inputDeleteId.value = id;
            formDelete.submit();
        }
    });
});

document.querySelectorAll('.btn-view-credentials').forEach(button => {
    button.addEventListener('click', function(event) {
        const row = event.target.closest('.usuario-fila');
        
        const email = row.dataset.email;
        const contrasena = row.dataset.contrasena;
        
        document.querySelector('.usuario-email').textContent = email;
        document.querySelector('.usuario-contrasena').textContent = contrasena;
        
        viewCredentialsModal.open();
    });
});
