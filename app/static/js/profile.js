document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('editButton');
    const saveButton = document.getElementById('saveButton');
    const profileFields = document.querySelectorAll('.profile-field');

    // Habilitar campos de edición
    editButton.addEventListener('click', function () {
        profileFields.forEach(field => {
            field.readOnly = false;
            field.classList.add('editable'); // Añadir clase para estilo de borde editable
        });
        editButton.style.display = 'none';
        saveButton.style.display = 'inline-block';
    });

    // Al enviar el formulario
    document.getElementById('editProfileForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const nombre = document.getElementById('nombreField').value;
        const apellido = document.getElementById('apellidoField').value;
        const email = document.getElementById('emailField').value;
        const telefono = document.getElementById('telefonoField').value;
        const direccion = document.getElementById('direccionField').value;

        fetch('/perfil', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `nombre=${nombre}&apellido=${apellido}&email=${email}&telefono=${telefono}&direccion=${direccion}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Datos actualizados con éxito');
                profileFields.forEach(field => {
                    field.readOnly = true;
                    field.classList.remove('editable'); // Remover clase de borde editable
                });
                editButton.style.display = 'inline-block';
                saveButton.style.display = 'none';
            } else {
                alert('Error al actualizar los datos');
            }
        })
        .catch(error => {
            alert('Error en la conexión');
        });
    });
});
