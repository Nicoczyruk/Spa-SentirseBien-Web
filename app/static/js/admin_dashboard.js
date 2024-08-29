document.addEventListener('DOMContentLoaded', function () {
    const generateBtn = document.getElementById('generateEmployeeBtn');
    const confirmBtn = document.getElementById('confirmEmployeeBtn');
    const generatedEmployeeDiv = document.getElementById('generatedEmployee');
    const generatedUsernameSpan = document.getElementById('generatedUsername');
    const generatedPasswordSpan = document.getElementById('generatedPassword');
    const generatedEmailSpan = document.getElementById('generatedEmail'); // Nuevo elemento para mostrar el email

    generateBtn.addEventListener('click', function () {
        // Generar nombre de usuario, contraseña y correo electrónico aleatorios
        const username = 'empleado_' + Math.floor(Math.random() * 10000);
        const password = Math.random().toString(36).slice(-8);
        const email = `${username}@spasentirsebien.com`; // Generar correo basado en el nombre de usuario

        generatedUsernameSpan.textContent = username;
        generatedPasswordSpan.textContent = password;
        generatedEmailSpan.textContent = email; // Mostrar el correo generado

        generatedEmployeeDiv.style.display = 'block';
    });

    confirmBtn.addEventListener('click', function () {
        // Enviar datos al servidor para confirmar la creación del empleado
        fetch('/create_employee', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: generatedUsernameSpan.textContent,
                password: generatedPasswordSpan.textContent,
                email: generatedEmailSpan.textContent // Enviar el correo generado
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Empleado creado exitosamente.');
                generatedEmployeeDiv.style.display = 'none';
                window.location.reload(); // Recargar la página para actualizar la lista de empleados
            } else {
                alert('Error al crear empleado: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error al crear empleado: ' + error.message);
        });
    });
});
