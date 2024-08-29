document.addEventListener('DOMContentLoaded', function () {
    const responseForm = document.getElementById('responseForm');

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

function openResponseModal(consultaId, mensaje) {
    console.log("Consulta ID:", consultaId); // Verifica que el ID es correcto

    // Rellenar los campos ocultos y el mensaje en el modal
    document.getElementById('consultaId').value = consultaId;
    document.getElementById('mensajeConsulta').value = mensaje;

    // Mostrar el modal de respuesta
    const responseModal = new bootstrap.Modal(document.getElementById('responseModal'));
    responseModal.show();
}


