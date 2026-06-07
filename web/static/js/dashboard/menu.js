import { createTableFilter } from "./core.js";

const rows = document.querySelectorAll(".producto-fila");
const form = document.querySelector(".form-filter");

const inputs = {
    nombre: form.querySelector("#filter-nombre"),
    min: form.querySelector("#filter-precio-min"),
    max: form.querySelector("#filter-precio-max"),
    categoria: form.querySelector("#filter-categoria")
};

createTableFilter({
    inputs,
    rows,

    getRowData: (row) => ({
        nombre: row.querySelector(".producto-nombre").textContent.toLowerCase(),
        precio: parseFloat(row.querySelector(".producto-precio").textContent.replace("$", "")),
        categoria: row.dataset.categoria
    }),

    matchRow: (data) => {
        const nombre = inputs.nombre.value.toLowerCase().trim();
        const min = parseFloat(inputs.min.value) || 0;
        const max = parseFloat(inputs.max.value) || Infinity;
        const categoria = inputs.categoria.value;

        return (
            (!nombre || data.nombre.includes(nombre)) &&
            (data.precio >= min && data.precio <= max) &&
            (categoria === "all" || categoria === data.categoria)
        );
    }
});


import { createModal } from "./core.js";

const addProductModal = createModal("modal-add-product");
const viewCategoriesModal = createModal("modal-view-categories");
const addCategoryModal = createModal("modal-add-category");
const editCategoryModal = createModal("modal-edit-category");
const editProductModal = createModal("modal-edit-product");

document
    .getElementById("btn-open-add-product")
    .addEventListener("click", () => addProductModal.open());

document
    .getElementById("btn-open-view-categories")
    .addEventListener("click", () => viewCategoriesModal.open());

document
    .getElementById("btn-open-add-category")
    .addEventListener("click", () => addCategoryModal.open());

document.querySelectorAll(".btn-open-edit-category").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");

        document.querySelector("#edit-cat-id").value = row.dataset.id;
        document.querySelector("#edit-category-name").value =
            row.querySelector(".cat-nombre").textContent.trim();

        editCategoryModal.open();
    });
});

document.querySelectorAll(".btn-open-edit-product").forEach(btn => {
    btn.addEventListener("click", (event) => {
        const row = event.currentTarget.closest("tr");

        document.querySelector("#edit-product-id").value = row.dataset.id;
        document.querySelector("#edit-product-name").value = row.querySelector(".producto-nombre").textContent;
        document.querySelector("#edit-product-price").value = row.querySelector(".producto-precio").textContent.replace("$", "");
        document.querySelector("#edit-product-description").value = row.querySelector(".producto-descripcion").textContent;
        document.querySelector("#edit-product-category").value = row.dataset.catId;

        editProductModal.open();
    });
});

const formDelete = document.getElementById('form-delete-menu');
const inputTipo = document.getElementById('delete-tipo');
const inputId = document.getElementById('delete-id');

const handleDelete = (tipo, id) => {
    if (confirm(`¿Estás seguro de que deseas eliminar este ${tipo}?`)) {
        inputTipo.value = tipo;
        inputId.value = id;
        formDelete.submit();
    }
};

document.querySelectorAll('.btn-delete-trigger, .btn-delete-product').forEach(btn => {
    btn.addEventListener('click', (event) => {
        const modal = event.currentTarget.closest('.modal-overlay');
        const tipo = event.currentTarget.dataset.tipo;
        
        const idInput = modal.querySelector('input[name="id"]');
        
        if (idInput && tipo) {
            handleDelete(tipo, idInput.value);
        }
    });
});

document.querySelectorAll('.btn-delete-category').forEach(btn => {
    btn.addEventListener('click', (event) => {
        const row = event.currentTarget.closest("tr");
        const id = row.dataset.id;
        
        handleDelete('categoria', id);
    });
});
