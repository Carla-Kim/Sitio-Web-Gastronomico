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

new Chart(
    menu_chart,
    {
        type: "polarArea",

        data: {
            labels: menu.categorias,

            datasets: [{
                label: "Menús",
                data: menu.cantidades
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                title: {
                    display: true,
                    text: "Productos por categoría"
                }
            }
        }
    }
);

new Chart(
    reseñas_chart,
    {
        type: "bar",

        data: {
            labels: reseñas.aspectos,

            datasets: [{
                label: "Reseñas",
                data: reseñas.promedios
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                title: {
                    display: true,
                    text: "Promedio de Reseñas"
                }
            }
        }
    }
);

new Chart(
    reservas_chart,
    {
        type: "line",

        data: {
            labels: reservas.meses,

            datasets: [{
                label: "Reservas",
                data: reservas.cantidades
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                title: {
                    display: true,
                    text: "Reservas por mes"
                }
            }
        }
    }
);

new Chart(
    usuarios_chart,
    {
        type: "bar",

        data: {
            labels: usuarios.roles,

            datasets: [{
                label: "Usuarios",
                data: usuarios.cantidades
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            indexAxis: "y",

            plugins: {
                title: {
                    display: true,
                    text: "Usuarios por rol"
                }
            }
        }
    }
);
