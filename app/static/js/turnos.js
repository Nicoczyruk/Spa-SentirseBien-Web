// Confirmar la cancelación del turno
function confirmarCancelacion(turnoId) {
    if (confirm("¿Estás seguro de que deseas cancelar este turno?")) {
        fetch(`/cancelar_turno/${turnoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => {
            if (response.ok) {
                alert('Turno cancelado exitosamente.');
                window.location.reload(); // Recargar la página para reflejar los cambios
            } else {
                alert('Hubo un problema al cancelar el turno.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al cancelar el turno.');
        });
    }
}

// Manejar el modal de modificación de turno
document.addEventListener('DOMContentLoaded', function () {
    const modificarTurnoModal = document.getElementById('modificarTurnoModal');
    modificarTurnoModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const turnoId = button.getAttribute('data-turno-id');
        const fecha = button.getAttribute('data-fecha');
        const hora = button.getAttribute('data-hora');

        const turnoIdInput = document.getElementById('turnoId');
        const fechaInput = document.getElementById('fecha');
        const horaInput = document.getElementById('hora');

        turnoIdInput.value = turnoId;
        fechaInput.value = fecha;
        horaInput.value = hora;

        // Modificar la acción del formulario
        document.getElementById('modificarTurnoForm').action = "/modificar_turno/" + turnoId;
    });
});