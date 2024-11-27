/* 
  Fichier de script combiné pour gérer le login (Task 1) 
  et l'affichage des lieux (Task 2).
*/

// ----------------------- TASK 1: LOGIN -----------------------
// Fonction utilitaire pour effectuer la requête de connexion
async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    return response; // Retourne la réponse pour traitement
  } catch (error) {
    console.error('Erreur lors de la requête:', error);
    throw error;
  }
}

// Fonction utilitaire pour récupérer un cookie par son nom
function getCookie(name) {
  const cookieArr = document.cookie.split(';');
  for (let cookie of cookieArr) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) {
      return value;
    }
  }
  return null;
}

// ----------------------- TASK 2: AUTHENTICATION CHECK -----------------------
// Vérifie si l'utilisateur est authentifié
function checkAuthentication() {
  const token = getCookie('token'); // Récupère le token JWT
  const loginLink = document.getElementById('login-link'); // Lien de connexion

  if (!token) {
    loginLink.style.display = 'block'; // Afficher le lien de connexion si pas de token
  } else {
    loginLink.style.display = 'none'; // Masquer le lien de connexion si authentifié
    console.log('Utilisateur authentifié');
    fetchPlaces(token); // Charge les lieux si l'utilisateur est authentifié
  }
}

// ----------------------- TASK 2: FETCH PLACES -----------------------
// Récupère la liste des lieux depuis l'API
async function fetchPlaces(token) {
  try {
    const response = await fetch('https://your-api-url/places', { // Remplace par l'URL de ton API
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`, // Inclut le token JWT dans l'en-tête
      }
    });

    if (response.ok) {
      const places = await response.json(); // Récupère les lieux sous forme de JSON
      displayPlaces(places); // Affiche les lieux
    } else {
      console.error('Erreur lors de la récupération des lieux:', response.statusText);
    }
  } catch (error) {
    console.error('Erreur réseau:', error);
  }
}

// ----------------------- TASK 3: DISPLAY PLACES -----------------------
// Affiche dynamiquement la liste des lieux
function displayPlaces(places) {
  const placesList = document.getElementById('places-list'); // Sélectionne la section où les lieux seront affichés
  placesList.innerHTML = ''; // Efface le contenu actuel pour éviter les duplications

  places.forEach(place => {
    // Crée un conteneur pour chaque lieu
    const placeCard = document.createElement('div');
    placeCard.classList.add('place-card'); // Ajoute une classe pour styliser les lieux (CSS)
    placeCard.setAttribute('data-price', place.price); // Ajoute l'attribut data-price pour le filtrage

    // Remplit les informations du lieu
    placeCard.innerHTML = `
      <h2>${place.name}</h2>
      <p>${place.description}</p>
      <p><strong>Prix par nuit :</strong> ${place.price}€</p>
      <p><strong>Localisation :</strong> ${place.location}</p>
      <button class="details-button">View Details</button>
        `;

    // Ajoute le lieu à la section des lieux
    placesList.appendChild(placeCard);
  });

  // Ajoute le filtre après l'affichage des lieux
  addPriceFilter();
}

// ----------------------- TASK 4: FILTER PLACES -----------------------
// Fonction pour filtrer les lieux affichés en fonction du prix sélectionné
function addPriceFilter() {
  const priceFilter = document.getElementById('price-filter'); // Récupère le menu déroulant de filtrage
  const placeCards = document.querySelectorAll('.place-card'); // Récupère toutes les cartes des lieux

  if (priceFilter) {
    // Ajoute un écouteur sur le menu déroulant
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value; // Récupère la valeur sélectionnée

      // Parcourt chaque carte de lieu et applique le filtre
      placeCards.forEach((card) => {
        const placePrice = parseInt(card.getAttribute('data-price'), 10); // Récupère le prix de la carte

        // Affiche ou masque la carte en fonction du filtre
        if (selectedPrice === 'All' || placePrice <= parseInt(selectedPrice, 10)) {
          card.style.display = 'block'; // Affiche la carte
        } else {
          card.style.display = 'none'; // Masque la carte
        }
      });
    });
  }
}

// ----------------------- TASK 1: LOGIN EVENT -----------------------
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form'); // Récupère le formulaire de connexion

  // Vérifie l'authentification au chargement de la page
  checkAuthentication();

  if (loginForm) {
    // Ajoute un écouteur pour l'événement "submit" du formulaire
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      // Récupère les valeurs saisies dans le formulaire
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      // Vérifie que les champs ne sont pas vides
      if (!email || !password) {
        alert('Veuillez remplir tous les champs avant de soumettre.');
        return;
      }

      // Désactive le bouton de soumission temporairement
      const submitButton = loginForm.querySelector('button[type="submit"]');
      submitButton.disabled = true;
      submitButton.textContent = 'Connexion en cours...';

      try {
        // Envoie la requête de connexion
        const response = await loginUser(email, password);

        if (response.ok) {
          const data = await response.json(); // Récupère les données en JSON

          // Stocke le token dans un cookie
          document.cookie = `token=${data.access_token}; path=/; secure; samesite=strict`;

          // Redirige l'utilisateur vers la page principale
          alert('Connexion réussie ! Vous allez être redirigé.');
          window.location.href = 'index.html';
        } else {
          const error = await response.json();
          alert(`Erreur: ${error.message || 'Identifiants incorrects. Veuillez réessayer.'}`);
        }
      } catch (error) {
        console.error('Une erreur est survenue lors de la connexion:', error);
        alert('Une erreur est survenue. Veuillez réessayer plus tard.');
      } finally {
        submitButton.disabled = false; // Réactive le bouton de soumission
        submitButton.textContent = 'Login';
      }
    });
  }
});