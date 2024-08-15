document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('establishment-form');
    const submitBtn = document.getElementById('submit-btn');
    const establishmentsContainer = document.getElementById('establishments-container');
    const modal = document.getElementById('modal');
    const modalForm = document.getElementById('modal-form');
    const closeModalBtn = document.querySelector('.close');
    const notification = document.getElementById('notification');
    const loginForm = document.getElementById('login-form');
    const loginNotification = document.getElementById('login-notification');
    const loginContainer = document.getElementById('login-container');
    const contentContainer = document.getElementById('content-container');
    let editingEstablishmentRuc = null;

    const ADMIN_USERNAME = 'rmrivera@espe.edu.ec';
    const ADMIN_PASSWORD = 'rmrivera2022';

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
            loginContainer.style.display = 'none';
            contentContainer.style.display = 'block';
        } else {
            loginNotification.textContent = 'Usuario o contraseña incorrectos';
            loginNotification.classList.add('error');
            loginNotification.style.display = 'block';
            setTimeout(() => {
                loginNotification.style.display = 'none';
            }, 3000);
        }
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const establishment = {
            ruc: document.getElementById('ruc').value,
            commercial_name: document.getElementById('commercial_name').value,
            legal_name: document.getElementById('legal_name').value,
            address: document.getElementById('address').value,
            phone: document.getElementById('phone').value,
            contact_name: document.getElementById('contact_name').value,
            establishment_type: document.getElementById('establishment_type').value,
            logo_image: document.getElementById('logo_image').value,
        };

        addEstablishment(establishment);
    });

    modalForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const establishment = {
            ruc: document.getElementById('modal-ruc').value,
            commercial_name: document.getElementById('modal-commercial_name').value,
            legal_name: document.getElementById('modal-legal_name').value,
            address: document.getElementById('modal-address').value,
            phone: document.getElementById('modal-phone').value,
            contact_name: document.getElementById('modal-contact_name').value,
            establishment_type: document.getElementById('modal-establishment_type').value,
            logo_image: document.getElementById('modal-logo_image').value,
        };

        updateEstablishment(establishment);
    });

    closeModalBtn.addEventListener('click', function() {
        closeModal();
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    function addEstablishment(establishment) {
        fetch('/api/establishments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(establishment),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification('Error al añadir el comercio', 'error');
            } else {
                showNotification('Comercio añadido con éxito', 'success');
                loadEstablishments();
                form.reset();
            }
        })
        .catch(error => showNotification('Error al añadir el comercio', 'error'));
    }

    function updateEstablishment(establishment) {
        fetch('/api/establishments', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(establishment),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification('Error al actualizar el comercio', 'error');
            } else {
                showNotification('Comercio actualizado con éxito', 'success');
                loadEstablishments();
                closeModal();
            }
        })
        .catch(error => showNotification('Error al actualizar el comercio', 'error'));
    }

    function deleteEstablishment(ruc) {
        fetch(`/api/establishments/${ruc}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification('Error al eliminar el comercio', 'error');
            } else {
                showNotification('Comercio eliminado con éxito', 'success');
                loadEstablishments();
            }
        })
        .catch(error => showNotification('Error al eliminar el comercio', 'error'));
    }

    function loadEstablishments() {
        fetch('/api/establishments')
            .then(response => response.json())
            .then(data => {
                establishmentsContainer.innerHTML = '';
                data.forEach(establishment => {
                    const card = document.createElement('div');
                    card.className = 'establishment-card';

                    const logo = document.createElement('img');
                    logo.src = establishment.logo_image;
                    logo.alt = `${establishment.commercial_name} logo`;
                    card.appendChild(logo);

                    const name = document.createElement('h3');
                    name.textContent = establishment.commercial_name;
                    card.appendChild(name);

                    const type = document.createElement('p');
                    type.textContent = `Tipo: ${establishment.establishment_type}`;
                    card.appendChild(type);

                    const address = document.createElement('p');
                    address.textContent = `Dirección: ${establishment.address}`;
                    card.appendChild(address);

                    const phone = document.createElement('p');
                    phone.textContent = `Teléfono: ${establishment.phone}`;
                    card.appendChild(phone);

                    const contact = document.createElement('p');
                    contact.textContent = `Contacto: ${establishment.contact_name}`;
                    card.appendChild(contact);

                    const editBtn = document.createElement('button');
                    editBtn.className = 'edit-btn';
                    editBtn.textContent = 'Editar';
                    editBtn.addEventListener('click', () => {
                        document.getElementById('modal-ruc').value = establishment.ruc;
                        document.getElementById('modal-commercial_name').value = establishment.commercial_name;
                        document.getElementById('modal-legal_name').value = establishment.legal_name;
                        document.getElementById('modal-address').value = establishment.address;
                        document.getElementById('modal-phone').value = establishment.phone;
                        document.getElementById('modal-contact_name').value = establishment.contact_name;
                        document.getElementById('modal-establishment_type').value = establishment.establishment_type;
                        document.getElementById('modal-logo_image').value = establishment.logo_image;
                        openModal();
                    });
                    card.appendChild(editBtn);

                    const deleteBtn = document.createElement('button');
                    deleteBtn.className = 'delete-btn';
                    deleteBtn.textContent = 'Eliminar';
                    deleteBtn.addEventListener('click', () => {
                        deleteEstablishment(establishment.ruc);
                    });
                    card.appendChild(deleteBtn);

                    establishmentsContainer.appendChild(card);
                });
            })
            .catch(error => showNotification('Error al cargar los comercios', 'error'));
    }

    function openModal() {
        modal.style.display = 'block';
    }

    function closeModal() {
        modal.style.display = 'none';
        modalForm.reset();
    }

    function showNotification(message, type) {
        notification.textContent = message;
        notification.className = 'notification';
        if (type === 'error') {
            notification.classList.add('error');
        }
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }

    loadEstablishments();
});
