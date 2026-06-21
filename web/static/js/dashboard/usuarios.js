import { createModal } from "./core.js";

const rows = document.querySelectorAll(".usuario-fila");
const form = document.querySelector(".form-filter");

const inputs = {
    nombre_apellido: form.querySelector("#filter-nombre-apellido"),
    email: form.querySelector("#filter-usuario-email"),
    rol: form.querySelector("#filter-usuario-rol")
};

const formEditCompleto = document.getElementById('form-edit-user-completo');

formEditCompleto.addEventListener('submit', (e) => {
    const selectRol = document.getElementById('input-full-rol');
    
    if (selectRol.disabled) {
        selectRol.disabled = false;
    }
});

const addUserModal = createModal("modal-add-user");
const editUserParcialModal = createModal("modal-edit-user-parcial");
const editUserCompletoModal = createModal("modal-edit-user-completo");

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
        const idUsuarioFila = String(row.dataset.usuarioId);
        const currentUserId = String(document.body.dataset.userId);
        
        document.querySelector("#input-full-id").value = idUsuarioFila;
        document.querySelector("#input-full-username").value = row.dataset.usuarioUsuario;
        document.querySelector("#input-full-nombre").value = row.dataset.nombre;
        document.querySelector("#input-full-apellido").value = row.dataset.apellido;
        document.querySelector("#input-full-email").value = row.dataset.email;
        document.querySelector("#input-full-password").value = row.dataset.password;

        
        const selectRol = document.querySelector("#input-full-rol");
        selectRol.value = row.dataset.rol;

        const btnBorrarEnModal = document.querySelector(".btn-delete-user-modal");

        if (idUsuarioFila === currentUserId) {
            selectRol.disabled = true;    
            btnBorrarEnModal.style.display = 'none'; 
        } else {
            selectRol.disabled = false;      
            btnBorrarEnModal.style.display = 'inline-block';
        }
        
        const esUnicoAdmin = (document.querySelectorAll('[data-rol="admin"]').length === 1 && row.dataset.rol === 'admin');
        if (esUnicoAdmin) {
            selectRol.disabled = true; 
        }

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

const toggleBtn = document.getElementById('toggle-pass-btn');
const passwordInput = document.getElementById('edit-user-password');

toggleBtn.addEventListener('click', function() {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.textContent = 'Ocultar';
    } else {
        passwordInput.type = 'password';
        toggleBtn.textContent = 'Mostrar';
    }
});

const deleteModal = document.getElementById('modal-delete-user');
let userIdToDelete = null;

document.querySelectorAll('.btn-delete-user-modal').forEach(btn => {
    btn.addEventListener('click', (event) => {
        userIdToDelete = event.currentTarget.dataset.id;
        editUserParcialModal.close();
        editUserCompletoModal.close();
        deleteModal.classList.remove('hidden');
    });
});

document.getElementById('btn-confirm-delete').addEventListener('click', () => {
    if (userIdToDelete) {
        document.getElementById('delete-id-usuario').value = userIdToDelete;
        document.getElementById('form-delete-usuario').submit();
    }
});

document.getElementById('btn-cancel-delete').addEventListener('click', () => {
    deleteModal.classList.add('hidden');
});

window.addEventListener('DOMContentLoaded', () => {
    const filas = document.querySelectorAll(".usuario-fila");
    
    const admins = Array.from(filas).filter(fila => fila.dataset.rol === 'admin');

    if (admins.length === 1) {
        const filaAdmin = admins[0];
        
        const btnCredenciales = filaAdmin.querySelector(".btn-open-edit-user-role");
        if (btnCredenciales) btnCredenciales.style.display = 'none';
        
        const btnEditarCompleto = filaAdmin.querySelector(".btn-open-edit-completo");
        if (btnEditarCompleto) btnEditarCompleto.style.display = 'none';
        
        console.log("Protección activada: Es el último administrador.");
    }
});