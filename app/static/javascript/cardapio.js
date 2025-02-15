const coll = document.getElementsByClassName("collapsible");

function updateMaxHeight(content) {
    if (content.style.maxHeight) {
        content.style.maxHeight = content.scrollHeight + "px";
    }
}

for (let i = 0; i < coll.length; i++) {
    const content = coll[i].nextElementSibling;
    content.style.maxHeight = content.scrollHeight + "px"; // Abre por padrão

    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });

    // Atualiza altura ao redimensionar a janela
    window.addEventListener("resize", () => updateMaxHeight(content));

    // Usa MutationObserver para detectar mudanças no layout (ex: DevTools)
    const observer = new MutationObserver(() => updateMaxHeight(content));
    observer.observe(content, { attributes: true, childList: true, subtree: true });
}