document.getElementById("btn-resultados").addEventListener("click", () => {
    window.parent.postMessage({
        type: "ver-resultados"
    }, "*");
});