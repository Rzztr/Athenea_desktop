
function mostrarMapa(latitud, longitud) {
    console.log("Latitud:", latitud, "Longitud:", longitud); // Depuración

    const modal = document.getElementById("mapModal");
    modal.style.display = "block";

    const mapa = new google.maps.Map(document.getElementById("map"), {
        center: { lat: parseFloat(latitud), lng: parseFloat(longitud) },
        zoom: 15,
    });

    new google.maps.Marker({
        position: { lat: parseFloat(latitud), lng: parseFloat(longitud) },
        map: mapa,
    });
}

function cerrarMapa() {
    const modal = document.getElementById("mapModal");
    modal.style.display = "none";
}

// Asociar eventos a los botones
document.addEventListener("DOMContentLoaded", () => {
    const mapButtons = document.querySelectorAll(".mapButton");
    const closeButton = document.querySelector(".closeButton");

    // Asignar evento a cada botón "Ver Mapa"
    mapButtons.forEach(button => {
        button.addEventListener("click", () => {
            const lat = button.getAttribute("data-lat");
            const lng = button.getAttribute("data-lng");
            mostrarMapa(lat, lng);
        });
    });

    // Evento para cerrar el modal
    closeButton.addEventListener("click", cerrarMapa);
});
// Función para eliminar una ubicación
function eliminarUbicacion(id, rowElement) {
    if (confirm("¿Estás seguro de que deseas eliminar esta ubicación?")) {
        fetch(`/eliminar_ubicacion/${id}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje) {
                    alert(data.mensaje);
                    // Eliminar la fila de la tabla
                    rowElement.remove();
                }
            })
            .catch(error => {
                console.error("Error al eliminar la ubicación:", error);
                alert("Hubo un error al intentar eliminar la ubicación.");
            });
    }
}

// Asignar eventos a los botones "Eliminar"
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".deleteButton");

    deleteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const id = button.getAttribute("data-id");
            const rowElement = button.closest("tr"); // La fila completa
            eliminarUbicacion(id, rowElement);
        });
    });
});

