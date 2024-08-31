document.getElementById('logoutButton').addEventListener('click', function(event) {
    event.preventDefault();

    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar botones de Log In y Registrarse
            document.querySelector('a[href="#loginModal"]').style.display = 'inline-block';
            document.querySelector('a[href="#registerModal"]').style.display = 'inline-block';

            // Ocultar ícono de usuario
            document.getElementById('userDropdown').style.display = 'none';

            // Redirigir a la página principal
            window.location.href = '/';
        } else {
            // Mostrar ventana emergente de error
            alert('Logout failed.');
        }
    })
    .catch(error => {
        // Mostrar ventana emergente de error
        alert('An error occurred: ' + error.message);
    });
});