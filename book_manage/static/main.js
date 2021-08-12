
const bxMenu = document.querySelector('.bx-menu');
const bxX = document.querySelector('.bx-x');
const navBar = document.querySelector('.nav-bar');

// Show/Hide nav menus

// show nav menu
bxMenu.addEventListener('click', () => {
    navBar.classList.toggle('show-nav_bar');
    bxX.classList.toggle('show');
    bxMenu.classList.toggle('hide');
})

// hide nav menu
bxX.addEventListener('click', () => {
    navBar.classList.remove('show-nav_bar');
    bxX.classList.remove('show');
    bxMenu.classList.remove('hide');
})