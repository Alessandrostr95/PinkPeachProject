const triennale = "triennale";
const magistrale = "magistrale"

var currentState = triennale;

var coll;

window.onload = function() {
    const slideBar = document.querySelector("#slide-bar");
    const triennale = document.querySelector("#triennale");
    const magistrale = document.querySelector("#magistrale");
    
    const calendarioTriennale = document.getElementById("calendario-triennale");
    const calendarioMagistrale = document.getElementById("calendario-magistrale");

    document.querySelector("#switch-button").addEventListener("click", function(){
        /**
         * Cambio la radice triennale/magistrale del sito
         * ...
         */
        slideBar.classList.toggle("right");
        triennale.classList.toggle("toggled");
        magistrale.classList.toggle("toggled");
        currentState = currentState === triennale ? magistrale : triennale;
        calendarioTriennale.classList.toggle("hidden");
        calendarioMagistrale.classList.toggle("hidden");
    });


    /*
     * When the user scrolls down, hide the navbar. 
     * When the user scrolls up, show the navbar.
     */
    var prevScrollpos = window.pageYOffset;
    const barraMenu = document.getElementById("barraMenu");

    window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;
        var h = barraMenu.style.height;

        if (prevScrollpos > currentScrollPos) {
            barraMenu.style.top = "0";
            barraMenu.classList.add("ombra-menu");
        } else {
            barraMenu.style.top = `-100px`;
            barraMenu.classList.remove("ombra-menu");
        }
        prevScrollpos = currentScrollPos;
    }


    /* Faccio collassare gli elementi del NAV-TREE quando clicco su un elemento padre */
    coll = document.querySelectorAll(".tree .tree-node");
    console.log( coll );

    for(let i = 0; i < coll.length; i++){
        let u = coll[i].parentElement.querySelector("ul");
        if( u ) {
            coll[i].addEventListener("click", function(){
                // console.log( u );
                u.classList.toggle("hidden");
            });
        }
    }

};