const nav = document.querySelector('nav');
const toggle = document.querySelector('.menu-toggle');
const overlay = document.querySelector('.nav-overlay');
const close = document.querySelector('.menu-close');
const navLinks = document.querySelectorAll('.nav-overlay ul li a');

const fechaInput = document.getElementById('fecha');
if (fechaInput) {
    fechaInput.min = new Date().toISOString().split('T')[0];
}

window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

toggle.addEventListener('click', () => {
    overlay.classList.add('open');
});
close.addEventListener('click', () => {
    overlay.classList.remove('open');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        overlay.classList.remove('open');
    });
});