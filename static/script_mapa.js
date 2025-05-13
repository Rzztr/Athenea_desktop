let map, marker, latitud, longitud;

// Inicializar el mapa
function initMap(lat = 19.432608, lng = -99.133209) {
  const mapOptions = {
    zoom: 15,
    center: { lat: lat, lng: lng },
  };

  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  marker = new google.maps.Marker({
    position: { lat: lat, lng: lng },
    map: map,
    draggable: false,
    title: "Ubicación actual"
  });
}

// Mostrar ubicación en el mapa
function mostrarUbicacion(position) {
  latitud = position.coords.latitude;
  longitud = position.coords.longitude;

  const posicionActual = { lat: latitud, lng: longitud };
  map.setCenter(posicionActual);
  marker.setPosition(posicionActual);

  alert(`Ubicación obtenida: Latitud ${latitud}, Longitud ${longitud}`);
}

// Manejar errores de geolocalización
function mostrarError(error) {
  let mensaje = '';
  switch (error.code) {
    case error.PERMISSION_DENIED:
      mensaje = "El usuario negó el acceso a la geolocalización.";
      break;
    case error.POSITION_UNAVAILABLE:
      mensaje = "La información de ubicación no está disponible.";
      break;
    case error.TIMEOUT:
      mensaje = "El tiempo para obtener la ubicación se agotó.";
      break;
    case error.UNKNOWN_ERROR:
      mensaje = "Ocurrió un error desconocido.";
      break;
  }
  alert(mensaje);
}

// Enviar ubicación al servidor
function enviarUbicacion() {
  if (!latitud || !longitud) {
    alert("Primero obtén la ubicación.");
    return;
  }

  fetch('/enviar_ubicacion', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ latitud: latitud, longitud: longitud })
  })
  .then(response => response.json())
  .then(data => alert(data.mensaje))
  .catch(error => console.error("Error al enviar la ubicación:", error));
}

// Inicializar el mapa con ubicación por defecto
window.onload = () => initMap();
