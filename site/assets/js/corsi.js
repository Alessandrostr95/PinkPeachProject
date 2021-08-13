window.onload = function() {

    /*
     * When the user scrolls down, hide the navbar. 
     * When the user scrolls up, show the navbar.
     */
    var prevScrollpos = window.pageYOffset;
    const barraMenu = document.getElementById("barraMenu");

    window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;
        // var h = barraMenu.style.height;

        if (prevScrollpos > currentScrollPos + 5) {
            barraMenu.style.top = "0";
            barraMenu.classList.add("ombra-menu");
        } else {
            barraMenu.style.top = `-100px`;
            barraMenu.classList.remove("ombra-menu");
        }
        prevScrollpos = currentScrollPos;
    }

    
    /* Faccio collassare gli elementi del NAV-TREE quando clicco su un elemento padre */
    /*
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
    */

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
console.log("\n\n\
▌─────────────────────────▐█─────▐\n\
▌────▄──────────────────▄█▓█▌────▐\n\
▌───▐██▄───────────────▄▓░░▓▓────▐\n\
▌───▐█░██▓────────────▓▓░░░▓▌────▐\n\
▌───▐█▌░▓██──────────█▓░░░░▓─────▐\n\
▌────▓█▌░░▓█▄███████▄███▓░▓█─────▐\n\
▌────▓██▌░▓██░░░░░░░░░░▓█░▓▌─────▐\n\
▌─────▓█████░░░░░░░░░░░░▓██──────▐\n\
▌─────▓██▓░░░░░░░░░░░░░░░▓█──────▐\n\
▌─────▐█▓░░░░░░█▓░░▓█░░░░▓█▌─────▐\n\
▌─────▓█▌░▓█▓▓██▓░█▓▓▓▓▓░▓█▌─────▐\n\
▌─────▓▓░▓██████▓░▓███▓▓▌░█▓─────▐\n\
▌────▐▓▓░█▄▐▓▌█▓░░▓█▐▓▌▄▓░██─────▐\n\
▌────▓█▓░▓█▄▄▄█▓░░▓█▄▄▄█▓░██▌────▐\n\
▌────▓█▌░▓█████▓░░░▓███▓▀░▓█▓────▐\n\
▌───▐▓█░░░▀▓██▀░░░░░─▀▓▀░░▓█▓────▐\n\
▌───▓██░░░░░░░░▀▄▄▄▄▀░░░░░░▓▓────▐\n\
▌───▓█▌░░░░░░░░░░▐▌░░░░░░░░▓▓▌───▐\n\
▌───▓█░░░░░░░░░▄▀▀▀▀▄░░░░░░░█▓───▐\n\
▌──▐█▌░░░░░░░░▀░░░░░░▀░░░░░░█▓▌──▐\n\
▌──▓█░░░░░░░░░░░░░░░░░░░░░░░██▓──▐\n\
▌──▓█░░░░░░░░░░░░░░░░░░░░░░░▓█▓──▐\n\
▌──██░░░░░░░░░░░░░░░░░░░░░░░░█▓──▐\n\
▌──█▌░░░░░░░░░░░░░░░░░░░░░░░░▐▓▌─▐\n\
▌─▐▓░░░░░░░░░░░░░░░░░░░░░░░░░░█▓─▐\n\
▌─█▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓─▐\n\
▌─█▓░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓▌▐\n\
▌▐█▓░░░░░░░░░░░░░░░░░░░░░░░░░░░██▐\n\
▌█▓▌░░░░░░░░░░░░░░░░░░░░░░░░░░░▓█▐\n\
██████████████████████████████████\n\
█░▀░░░░▀█▀░░░░░░▀█░░░░░░▀█▀░░░░░▀█\n\
█░░▐█▌░░█░░░██░░░█░░██░░░█░░░██░░█\n\
█░░▐█▌░░█░░░██░░░█░░██░░░█░░░██░░█\n\
█░░▐█▌░░█░░░██░░░█░░░░░░▄█░░▄▄▄▄▄█\n\
█░░▐█▌░░█░░░██░░░█░░░░████░░░░░░░█\n\
█░░░█░░░█▄░░░░░░▄█░░░░████▄░░░░░▄█\n\
██████████████████████████████████\n\
");