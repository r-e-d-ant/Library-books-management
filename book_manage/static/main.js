
'use strict'

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

// show librarian name
const userIcon = document.querySelector('.user-icon-container');
if(userIcon){
    const librarianName = document.querySelector('.librarian_name');
    userIcon.addEventListener('click', () => {
        librarianName.classList.toggle('show-librarian-name');
    })
}else {
    console.log("I love u")
}

// --- hide / show password ---
// show password
const showPasswordIcon = document.querySelector('.bxs-show');
const hidePasswordIcon = document.querySelector('.bxs-hide');
const passswordInput = document.querySelector('.password-input');

showPasswordIcon.addEventListener('click', ()=> {
    passswordInput.type = "text";
    showPasswordIcon.classList.toggle('hide');
    hidePasswordIcon.classList.remove('hide');
})

// hide password
hidePasswordIcon.addEventListener('click', ()=> {
    passswordInput.type = "password";
    showPasswordIcon.classList.remove('hide');
    hidePasswordIcon.classList.toggle('hide');
})