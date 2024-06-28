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
