// ================= PRODUCTOS DINÁMICOS =================
let productos = [];

const formularioProducto = document.getElementById("formProducto");
const listaProductos = document.getElementById("listaProductos");
const contador = document.getElementById("contador");

if (formularioProducto) {
    formularioProducto.addEventListener("submit", function(e){
        e.preventDefault();

        let nombre = document.getElementById("nombre").value.trim();
        let descripcion = document.getElementById("descripcion").value.trim();
        let categoria = document.getElementById("categoria").value;
        let mensaje = document.getElementById("mensaje");

        // VALIDACIÓN NOMBRE
        if(nombre.length < 3){
            mensaje.innerHTML = `<div class="alert alert-danger">El nombre debe tener mínimo 3 caracteres</div>`;
            return;
        }

        // VALIDACIÓN DESCRIPCIÓN
        if(descripcion.length < 5){
            mensaje.innerHTML = `<div class="alert alert-danger">La descripción es demasiado corta</div>`;
            return;
        }

        // VALIDACIÓN CATEGORÍA
        if(categoria === ""){
            mensaje.innerHTML = `<div class="alert alert-danger">Seleccione una categoría</div>`;
            return;
        }

        let producto = {
            nombre: nombre,
            descripcion: descripcion,
            categoria: categoria
        };

        productos.push(producto);
        mostrarProductos();

        mensaje.innerHTML = `<div class="alert alert-success">Producto registrado correctamente ✔️</div>`;
        formularioProducto.reset();
    });
}

function mostrarProductos(){
    if (!listaProductos) return;
    listaProductos.innerHTML="";

    productos.forEach((producto, index)=>{
        let tarjeta = document.createElement("div");
        tarjeta.className="col-md-4";
        tarjeta.innerHTML = `
        <div class="producto shadow">
            <h4>${producto.nombre}</h4>
            <p>${producto.descripcion}</p>
            <span class="badge bg-success">${producto.categoria}</span>
            <br><br>
            <button class="btn btn-danger" onclick="eliminarProducto(${index})">Eliminar</button>
        </div>
        `;
        listaProductos.appendChild(tarjeta);
    });

    if (contador) contador.textContent = productos.length;
}

function eliminarProducto(index){
    productos.splice(index, 1);
    mostrarProductos();
}

// Permitir que el botón interactivo de eliminar responda en Flask
window.eliminarProducto = eliminarProducto;

function mostrarCategoria(nombre){
    alert("Mostrando productos de la categoría: " + nombre);
}

// ================= VALIDACIÓN CONTACTO =================
const formularioContacto = document.getElementById("formContacto");

if (formularioContacto) {
    formularioContacto.addEventListener("submit", function(e){
        e.preventDefault();

        let nombre = document.getElementById("nombreUsuario");
        let correo = document.getElementById("correo");
        let respuesta = document.getElementById("respuestaContacto");
        let correcto = true;

        if(!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$/.test(nombre.value.trim())){
            nombre.classList.add("is-invalid");
            nombre.classList.remove("is-valid");
            correcto = false;
        } else {
            nombre.classList.remove("is-invalid");
            nombre.classList.add("is-valid");
        }

        if(!correo.value.includes("@")){
            correo.classList.add("is-invalid");
            correo.classList.remove("is-valid");
            correcto = false;
        } else {
            correo.classList.remove("is-invalid");
            correo.classList.add("is-valid");
        }

        if(correcto){
            respuesta.innerHTML = `<div class="alert alert-success mt-3">Mensaje enviado correctamente ✔️</div>`;
            formularioContacto.reset();
        } else {
            respuesta.innerHTML = `<div class="alert alert-danger mt-3">Revise los campos ingresados</div>`;
        }
    });
}

// ================= VALIDACIÓN EN TIEMPO REAL =================
const inputNombre = document.getElementById("nombreUsuario");
if (inputNombre) {
    inputNombre.addEventListener("input", function(){
        if(/^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$/.test(this.value)){
            this.classList.add("is-valid");
            this.classList.remove("is-invalid");
        } else {
            this.classList.add("is-invalid");
            this.classList.remove("is-valid");
        }
    });
}

const inputCorreo = document.getElementById("correo");
if (inputCorreo) {
    inputCorreo.addEventListener("input", function(){
        if(this.value.includes("@")){
            this.classList.add("is-valid");
            this.classList.remove("is-invalid");
        } else {
            this.classList.add("is-invalid");
            this.classList.remove("is-valid");
        }
    });
}
