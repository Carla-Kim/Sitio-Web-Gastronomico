const nav = document.querySelector('nav');
const toggle = document.querySelector('.menu-toggle');
const overlay = document.querySelector('.nav-overlay');
const close = document.querySelector('.menu-close');

window.addEventListener('scroll', () => {
    if (window.scrollY>10) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});
console.log("Hola")

toggle.addEventListener('click', () => {
    overlay.classList.add('open');
});
close.addEventListener('click', () => {
    overlay.classList.remove('open');
});