document.addEventListener('DOMContentLoaded', function() {
    fetch('/check_session')
    .then(response => response.json())
    .then(data => {
        if (data.logged_in) {
            // Ocultar botones de Log In y Registrarse
            document.querySelector('a[href="#loginModal"]').style.display = 'none';
            document.querySelector('a[href="#registerModal"]').style.display = 'none';

            // Mostrar ícono de usuario con el nombre de usuario
            document.getElementById('userDropdown').style.display = 'block';
            document.getElementById('usernameDisplay').innerText = data.username;
        } else {
            // Mostrar botones de Log In y Registrarse
            document.querySelector('a[href="#loginModal"]').style.display = 'inline-block';
            document.querySelector('a[href="#registerModal"]').style.display = 'inline-block';

            // Ocultar ícono de usuario
            document.getElementById('userDropdown').style.display = 'none';
        }
    });
});