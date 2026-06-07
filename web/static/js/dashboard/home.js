const menu_chart = document.getElementById("menu-chart");
const reseñas_chart = document.getElementById("reseñas-chart");
const reservas_chart = document.getElementById("reservas-chart");
const usuarios_chart = document.getElementById("usuarios-chart");

const dashboard = JSON.parse(
    document.getElementById("dashboard-data").textContent
);
const menu = dashboard.menu
const reservas = dashboard.reservas
const reseñas = dashboard.reseñas
const usuarios = dashboard.usuarios

function createChart({
    canvasId,
    type,
    labels,
    data,
    datasetLabel,
    title,
    options = {}
}) {
    return new Chart(
        document.getElementById(canvasId),
        {
            type,

            data: {
                labels,

                datasets: [{
                    label: datasetLabel,
                    data
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    title: {
                        display: !!title,
                        text: title
                    }
                },

                ...options
            }
        }
    );
}

createChart({
    canvasId: "menu-chart",
    type: "polarArea",
    labels: menu.categorias,
    data: menu.cantidades,
    datasetLabel: "Menús",
    title: "Productos por categoría"
});

createChart({
    canvasId: "reseñas-chart",
    type: "bar",
    labels: reseñas.aspectos,
    data: reseñas.promedios,
    datasetLabel: "Reseñas",
    title: "Promedio de Reseñas"
});

createChart({
    canvasId: "reservas-chart",
    type: "line",
    labels: reservas.meses,
    data: reservas.cantidades,
    datasetLabel: "Reservas",
    title: "Reservas por mes"
});

createChart({
    canvasId: "usuarios-chart",
    type: "bar",
    labels: usuarios.roles,
    data: usuarios.cantidades,
    datasetLabel: "Usuarios",
    title: "Usuarios por rol",
    options: {
        indexAxis: "y"
    }
});
