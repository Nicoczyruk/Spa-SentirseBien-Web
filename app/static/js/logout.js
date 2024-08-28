document.getElementById('logoutButton').addEventListener('click', function(event) {
    event.preventDefault();

    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => {
        if (response.ok) {
            // Mostrar botones de Log In y Registrarse
            document.querySelector('a[href="#loginModal"]').style.display = 'block';
            document.querySelector('a[href="#registerModal"]').style.display = 'block';

            // Ocultar ícono de usuario
            document.getElementById('userDropdown').style.display = 'none';
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