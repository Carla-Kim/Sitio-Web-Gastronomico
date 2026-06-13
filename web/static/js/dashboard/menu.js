import { createTableFilter, createModal } from "./core.js";

const rows = document.querySelectorAll(".producto-fila");
const form = document.querySelector(".form-filter");
const editImageInput = document.querySelector("#edit-product-image");
const addImageInput = document.querySelector("#add-product-image");

const addProductModal = createModal("modal-add-product");
const viewCategoriesModal = createModal("modal-view-categories");
const addCategoryModal = createModal("modal-add-category");
const editCategoryModal = createModal("modal-edit-category");
const editProductModal = createModal("modal-edit-product");

createTableFilter({
    inputs: {
        nombre: document.querySelector("#filter-nombre"),
        min: document.querySelector("#filter-min"), 
        max: document.querySelector("#filter-max"), 
        categoria: document.querySelector("#filter-categoria")
    },
    rows,
    getRowData: (row) => ({
        nombre: row.querySelector(".producto-nombre").textContent.toLowerCase(),
        precio: parseFloat(row.querySelector(".producto-precio").textContent.replace("$", "")),
        categoria: row.dataset.categoria
    }),
    matchRow: (data) => {
        const nombre = document.querySelector("#filter-nombre").value.toLowerCase().trim();
        const min = parseFloat(document.querySelector("#filter-min").value) || 0;
        const max = parseFloat(document.querySelector("#filter-max").value) || Infinity;
        const categoria = document.querySelector("#filter-categoria").value;

        return (
            (!nombre || data.nombre.includes(nombre)) &&
            (data.precio >= min && data.precio <= max) &&
            (categoria === "all" || categoria === data.categoria)
        );
    }
});

document.getElementById("btn-open-add-product").addEventListener("click", () => addProductModal.open());
document.getElementById("btn-open-view-categories").addEventListener("click", () => viewCategoriesModal.open());
document.getElementById("btn-open-add-category").addEventListener("click", () => addCategoryModal.open());

document.querySelectorAll(".btn-open-edit-category").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        document.querySelector("#edit-cat-id").value = row.dataset.id;
        document.querySelector("#edit-category-name").value = row.querySelector(".cat-nombre").textContent.trim();
        editCategoryModal.open();
    });
});

document.querySelectorAll(".btn-open-edit-product").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");
        const data = row.dataset;
        document.querySelector("#edit-product-id").value = data.id;
        document.querySelector("#edit-product-name").value = data.nombre;
        document.querySelector("#edit-product-price").value = data.precio;
        document.querySelector("#edit-product-description").value = data.descripcion;
        document.querySelector("#edit-product-category").value = data.categoria;
        
        const preview = document.querySelector("#edit-product-actual-preview");
        preview.src = data.imagen || "";
        editProductModal.open();
    });
});

const formDelete = document.getElementById('form-delete-menu');
const inputTipo = document.getElementById('delete-tipo');
const inputId = document.getElementById('delete-id');

const openConfirmModal = (tipo, id) => {
    const modalId = tipo === 'producto' ? 'modal-delete-product' : 'modal-delete-category';
    const modal = document.getElementById(modalId);
    
    modal.querySelector('.btn-delete-trigger').onclick = () => {
        inputTipo.value = tipo;
        inputId.value = id;
        formDelete.submit();
    };
    
    modal.classList.remove('hidden');
};

document.querySelectorAll('.btn-delete-category').forEach(btn => {
    btn.addEventListener('click', (event) => {
        const id = event.currentTarget.closest('tr').dataset.id;
        openConfirmModal('categoria', id);
    });
});

document.querySelectorAll('.btn-delete-trigger[data-tipo="producto"]').forEach(btn => {
    btn.addEventListener('click', (event) => {
        const id = document.getElementById('edit-product-id').value;
        openConfirmModal('producto', id);
    });
});

document.querySelectorAll('#btn-cancel-delete-product, #btn-cancel-delete-category').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.target.closest('.modal-overlay').classList.add('hidden');
    });
});