document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const data = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('registerEmail').value,
        telefono: document.getElementById('telefono').value,
        direccion: document.getElementById('direccion').value,
        nombre_usuario: document.getElementById('nombre_usuario').value,
        password: document.getElementById('registerPassword').value
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Obtener el elemento del modal
            const modal = document.getElementById('registerModal');
            // Obtener la instancia del modal de Bootstrap
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }

            // Mostrar el mensaje de éxito
            alert('Registro exitoso, ahora puedes iniciar sesión.');

            // Recargar la página para eliminar cualquier residual como el backdrop
            window.location.reload();
        } else {
            // Mostrar el mensaje de error
            alert('Registro fallido: ' + data.message);
        }
    })
    .catch(error => {
        alert('Ocurrió un error: ' + error.message);
    });
});
