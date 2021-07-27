window.onload = function() {
    const slideBar = document.querySelector("#slide-bar");
    const triennale = document.querySelector("#triennale");
    const magistrale = document.querySelector("#magistrale")

    document.querySelector("#switch-button").addEventListener("click", function(){
        slideBar.classList.toggle("right");
        triennale.classList.toggle("toggled");
        magistrale.classList.toggle("toggled");
    });
};