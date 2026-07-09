// SEMANA 6: Validaciones dinámicas 

const forma = document.getElementById("formProducto");
const lista = document.getElementById("listaProductos");
const contador = document.getElementById("contador");

// Captura directa de tus mismos inputs
const inputNombre = document.getElementById("nombre");
const inputDescripcion = document.getElementById("descripcion");
const selectCategoria = document.getElementById("categoria");

let total = 0;

// ==========================================
// FUNCIONES DE VALIDACIÓN EN TIEMPO REAL
// ==========================================

function validarNombre() {
    const valor = inputNombre.value.trim();
    if (valor === "" || valor.length < 3) {
        inputNombre.classList.remove("is-valid");
        inputNombre.classList.add("is-invalid");
        return false;
    } else {
        inputNombre.classList.remove("is-invalid");
        inputNombre.classList.add("is-valid");
        return true;
    }
}

function validarDescripcion() {
    const valor = inputDescripcion.value.trim();
    if (valor === "" || valor.length < 10) {
        inputDescripcion.classList.remove("is-valid");
        inputDescripcion.classList.add("is-invalid");
        return false;
    } else {
        inputDescripcion.classList.remove("is-invalid");
        inputDescripcion.classList.add("is-valid");
        return true;
    }
}

function validarCategoria() {
    const valor = selectCategoria.value;
    if (valor === "") {
        selectCategoria.classList.remove("is-valid");
        selectCategoria.classList.add("is-invalid");
        return false;
    } else {
        selectCategoria.classList.remove("is-invalid");
        selectCategoria.classList.add("is-valid");
        return true;
    }
}

function limpiarEstilos() {
    inputNombre.classList.remove("is-valid", "is-invalid");
    inputDescripcion.classList.remove("is-valid", "is-invalid");
    selectCategoria.classList.remove("is-valid", "is-invalid");
}

// Escuchar eventos dinámicos cuando el usuario escribe (input) o sale del campo (blur)
inputNombre.addEventListener("input", validarNombre);
inputNombre.addEventListener("blur", validarNombre);

inputDescripcion.addEventListener("input", validarDescripcion);
inputDescripcion.addEventListener("blur", validarDescripcion);

selectCategoria.addEventListener("change", validarCategoria);

// ==========================================
// CAPTURA DEL EVENTO SUBMIT (Misma lógica S5)
// ==========================================
forma.addEventListener("submit", function (mi) {
    mi.preventDefault();

    // Validar todo antes de dejar registrar
    const nValido = validarNombre();
    const dValido = validarDescripcion();
    const cValido = validarCategoria();

    if (!nValido || !dValido || !cValido) {
        return; // No hace nada si hay errores visuales
    }

    // Tu lógica exacta de la semana 5
    total++;
    contador.textContent = total;

    const elemento = document.createElement("div");
    elemento.className = "col-md-4 mb-3";
    elemento.innerHTML = `
        <div class="card p-3 shadow-sm h-100 border-start border-success border-4">
            <h5>${inputNombre.value.trim()}</h5>
            <p class="text-muted small mb-1"><strong>Categoría:</strong> ${selectCategoria.value}</p>
            <p class="small text-secondary">${inputDescripcion.value.trim()}</p>
            <button class="btn btn-danger btn-sm boton-eliminar mt-auto">Eliminar</button>
        </div>
    `;

    lista.appendChild(elemento);

    elemento.querySelector(".boton-eliminar").addEventListener("click", function() {
        elemento.remove();
        total--;
        contador.textContent = total;
    });

    forma.reset();
    limpiarEstilos();
});
