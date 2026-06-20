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

const DORADO = "#C9A84C";
const DORADO_SUAVE = "rgba(201, 168, 76, 0.25)";
const MUTED = "#A09080";
const GRID_COLOR = "rgba(201, 168, 76, 0.12)";

const PALETTE = ["#C9A84C", "#8B7355", "#A09080", "#D4B868", "#7C9473", "#6A6050"];

const ESTADO_COLORES = {
    reservada: "#C9A84C",
    finalizada: "#7C9473",
    cancelada: "#B85C5C"
};

Chart.defaults.color = MUTED;
Chart.defaults.font.family = "'Montserrat', sans-serif";
Chart.defaults.borderColor = GRID_COLOR;
Chart.defaults.plugins.legend.labels.color = MUTED;
Chart.defaults.plugins.title.color = DORADO;
Chart.defaults.plugins.title.font = { size: 14, weight: "600" };

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
                    yAxisID: "y",
                    backgroundColor: DORADO,
                    borderColor: DORADO,
                    borderRadius: 4
                },

                {
                    label: "Precio Promedio",
                    data: menu.precios_promedio,
                    yAxisID: "y1",
                    backgroundColor: MUTED,
                    borderColor: MUTED,
                    borderRadius: 4
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                y: {
                    position: "left",
                    grid: { color: GRID_COLOR },
                    ticks: { color: MUTED },

                    title: {
                        display: true,
                        text: "Cantidad",
                        color: MUTED
                    }
                },

                y1: {
                    position: "right",
                    ticks: { color: MUTED },

                    title: {
                        display: true,
                        text: "Precio promedio",
                        color: MUTED
                    },

                    grid: {
                        drawOnChartArea: false
                    }
                },

                x: {
                    grid: { color: GRID_COLOR },
                    ticks: { color: MUTED }
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
                ],

                backgroundColor: DORADO_SUAVE,
                borderColor: DORADO,
                pointBackgroundColor: DORADO,
                pointBorderColor: "#0C0C0C"
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                r: {
                    min: 0,
                    max: 5,

                    angleLines: { color: GRID_COLOR },
                    grid: { color: GRID_COLOR },
                    pointLabels: { color: MUTED },

                    ticks: {
                        stepSize: 1,
                        color: MUTED,
                        backdropColor: "transparent"
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
                data: reservas_por_mes.cantidades,
                borderColor: DORADO,
                backgroundColor: DORADO_SUAVE,
                pointBackgroundColor: DORADO,
                pointBorderColor: "#0C0C0C",
                tension: 0.1
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                x: {
                    grid: { color: GRID_COLOR },
                    ticks: { color: MUTED }
                },
                y: {
                    grid: { color: GRID_COLOR },
                    ticks: { color: MUTED }
                }
            },

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
                data: reservas_por_estado.cantidades,
                backgroundColor: reservas_por_estado.estados.map(
                    (estado, i) => ESTADO_COLORES[String(estado).toLowerCase()] || PALETTE[i % PALETTE.length]
                ),
                borderRadius: 4
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                x: {
                    grid: { color: GRID_COLOR },
                    ticks: { color: MUTED }
                },
                y: {
                    grid: { color: GRID_COLOR },
                    ticks: { color: MUTED }
                }
            },

            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Reservas por estado"
                }
            }
        }
    }
);
