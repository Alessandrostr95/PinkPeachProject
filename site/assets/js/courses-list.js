var currentYear = "";
var text2write = "";
const speed = 25;
var i = 0;
var s;

window.onload = function() {
  currentYear = document.getElementById("current-year").innerHTML;

  /**
   * Auto-write text
   */
  text2write = [
    "Lista corsi " + currentYear  // trovare un modo per modificare l'anno in maniera dinamica
  ];
  
  const speed = 25;
  var i = 0;
  var s;  
  
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
      s.innerHTML += ' <img src="../../assets/icons/icons8-book-80.png" height="30em" />';
  }

}

function filtra() {
  var input = document.getElementById("inputCorso");
  var filter = input.value.toUpperCase();
  var table = document.getElementById("listaCorsi");
  var tr = table.querySelectorAll("tbody tr");

  var match = [];
  for (let i = 0; i < tr.length; i++) {
    match.push(false);
  }

  for (let i = 0; i < tr.length; i++) {
    let td = tr[i].getElementsByTagName("td");

    let nome = td[0];
    let codice = td[1];
    let anno = td[2];

    function is_similar(s) {
        let txtValue = s.textContent || s.innerText;
        if(txtValue && txtValue.toUpperCase().indexOf(filter) > -1) {
            return true;
        } else {
            return false;
        }
    }
    match[i] = is_similar(nome) || is_similar(codice) || is_similar(anno);
  }

  for (let i = 0; i < tr.length; i++) {
    tr[i].style.display = match[i] ? "" : "none";
  }
}
