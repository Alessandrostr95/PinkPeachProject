const triennale = "triennale";
const magistrale = "magistrale"

var currentState = triennale;
var currentYear = "20-21"

window.onload = function() {
    /* setto i link della barra del menu */
    document.querySelector("#link-orari").href = `../${currentState}/${currentYear}/orario.html`;
    document.querySelector("#link-corsi").href = `../${currentState}/${currentYear}/corsi.html`;
    document.querySelector("#link-docenti").href = `../${currentState}/${currentYear}/docenti.html`;
    document.querySelector("#link-esami").href = `../${currentState}/${currentYear}/esami.html`;

    const slideBar = document.querySelector("#slide-bar");
    const triennale = document.querySelector("#triennale");
    const magistrale = document.querySelector("#magistrale");
    
    //const calendarioTriennale = document.getElementById("calendario-triennale");
    //const calendarioMagistrale = document.getElementById("calendario-magistrale");

    const navTreeTriennale = document.getElementById("nav-tree-triennale");
    const navTreeMagistrale = document.getElementById("nav-tree-magistrale");

    const newsTriennale = document.getElementById("news-triennale");
    const newsMagistrale = document.getElementById("news-magistrale");

    document.querySelector("#switch-button").addEventListener("click", function(){
        /**
         * Cambio la radice triennale/magistrale del sito
         * ...
         */
        slideBar.classList.toggle("right");
        triennale.classList.toggle("toggled");
        magistrale.classList.toggle("toggled");

        /* switch dello stato interno */
        currentState = currentState == "triennale" ? "magistrale" : "triennale";

        /* switch nel nav-tree */
        navTreeTriennale.classList.toggle("hidden");
        navTreeMagistrale.classList.toggle("hidden");

        /* switch delle news */
        newsTriennale.classList.toggle("hidden");
        newsMagistrale.classList.toggle("hidden");

        /* cambio i link della barra del menu */
        document.querySelector("#link-orari").href = `../${currentState}/${currentYear}/orario.html`;
        document.querySelector("#link-corsi").href = `../${currentState}/${currentYear}/corsi.html`;
        document.querySelector("#link-docenti").href = `../${currentState}/${currentYear}/docenti.html`;
        document.querySelector("#link-esami").href = `../${currentState}/${currentYear}/esami.html`;
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
    var coll = document.querySelectorAll(".tree .tree-node");
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

    autoWrite();

};

/**
 * Auto-write text
 */

const text2write = [
    "Benvenuto nel sito di informatica Tor Vergata.",
    "Fatto dagli studenti per gli studenti ",
];
const speed = 25;
var i = 0;
var s;
  
function autoWrite() {
    s = document.querySelector(".auto-write-text");
    write(0);
};
  
function write(k) {
    if(k == 0) {
        if (i < text2write[0].length) {
            s.innerHTML += text2write[0][i];
            i++;
            setTimeout(() => write(k), speed + Math.random() * 25);
        } else {
            s.innerHTML += "<br/>> ";
            i = 0;
            setTimeout(() => write(1), 500 + Math.random() * 25);
        }
    } else {
        if (i < text2write[1].length) {
            s.innerHTML += text2write[1][i];
            i++;
            setTimeout(() => write(1), speed + Math.random() * 25);
        } else {
            s.innerHTML += '<img src="../assets/icons/icons8-pixel-heart-96.png" height="25em" />';
        }
    }
}

/**
 * 
 * 
 */
console.log("\
_________________________________\n\
| ESPRESSIONE DI UNO STUDENTE    |\n\
| CHE PER LA PRIMA VOLTA VEDE IL |\n\
| SITO DI INFORMATICA UFFICIALE  |\n\
|________________________________|\n\
\n\
     .--'''''''''--.\n\
  .'      .---.      '.\n\
 /    .-----------.    \\\n\
/        .-----.        \\\n\
|       .-.   .-.       |\n\
|      /   \\ /   \\      |\n\
 \\    | .-. | .-. |    /\n\
  '-._| | | | | | |_.-'\n\
      | '-' | '-' |\n\
       \\___/ \\___/\n\
    _.-'  /   \\  `-._\n\
  .' _.--|     |--._ '.\n\
  ' _...-|     |-..._ '\n\
         |     |\n\
         '.___.'\n\
           | |\n\
          _| |_\n\
         /\\(_)/\\\n\
        /  ` '  \\\n\
       | |     | |\n\
       '-'     '-'\n\
       | |     | |\n\
       | |     | |\n\
       | |-----| |\n\
    .`/  |     | |/`.\n\
    |    |     |    |\n\
    '._.'| .-. |'._.'\n\
          \\ | /\n\
          | | |\n\
          | | |\n\
          | | |\n\
         /| | |\\\n\
       .'_| | |_`.\n\
       `. | | | .'\n\
    .    /  |  \\    .\n\
   /o`.-'  / \  `-.` o\\\n\
  /o  o\\ .'   `. /o  o\\\n\
  `.___.'       `.___.'\n\
");