function actualizarBoton() {
    var ambiente = document.querySelector('input[name="ambiente"]:checked');
    var servicio = document.querySelector('input[name="servicio"]:checked');
    var comida   = document.querySelector('input[name="comida"]:checked');
    document.getElementById('botonEnviar').disabled = !(ambiente && servicio && comida);
}

document.querySelectorAll('.estrellas input').forEach(function(input) {
    input.addEventListener('change', actualizarBoton);
});
