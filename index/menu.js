const sidebarBTN = document.getElementById("sidebar"); // Botao na header

// Registra um click no botao da header
sidebarBTN.addEventListener("click", () => {
  // Sidebar a ser alterada
  const sidebar = document.querySelector(".sidebar-hidden");
  const button = document.querySelector("#sidebar-button");

 

  // Alterna a visibilidade da sidebar
  sidebar.classList.toggle("sidebar-shown");

  button.classList.toggle("bx-x-circle"); 
});
