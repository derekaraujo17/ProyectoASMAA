document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("canvas-limpieza");
    if (!canvas) return;

    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const pibbleSucio = document.getElementById("pibble-sucio");
    const boton = document.getElementById("boton-login");
    const barra = document.getElementById("barra-progreso");
    const mensaje = document.getElementById("mensaje");

    let dibujando = false;
    let progreso = 0;
    let totalPixeles = 0;
    let pixelesBorrados = 0;

    const porcentajeTexto = document.getElementById("porcentaje");

    function ajustarCanvas() {
        canvas.width = pibbleSucio.clientWidth;
        canvas.height = pibbleSucio.clientHeight;

        ctx.globalCompositeOperation = "source-over";
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Dibujar la imagen sucia en el canvas
        ctx.drawImage(pibbleSucio, 0, 0, canvas.width, canvas.height);

        // Ocultar la imagen original
        pibbleSucio.style.display = "none";

        // Calcular el total de píxeles
        totalPixeles = canvas.width * canvas.height;
    }

    function inicializarCanvas() {
        if (pibbleSucio.complete) {
            ajustarCanvas();
        } else {
            pibbleSucio.onload = ajustarCanvas;
        }
    }

    inicializarCanvas();
    window.addEventListener("resize", ajustarCanvas);

    function limpiar(x, y) {
        ctx.globalCompositeOperation = "destination-out";
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, Math.PI * 2);
        ctx.fill();
    }

    function calcularProgreso() {
        if (totalPixeles === 0) return;

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const pixels = imageData.data;

        let transparentes = 0;

        for (let i = 3; i < pixels.length; i += 4) {
            if (pixels[i] === 0) {
                transparentes++;
            }
        }
        let porcentaje = (transparentes / totalPixeles) * 100;
        // Suavizar el progreso para que no avance tan rápido al inicio
        porcentaje = Math.pow(porcentaje / 100, 1) * 100;
        
        porcentaje = Math.min(100, Math.round(porcentaje));
        //Actualizar barra y texto
        barra.style.width = porcentaje + "%";
        if (porcentajeTexto) {
            porcentajeTexto.textContent = porcentaje + "%";
        }
        // Activar botón al llegar al 100%
        if (porcentaje >= 100) {
            barra.style.width = "100%";
            porcentajeTexto.textContent = "100%"
            boton.classList.add("activo");
            mensaje.innerHTML = "¡Pibble quedó reluciente! 🐶✨";
        }
    }
    
    function obtenerPosicion(e) {
        const rect = canvas.getBoundingClientRect();
        if (e.touches) {
            return {
                x: e.touches[0].clientX - rect.left,
                y: e.touches[0].clientY - rect.top
            };
        }
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    function iniciarDibujo(e) {
        dibujando = true;
        contador = 0;
        const pos = obtenerPosicion(e);
        limpiar(pos.x, pos.y);
        calcularProgreso();
    }
    let contador = 0;

    function dibujar(e) {
        if (!dibujando) return;
        e.preventDefault();

        const pos = obtenerPosicion(e);
        limpiar(pos.x, pos.y);

        contador++;
        if (contador %10 ===0){
            calcularProgreso();
        }
    }

    function detenerDibujo() {
        dibujando = false;
    }

    canvas.addEventListener("mousedown", iniciarDibujo);
    canvas.addEventListener("mousemove", dibujar);
    canvas.addEventListener("mouseup", detenerDibujo);
    canvas.addEventListener("mouseleave", detenerDibujo);

    canvas.addEventListener("touchstart", iniciarDibujo);
    canvas.addEventListener("touchmove", dibujar);
    canvas.addEventListener("touchend", detenerDibujo);
});