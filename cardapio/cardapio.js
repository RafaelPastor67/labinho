const sidebarBTN = document.getElementById("sidebar"); // Botao na header

// Registra um click no botao da header
sidebarBTN.addEventListener(
  "click",
  /*function (event)*/ () => {
    const sidebar = document.querySelector(".sidebar-hidden");
    const button = document.querySelector("#sidebar-button");

    button.classList.toggle("bx-x-circle"); 
    sidebar.classList.toggle("sidebar-shown");
  }
);

var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        // Abra o conteúdo colapsável por padrão
        var content = coll[i].nextElementSibling;
        content.style.maxHeight = content.scrollHeight + "px";

        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }


