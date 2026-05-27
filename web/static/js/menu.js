function productos_por_categoria(Categorias, Productos) {
    const resultado = []; 
    
    for (let i = 0; i < Categorias.length; i++) {
        const categoria = Categorias[i];
        const productos_categoria = [];
        
        
        for (let j = 0; j < Productos.length; j++) {
            const producto = Productos[j];
            
            if (producto.categorias_id === categoria.categorias_id) {
                productos_categoria.push(producto);
            }
        }
        
        resultado.push([categoria, productos_categoria]);
    }
    
    return resultado; 
}

function toggleHidden(idSeccion) {
    const seccion = document.getElementById(idSeccion);
    if (!seccion) return; // en el caso de que no haya secciones con ese id, no hacer nada

    const listaProductos = seccion.querySelector('.menu-items');
    if (listaProductos) {
        listaProductos.classList.toggle('hidden'); // Saca o pone 'hidden' para el display
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const [res_categorias, res_productos] = await Promise.all([
            fetch('/categorias'), 
            fetch('/productos')   
        ]); // endpoints para obtener categorías y productos

        const Categorias = await res_categorias.json();
        const Productos = await res_productos.json();

        const menu_agrupado = productos_por_categoria(Categorias, Productos);

        const contenedorMenu = document.querySelector(".menu-content");
        contenedorMenu.innerHTML = ""; 

        for (let i = 0; i < menu_agrupado.length; i++) {
            const datos_categoria = menu_agrupado[i][0];
            const productos_categoria = menu_agrupado[i][1];
            
            const index_bucle = i + 1;

            let seccion_html = 
                `<div class="menu-section" id="seccion-${index_bucle}">
                    
                    <div class="category-header" onclick="toggleHidden('seccion-${index_bucle}')" style="cursor: pointer;">
                        <h2 class="menu-section-title">${datos_categoria.nombre}</h2>
                    </div>

                    <ul class="menu-items hidden">`; // 'hidden' para que inicie oculta, se muestra al hacer click en el category-header

            for (let j = 0; j < productos_categoria.length; j++) {
                const producto = productos_categoria[j];

                seccion_html += 
                        `<li class="menu-item">
                            <div class="item-img-container"></div>
                            <div class="item-info">
                                <h3 class="item-name">${producto.nombre}</h3>
                                <p class="item-description">${producto.descripcion}</p>
                                <span class="item-price">$${producto.precio}</span>
                            </div>
                        </li>`;
            }

            seccion_html += 
                    `</ul>
                </div>`;

            contenedorMenu.insertAdjacentHTML('beforeend', seccion_html);
        }

    } catch (error) {
        console.error("Error al procesar o renderizar el menú:", error);
    }
});