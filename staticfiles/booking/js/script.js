document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        let serviceSelect = document.getElementById("service");
        if (serviceSelect) {
            console.log("Список услуг найден!");
        } else {
            console.error("Список услуг НЕ найден!");
        }
    }, 500); // Ждем 0.5 секунды для загрузки элемента
});

// Эффект изменения фона при прокрутке
window.addEventListener('scroll', function () {
    var navbar = document.querySelector('.navbar');
    if (navbar) {  // Проверяем, существует ли navbar
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});






