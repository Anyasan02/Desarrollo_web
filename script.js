// SEMANA 7: Uso de arreglos, estructuras repetitivas y simulación de plantillas dinámicas

const forma = document.getElementById("formProducto");
const lista = document.getElementById("listaProductos");
const contador = document.getElementById("contador");

const inputNombre = document.getElementById("nombre");
const inputDescripcion = document.getElementById("descripcion");
const selectCategoria = document.getElementById("categoria");

// ==========================================================================
// 1. ARREGLO DE OBJETOS: Representación de datos del proyecto (Requerido Semana 7)
// ==========================================================================
let BD_PRODUCTOS = [
    {
        id: 1,
        nombre: "Croquetas ProPlan",
        categoria: "Alimento",
        descripcion: "Alimento balanceado premium para perros adultos de raza mediana."
    },
    {
        id: 2,
        nombre: "Pelota de Goma",
        categoria: "Juguetes",
        descripcion: "Juguete mordedor altamente resistente para el estrés canino."
    }
];

// Variable global para controlar los IDs únicos
let proximoId = 3;

// ==========================================================================
// 2. ESTRUCTURA REPETITIVA Y CONDICIONAL PARA RENDERIZAR (Requerido Semana 7)
// ==========================================================================
function renderizarProductos() {
    // Limpiar el contenedor antes de renderizar
    lista.innerHTML = "";

    // ESTRUCTURA CONDICIONAL: Muestra un mensaje según el estado de los datos
    if (BD_PRODUCTOS.length === 0) {
        lista.innerHTML = `
            <div class="col-12 text-center my-4">
                <div class="alert alert-warning border-dashed py-4" role="alert">
                    ⚠️ No hay productos registrados en el catálogo actualmente.
                </div>
            </div>
        `;
        contador.textContent = 0;
        return;
    }

    // ESTRUCTURA REPETITIVA: Recorre el arreglo para mostrar los registros en tarjetas Bootstrap
    BD_PRODUCTOS.forEach(function(producto) {
        const elemento = document.createElement("div");
        elemento.className = "col-md-4 mb-3";
        elemento.innerHTML = `
            <div class="card p-3 shadow-sm h-100 border-start border-success border-4">
                <span class="badge bg-secondary align-self-start mb-2">${producto.categoria}</span>
                <h5 class="fw-bold text-dark">${producto.nombre}</h5>
                <p class="small text-secondary mb-3">${producto.descripcion}</p>
                <button class="btn btn-danger btn-sm mt-auto btn-eliminar" data-id="${producto.id}">Eliminar</button>
            </div>
        `;
        lista.appendChild(elemento);
    });

    // Actualizar el número de registros en pantalla
    contador.textContent = BD_PRODUCTOS.length;

    // Asignar el evento click para eliminar a los botones generados
    asignarEventosEliminar();
}

function asignarEventosEliminar() {
    const botones = document.querySelectorAll(".btn-eliminar");
    botones.forEach(function(boton) {
        boton.addEventListener("click", function(e) {
            const idEliminar = parseInt(e.target.getAttribute("data-id"));
            
            // Filtrar el arreglo sacando el producto seleccionado
            BD_PRODUCTOS = BD_PRODUCTOS.filter(producto => producto.id !== idEliminar);
            
            // Volver a renderizar la lista actualizada
            renderizarProductos();
        });
    });
}

// ==========================================================================
// 3. CONSERVACIÓN DE LAS VALIDACIONES DE LA SEMANA 6 (Requerido)
// ==========================================================================
function validarNombre() {
    const valor = inputNombre.value.trim();
    if (valor === "" || valor.length < 3) {
        inputNombre.classList.add("is-invalid");
        inputNombre.classList.remove("is-valid");
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
        inputDescripcion.classList.add("is-invalid");
        inputDescripcion.classList.remove("is-valid");
        return false;
    } else {
        inputDescripcion.classList.remove("is-invalid");
        inputDescripcion.classList.add("is-valid");
        return true;
    }
}

function validarCategoria() {
    if (selectCategoria.value === "") {
        selectCategoria.classList.add("is-invalid");
        selectCategoria.classList.remove("is-valid");
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

// Escuchar cambios en tiempo real
inputNombre.addEventListener("input", validarNombre);
inputNombre.addEventListener("blur", validarNombre);
inputDescripcion.addEventListener("input", validarDescripcion);
inputDescripcion.addEventListener("blur", validarDescripcion);
selectCategoria.addEventListener("change", validarCategoria);

// ==========================================================================
// 4. CAPTURA DEL SUBMIT: Agregar nuevos datos al arreglo global
// ==========================================================================
forma.addEventListener("submit", function (mi) {
    mi.preventDefault();

    const nValido = validarNombre();
    const dValido = validarDescripcion();
    const cValido = validarCategoria();

    if (!nValido || !dValido || !cValido) {
        return; 
    }

    // REGISTRO DE DATOS: Crear un nuevo objeto y meterlo al arreglo
    const nuevoProducto = {
        id: proximoId,
        nombre: inputNombre.value.trim(),
        categoria: selectCategoria.value,
        descripcion: inputDescripcion.value.trim()
    };

    BD_PRODUCTOS.push(nuevoProducto);
    proximoId++; // Incrementar ID para el siguiente producto

    // Volver a dibujar toda la interfaz desde el arreglo actualizado
    renderizarProductos();

    // Resetear formulario
    forma.reset();
    limpiarEstilos();
});

// Carga inicial automatica de los datos cuando abre la página
renderizarProductos();
