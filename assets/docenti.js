const triennale = "triennale";
const magistrale = "magistrale"

window.onload = function() {

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

    autoWrite();

};

/**
 * Auto-write text
 */

const text2write = [
    "Lista dei docenti"
];
const speed = 25;
var i = 0;
var s;
  
function autoWrite() {
    s = document.querySelector(".auto-write-text");
    write();
};
  
function write() {
    if (i < text2write[0].length) {
        s.innerHTML += text2write[0][i];
        i++;
        setTimeout(write, speed + Math.random() * 25);
    } else {
        s.innerHTML += ' <img src="../icons/icons8-graduation-cap-48.png" height="30em" />';
    }

}