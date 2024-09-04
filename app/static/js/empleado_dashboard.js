// Función para formatear fechas (sin segundos ni microsegundos)
function formatFecha(fechaStr) {
    const fecha = new Date(fechaStr);
    const dia = fecha.getDate().toString().padStart(2, '0');
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
    const anio = fecha.getFullYear();
    const horas = fecha.getHours().toString().padStart(2, '0');
    const minutos = fecha.getMinutes().toString().padStart(2, '0');

    return `${dia}/${mes}/${anio} ${horas}:${minutos}`;
}

// Al cargar el DOM
document.addEventListener('DOMContentLoaded', function () {
    const responseForm = document.getElementById('responseForm');
    const fechas = document.querySelectorAll('.fecha-consulta'); // Asegúrate de que las fechas tienen esta clase

    // Formatear las fechas al cargar la página
    fechas.forEach(function (element) {
        const fechaOriginal = element.textContent; // Asume que la fecha está como texto dentro del elemento
        element.textContent = formatFecha(fechaOriginal); // Formatear la fecha y actualizar el contenido
    });

    // Enviar el formulario de respuesta
    if (responseForm) {
        responseForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(responseForm);
            
            fetch('/responder_consulta', {
                method: 'POST',
                body: new URLSearchParams(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Mostrar un mensaje de éxito
                    alert('Consulta respondida correctamente.');

                    // Recargar la página para actualizar la lista de consultas
                    window.location.reload();
                } else {
                    alert('Error al responder la consulta.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ocurrió un error al enviar la respuesta.');
            });
        });
    }
});

// Función para abrir el modal de respuesta
function openResponseModal(consultaId, mensaje) {
    console.log("Consulta ID:", consultaId); // Verifica que el ID es correcto

    // Rellenar los campos ocultos y el mensaje en el modal
    document.getElementById('consultaId').value = consultaId;
    document.getElementById('mensajeConsulta').value = mensaje;

    // Mostrar el modal de respuesta
    const responseModal = new bootstrap.Modal(document.getElementById('responseModal'));
    responseModal.show();
}
