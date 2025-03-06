document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("btn_add_row").addEventListener("click", mostrarFormulario);
    document.getElementById("new-gasto-form").addEventListener("submit", enviarNuevoGasto);
});

function mostrarFormulario() {
    // Muestra el formulario de nuevo gasto (quitando la clase d-none)
    document.getElementById("new-gasto-form").classList.remove("d-none");
    // Opcional: Deshabilita el botón de "Agregar Gasto" mientras se muestra el formulario
    document.getElementById("btn_add_row").disabled = true;
}

function cancelNewRow() {
    // Oculta el formulario y limpia los campos
    document.getElementById("new-gasto-form").reset();
    document.getElementById("new-gasto-form").classList.add("d-none");
    document.getElementById("btn_add_row").disabled = false;
}

function enviarNuevoGasto(e) {
    e.preventDefault();
    var form = document.getElementById("new-gasto-form");
    var formData = new FormData(form);
    // Convertir los datos del form a un objeto
    var data = {};
    formData.forEach(function(value, key) {
        data[key] = value;
    });
    
    // Enviar datos vía AJAX al endpoint /add_gasto
    fetch("{{ url_for('gastos.add_gasto') }}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
            // Agregar CSRF token si lo requieres
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Insertar la nueva fila en la tabla sin recargar la página
            agregarFilaTabla(result.gasto);
            // Limpiar y ocultar el formulario
            cancelNewRow();
        } else {
            alert("Error: " + result.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error al guardar el gasto");
    });
}

function agregarFilaTabla(gasto) {
    var tbody = document.getElementById("gastos-tbody");
    var newRow = document.createElement("tr");
    newRow.setAttribute("data-id", gasto.id);

    // Crear celdas con los datos recibidos
    newRow.innerHTML = `
        <td>${gasto.nombre}</td>
        <td>${gasto.monto}</td>
        <td>${gasto.fecha}</td>
        <td>${gasto.cuotas || ''}</td>
        <td>${gasto.primera_cuota}</td>
        <td>${gasto.descripcion}</td>
        <td>${gasto.categoria}</td>
        <td>
            <button class="btn btn-danger btn-sm" onclick="deleteGasto(${gasto.id})">Eliminar</button>
        </td>
    `;
    tbody.appendChild(newRow);
}

function deleteGasto(id) {
    if (confirm("¿Estás seguro de eliminar este gasto?")) {
        fetch("/delete_gasto/" + id, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
                // Agrega CSRF token si es necesario
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var row = document.querySelector(`tr[data-id='${id}']`);
                if (row) {
                    row.remove();
                }
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error al eliminar el gasto");
        });
    }
}
