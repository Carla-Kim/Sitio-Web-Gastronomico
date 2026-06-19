const menu_chart = document.getElementById("menu-chart");
const reseñas_chart = document.getElementById("reseñas-chart");
const reservas_por_mes_chart = document.getElementById("reservas-por-mes-chart");
const reservas_por_estado_chart = document.getElementById("reservas-por-estado-chart");

const dashboard = JSON.parse(
    document.getElementById("dashboard-data").textContent
);
const menu = dashboard.productos_por_categoria
const reservas_por_mes = dashboard.reservas_por_mes
const reservas_por_estado = dashboard.reservas_por_estado
const reseñas = dashboard.promedio_resenas
document.getElementById("total-reservas-estado").textContent = reservas_por_estado.cantidades.reduce((a, b) => a + b, 0);

new Chart(
    menu_chart,
    {
        type: "bar",

        data: {
            labels: menu.categorias,

            datasets: [
                {
                    label: "Cantidad",
                    data: menu.cantidades,
                    yAxisID: "y"
                },

                {
                    label: "Precio Promedio",
                    data: menu.precios_promedio,
                    yAxisID: "y1"
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                y: {
                    position: "left",

                    title: {
                        display: true,
                        text: "Cantidad"
                    }
                },

                y1: {
                    position: "right",

                    title: {
                        display: true,
                        text: "Precio promedio"
                    },

                    grid: {
                        drawOnChartArea: false
                    }
                }
            },

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
        type: "radar",

        data: {
            labels: [
                "Ambiente",
                "Servicio",
                "Comida",
                "General"
            ],

            datasets: [{
                label: "Promedio",

                data: [
                    reseñas.ambiente,
                    reseñas.servicio,
                    reseñas.comida,
                    reseñas.general
                ]
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                r: {
                    min: 0,
                    max: 5,

                    ticks: {
                        stepSize: 1
                    }
                }
            },

            plugins: {
                title: {
                    display: true,
                    text: "Promedio de reseñas"
                }
            }
        }
    }
);

new Chart(
    reservas_por_mes_chart,
    {
        type: "line",

        data: {
            labels: reservas_por_mes.meses,

            datasets: [{
                label: "Reservas",
                data: reservas_por_mes.cantidades
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
    reservas_por_estado_chart,
    {
        type: "bar",

        data: {
            labels: reservas_por_estado.estados,

            datasets: [{
                label: "Reservas",
                data: reservas_por_estado.cantidades
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                title: {
                    display: true,
                    text: "Reservas por estado"
                }
            }
        }
    }
);
