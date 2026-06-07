function toggleHidden(idSeccion) {
    const seccion = document.getElementById(idSeccion);
    if (!seccion) return; // en el caso de que no haya secciones con ese id, no hacer nada

    const listaProductos = seccion.querySelector('.menu-items');
    if (listaProductos) {
        listaProductos.classList.toggle('hidden'); // Saca o pone 'hidden' para el display
    }
}
