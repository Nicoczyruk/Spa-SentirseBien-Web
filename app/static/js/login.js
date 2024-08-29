// static/js/login.js

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${email}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Cerrar modal de login
            const loginModal = document.getElementById('loginModal');
            const modalInstance = bootstrap.Modal.getInstance(loginModal);
            modalInstance.hide();

            // Ocultar botones de Log In y Registrarse
            document.querySelector('a[href="#loginModal"]').style.display = 'none';
            document.querySelector('a[href="#registerModal"]').style.display = 'none';

            // Mostrar ícono de usuario
            document.getElementById('userDropdown').style.display = 'block';
        } else {
            // Mostrar ventana emergente de error
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => {
        // Mostrar ventana emergente de error
        alert('An error occurred: ' + error.message);
    });
});