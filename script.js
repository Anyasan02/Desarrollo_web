const form = document.getElementById("formProducto");
const lista = document.getElementById("listaProductos");
const contador = document.getElementById("contador");

let total = 0;

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;

    if (nombre === "" || descripcion === "" || categoria === "") {
        alert("Completa todos los campos");
        return;
    }

    const col = document.createElement("div");
    col.classList.add("col-md-4");

    const card = document.createElement("div");
    card.classList.add("card", "p-3", "shadow-sm");

    const titulo = document.createElement("h5");
    titulo.textContent = nombre;
    titulo.classList.add("text-success");

    const desc = document.createElement("p");
    desc.textContent = descripcion;

    const cat = document.createElement("span");
    cat.textContent = categoria;
    cat.classList.add("badge", "bg-success");

    const btn = document.createElement("button");
    btn.textContent = "Eliminar";
    btn.classList.add("btn", "btn-danger", "btn-sm", "mt-2");

    btn.addEventListener("click", function () {
        col.remove();
        total--;
        contador.textContent = total;
    });

    card.appendChild(titulo);
    card.appendChild(desc);
    card.appendChild(cat);
    card.appendChild(btn);

    col.appendChild(card);
    lista.appendChild(col);

    total++;
    contador.textContent = total;

    form.reset();
});