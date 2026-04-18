document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("canvas-limpieza");
    if (!canvas) return;

    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const pibbleSucio = document.getElementById("pibble-sucio");
    const boton = document.getElementById("boton-login");
    const barra = document.getElementById("barra-progreso");
    const mensaje = document.getElementById("mensaje");
    const porcentajeTexto = document.getElementById("porcentaje");

    let dibujando = false;
    let pixelesIniciales = null;
    let pixelesTotalesOpacos = 0;

    function ajustarCanvas() {
        const rect = pibbleSucio.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return;

        canvas.width = rect.width;
        canvas.height = rect.height;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const img = pibbleSucio;

        const naturalRatio = img.naturalWidth / img.naturalHeight;
        const containerRatio = rect.width / rect.height;

        let drawWidth, drawHeight, offsetX, offsetY;

        // Simula object-fit: contain
        if (naturalRatio > containerRatio) {
            drawWidth = rect.width;
            drawHeight = rect.width / naturalRatio;
            offsetX = 0;
            offsetY = (rect.height - drawHeight) / 2;
        } else {
            drawHeight = rect.height;
            drawWidth = rect.height * naturalRatio;
            offsetX = (rect.width - drawWidth) / 2;
            offsetY = 0;
        }

        ctx.drawImage(
            pibbleSucio,
            0,
            0,
            img.naturalWidth,
            img.naturalHeight,
            offsetX,
            offsetY,
            drawWidth,
            drawHeight
        );

        // Guardar estado inicial
        pixelesIniciales = ctx.getImageData(0, 0, canvas.width, canvas.height);

        const data = pixelesIniciales.data;
        pixelesTotalesOpacos = 0;

        for (let i = 3; i < data.length; i += 4) {
            if (data[i] > 0) {
                pixelesTotalesOpacos++;
            }
        }

        // Ocultar la imagen HTML original
        pibbleSucio.style.visibility = "hidden";

        actualizarProgreso();
    }

    function inicializarCanvas() {
        if (pibbleSucio.complete && pibbleSucio.naturalWidth > 0) {
            ajustarCanvas();
        } else {
            pibbleSucio.onload = ajustarCanvas;
        }
    }

    window.addEventListener("resize", ajustarCanvas);
    inicializarCanvas();

    function limpiar(x, y) {
        ctx.save();
        ctx.globalCompositeOperation = "destination-out";
        ctx.beginPath();
        ctx.arc(x, y, 40, 0, Math.PI * 2); // Cambié 20 por 40 para que el cepillo sea más grande
        ctx.fill();
        ctx.restore();
    }

    function actualizarProgreso() {
        if (!pixelesIniciales || pixelesTotalesOpacos === 0) {
            barra.style.width = "0%";
            if (porcentajeTexto) porcentajeTexto.textContent = "0%";
            return;
        }

        const imageDataActual = ctx.getImageData(
            0,
            0,
            canvas.width,
            canvas.height
        );

        const actual = imageDataActual.data;
        const inicial = pixelesIniciales.data;

        let borrados = 0;

        for (let i = 3; i < actual.length; i += 4) {
            // Solo contar píxeles que originalmente eran visibles
            if (inicial[i] > 0 && actual[i] === 0) {
                borrados++;
            }
        }

        let porcentaje = Math.round(
            (borrados / pixelesTotalesOpacos) * 100
        );

        porcentaje = Math.min(Math.max(porcentaje, 0), 100);

        barra.style.width = porcentaje + "%";
        if (porcentajeTexto) {
            porcentajeTexto.textContent = porcentaje + "%";
        }

        if (porcentaje >= 100) {
            barra.style.width = "100%";
            if (porcentajeTexto) porcentajeTexto.textContent = "100%";
            boton.classList.add("activo");
            mensaje.innerHTML = "¡YAAAAAAAAAAY!";

            boton.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
    }

    function obtenerPosicion(e) {
        const rect = canvas.getBoundingClientRect();
        if (e.touches) {
            return {
                x: e.touches[0].clientX - rect.left,
                y: e.touches[0].clientY - rect.top,
            };
        }
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        };
    }

    function iniciarDibujo(e) {
        dibujando = true;
        canvas.classList.add("canvas-activo");

        const pos = obtenerPosicion(e);
        limpiar(pos.x, pos.y);
        actualizarProgreso();
    }


    let contador = 0;

    function dibujar(e) {
        if (!dibujando) return;
        e.preventDefault();

        const pos = obtenerPosicion(e);
        limpiar(pos.x, pos.y);

        contador++;
        if (contador % 10 === 0) {
            actualizarProgreso();
        }
    }

    function detenerDibujo() {
        dibujando = false;
        canvas.classList.remove("canvas-activo");
    }

    canvas.addEventListener("mousedown", iniciarDibujo);
    canvas.addEventListener("mousemove", dibujar);
    canvas.addEventListener("mouseup", detenerDibujo);
    canvas.addEventListener("mouseleave", detenerDibujo);

    canvas.addEventListener("touchstart", iniciarDibujo);
    canvas.addEventListener("touchmove", dibujar);
    canvas.addEventListener("touchend", detenerDibujo);
});