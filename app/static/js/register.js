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
            // Cerrar modal y mostrar un mensaje de éxito sin jQuery
            const modal = document.getElementById('registerModal');
            const modalInstance = bootstrap.Modal.getInstance(modal);
            modalInstance.hide();

            alert('Registro exitoso, ahora puedes iniciar sesión.');
        } else {
            // Mostrar el mensaje de error
            alert('Registro fallido: ' + data.message);
        }
    })
    .catch(error => {
        alert('An error occurred: ' + error.message);
    });
});