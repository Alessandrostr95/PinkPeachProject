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
