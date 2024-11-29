document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');

    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        // Récupération des données du formulaire
        const userData = {
            first_name: document.getElementById('first_name').value.trim(),
            last_name: document.getElementById('last_name').value.trim(),
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value.trim()
        };

        // Validation des champs
        if (!userData.first_name || !userData.last_name || !userData.email || !userData.password) {
            alert('Veuillez remplir tous les champs');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5001/api/v1/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const data = await response.json();

            if (response.ok) {
                alert('Inscription réussie ! Vous allez être redirigé vers la page de connexion.');
                window.location.href = '/login';
            } else {
                alert(data.error || 'Erreur lors de l\'inscription');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Une erreur est survenue lors de l\'inscription');
        }
    });
});
