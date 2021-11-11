let listElements = document.querySelectorAll('.list__button--click'); 

listElements.forEach(listElement => {
    listElement.addEventListener('click', ()=>{
        
        listElement.classList.toggle('arrow');

        let height = 0;
        let menu = listElement.nextElementSibling;
        if(menu.clientHeight == "0"){
            height=menu.scrollHeight;
        }

        menu.style.height = `${height}px`;

    })
});

function mostrarPassword(){
    var objeto = document.getElementById("password");
    objeto.type = "text";
}

function ocultarPassword(){
    var obj = document.getElementById("password");
    obj.type = "password";
}

/**
* Alterna una clase de un elemento (la elimina si existe, la añade si no)
* @param {object}<Element> elemento - Elemento a manipular
* @param {object}<String> clase - Clase a alternar
* @returns {boolean} True si se añadió la clase, False si se eliminó
*/

function alternarClase(elemento, clase) {
    var clases, i;
    clase = '' + clase;
    if (!(elemento instanceof Element)) {
      throw new TypeError('Se esperaba un elemento');
    }
    if (clase === '' || clase.indexOf(' ') !== -1) {
      throw new SyntaxError('Nombre de clase no válido');
    }
    if (elemento.classList) {
      // Usa el método nativo toggle, si está disponible
      return elemento.classList.toggle(clase);
    } else if (elemento.className === '') {
      elemento.className = clase;
      return true;
    } else {
      clases = elemento.className.split(' ');
      for (i = 0; clases[i] !== clase && i < clases.length; i++);
      if (i < clases.length) {
        clases.splice(i, 1);
      } else {
        clases.push(clase);
      }
      elemento.className = clases.join(' ');
      return clases[i] === clase;
    }
  }