const Btn =  document.querySelector('.slicknav_btn');
const menu = document.querySelector('.slicknav_menu');
const icon = document.querySelector('.logo');

Btn.addEventListener('click', () => {
    menu.classList.toggle('active');
    icon.classList.toggle('active');
})