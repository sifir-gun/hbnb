// ----------------------- UTILITAIRES -----------------------
// Fonction pour effectuer la requête de connexion
async function loginUser(email, password) {
  try {
      const response = await fetch('http://127.0.0.1:5001/api/v1/auth/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      
      if (response.ok) {
          // Store the token
          document.cookie = `token=${data.access_token}; path=/; secure; samesite=strict`;
          return response;
      } else {
          throw new Error(data.error || 'Login failed');
      }
  } catch (error) {
      console.error('Erreur lors de la requête:', error);
      throw error;
  }
}

// Fonction pour récupérer un cookie par son nom
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

// Fonction pour extraire l'ID du lieu depuis l'URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('place_id');
}

// ----------------------- AUTHENTICATION CHECK -----------------------
function checkAuthentication() {
  const token = getCookie("token");
  console.log("Token:", token); // Vérifier si le token est bien récupéré

  const loginButton = document.getElementById("auth-button");
  const loginLink = document.getElementById("login-link");
  const addReviewSection = document.getElementById("add-review");
  const placeId = getPlaceIdFromURL();

  console.log("Login button found:", !!loginButton); // Vérifier si le bouton est trouvé

  if (!token) {
      // Non connecté
      if (loginLink) loginLink.style.display = "block";
      if (addReviewSection) addReviewSection.style.display = "none";
      if (loginButton) {
          loginButton.textContent = "Login";
          loginButton.href = "/login";
          loginButton.classList.remove("user-initial");
          // Reset des styles
          loginButton.style.borderRadius = "20px";
          loginButton.style.width = "auto";
          loginButton.style.height = "auto";
          loginButton.style.padding = "0.5rem 1rem";
      }
      // Charge quand même les lieux pour les utilisateurs non authentifiés
      if (window.location.pathname === "/") {
          fetchPlaces();
      } else if (placeId) {
          fetchPlaceDetails(null, placeId);
      }
  } else {
      // Utilisateur connecté
      if (loginLink) loginLink.style.display = "none";
      if (addReviewSection) {
          addReviewSection.style.display = "block";
          setupReviewForm(token, placeId);
      }

      // Afficher l'URL complète de la requête
      console.log("Fetching user profile from:", "http://127.0.0.1:5001/api/v1/users/profile");

      fetch("http://127.0.0.1:5001/api/v1/users/profile", {
          method: 'GET',
          headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          }
      })
      .then((response) => {
          console.log("Profile response status:", response.status);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
      })
      .then((user) => {
          console.log("User data:", user); // Vérifier les données utilisateur
          if (loginButton && user.first_name) {
              console.log("Updating button with:", user.first_name.charAt(0));
              loginButton.textContent = user.first_name.charAt(0).toUpperCase();
              loginButton.classList.add("user-initial");
              loginButton.style.borderRadius = "50%";
              loginButton.style.width = "40px";
              loginButton.style.height = "40px";
              loginButton.style.display = "flex";
              loginButton.style.alignItems = "center";
              loginButton.style.justifyContent = "center";
              loginButton.style.padding = "0";
              loginButton.href = "#"; // Empêcher la redirection vers la page de login
          }
      })
      .catch((error) => {
          console.error("Erreur lors de la récupération du profil:", error);
      })
      .finally(() => {
          // Chargement des données après la vérification du profil
          if (window.location.pathname === "/") {
              fetchPlaces(token);
          } else if (placeId) {
              fetchPlaceDetails(token, placeId);
          }
          console.log("Utilisateur authentifié");
      });
  }
}

// ----------------------- FETCH PLACES -----------------------
// Récupère la liste des lieux depuis l'API
async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Erreur lors de la récupération des lieux:', response.statusText);
        }
    } catch (error) {
        console.error('Erreur réseau:', error);
    }
}

// ----------------------- DISPLAY PLACES -----------------------
// Affiche dynamiquement la liste des lieux
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.classList.add('place-card');
        placeCard.setAttribute('data-price', place.price);
        
        if (place.amenities && place.amenities.length > 0) {
            const categories = place.amenities.map(amenity => 
                amenity.name.toLowerCase().replace(' ', '-')
            );
            placeCard.setAttribute('data-category', categories.join(' '));
        }

        placeCard.innerHTML = `
            <a href="/place?place_id=${place.id}">
                <img src="/static/images/places/default-place.jpg" 
                    alt="${place.title || place.name}" 
                    class="place-image">
                <h2>${place.title || place.name}</h2>
                <p>${place.price}€ par nuit</p>
            </a>
            <p>${place.description || ''}</p>
            <p><strong>Localisation :</strong> ${place.location || ''}</p>
            <button class="details-button" 
                    onclick="window.location.href='/place?place_id=${place.id}'">
                Voir les détails
            </button>
        `;

        placesList.appendChild(placeCard);
    });

    addPriceFilter();
    addCategoryFilter();
}

// ----------------------- PLACE DETAILS -----------------------
// Récupère et affiche les détails d'un lieu spécifique
async function fetchPlaceDetails(token, placeId) {
    if (!placeId) {
        console.error('Aucun ID de lieu fourni');
        return;
    }

    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://127.0.0.1:5001/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP! statut: ${response.status}`);
        }

        const placeData = await response.json();
        displayPlaceDetails(placeData);
    } catch (error) {
        console.error('Erreur lors de la récupération des détails:', error);
        displayError('Impossible de charger les détails du lieu');
    }
}

// Affiche les détails d'un lieu
function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;

    placeDetailsSection.innerHTML = '';

    const mainInfo = document.createElement('div');
    mainInfo.className = 'place-main-info';
    mainInfo.innerHTML = `
        <h1>${place.title}</h1>
        <div class="place-meta">
            <span class="price">${place.price}€ par nuit</span>
            ${place.owner ? `<span class="host">Hôte: ${place.owner.first_name}</span>` : ''}
        </div>
        <p class="description">${place.description || 'Aucune description disponible'}</p>
    `;
    placeDetailsSection.appendChild(mainInfo);

    if (place.amenities && place.amenities.length > 0) {
        const amenitiesSection = document.createElement('div');
        amenitiesSection.className = 'amenities-section';
        amenitiesSection.innerHTML = `
            <h2>Équipements</h2>
            <div class="amenities-grid">
                ${place.amenities.map(amenity => `
                    <div class="amenity-item">
                        <img src="/static/images/icons/${amenity.name.toLowerCase()}.png" 
                            alt="${amenity.name}" 
                            class="amenity-icon">
                        <span>${amenity.name}</span>
                    </div>
                `).join('')}
            </div>
        `;
        placeDetailsSection.appendChild(amenitiesSection);
    }

    if (place.reviews && place.reviews.length > 0) {
        const reviewsSection = document.createElement('div');
        reviewsSection.className = 'reviews-section';
        reviewsSection.innerHTML = `
            <h2>Avis (${place.reviews.length})</h2>
            <div class="reviews-container">
                ${place.reviews.map(review => `
                    <div class="review-card">
                        <div class="review-header">
                            <span class="reviewer-name">
                                ${review.author ? review.author.first_name : 'Anonyme'}
                            </span>
                            <div class="rating">
                                ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}
                            </div>
                        </div>
                        <p>${review.text}</p>
                    </div>
                `).join('')}
            </div>
        `;
        placeDetailsSection.appendChild(reviewsSection);
    }
}

// ----------------------- REVIEWS -----------------------
// Configure le formulaire d'ajout d'avis
function setupReviewForm(token, placeId) {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    const ratingInput = reviewForm.querySelector('.rating-input');
    const stars = ratingInput.querySelectorAll('span');
    let selectedRating = 0;

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            selectedRating = index + 1;
            stars.forEach((s, i) => {
                s.textContent = i < selectedRating ? '★' : '☆';
            });
        });
    });

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const reviewText = reviewForm.querySelector('textarea').value;
        if (!reviewText || selectedRating === 0) {
            alert('Veuillez fournir une note et un commentaire');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5001/api/v1/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: selectedRating,
                    place_id: placeId
                })
            });

            if (!response.ok) {
                throw new Error('Échec de l\'envoi de l\'avis');
            }

            fetchPlaceDetails(token, placeId);
            reviewForm.reset();
            selectedRating = 0;
            stars.forEach(s => s.textContent = '☆');
        } catch (error) {
            console.error('Erreur lors de l\'envoi de l\'avis:', error);
            alert('Échec de l\'envoi de l\'avis. Veuillez réessayer.');
        }
    });
}

// Fonction pour gérer la soumission du formulaire de place
async function handlePlaceSubmission(event) {
  event.preventDefault();
  
  const token = getCookie("token");
  if (!token) {
      alert("Vous devez être connecté pour ajouter un logement");
      window.location.href = '/login';
      return;
  }

  const formData = {
      title: document.getElementById('title').value,
      description: document.getElementById('description').value,
      price: parseFloat(document.getElementById('price').value),
      latitude: parseFloat(document.getElementById('latitude').value) || null,
      longitude: parseFloat(document.getElementById('longitude').value) || null,
      amenities: Array.from(document.querySelectorAll('.amenity-checkbox input:checked'))
          .map(checkbox => checkbox.value)
  };

  try {
      const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(formData)
      });

      if (response.ok) {
          alert('Logement ajouté avec succès !');
          window.location.href = '/';
      } else {
          const error = await response.json();
          alert(`Erreur: ${error.error || 'Une erreur est survenue'}`);
      }
  } catch (error) {
      console.error('Erreur lors de l\'ajout du logement:', error);
      alert('Une erreur est survenue lors de l\'ajout du logement');
  }
}

// Initialisation des écouteurs d'événements
document.addEventListener('DOMContentLoaded', () => {
  const placeForm = document.getElementById('place-form');
  if (placeForm) {
      placeForm.addEventListener('submit', handlePlaceSubmission);
      loadAmenities();  // Charger les équipements disponibles
  }
});

// Gestion de la modal
document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('add-place-modal');
  const btn = document.getElementById('add-place-button');
  const span = document.getElementsByClassName('close')[0];
  const form = document.getElementById('place-form');

  btn.onclick = function(e) {
      e.preventDefault();
      const token = getCookie('token');
      if (!token) {
          alert('Vous devez être connecté pour ajouter un logement');
          window.location.href = '/login';
          return;
      }
      modal.style.display = 'block';
  }

  span.onclick = function() {
      modal.style.display = 'none';
  }

  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = 'none';
      }
  }

  // Gestion du formulaire
  form.onsubmit = async function(e) {
      e.preventDefault();
      const token = getCookie('token');

      const formData = {
          title: document.getElementById('title').value,
          description: document.getElementById('description').value,
          price: parseFloat(document.getElementById('price').value),
          latitude: parseFloat(document.getElementById('latitude').value) || null,
          longitude: parseFloat(document.getElementById('longitude').value) || null
      };

      try {
          const response = await fetch('http://127.0.0.1:5001/api/v1/places/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify(formData)
          });

          if (response.ok) {
              alert('Logement ajouté avec succès !');
              modal.style.display = 'none';
              window.location.reload();
          } else {
              const error = await response.json();
              alert(`Erreur: ${error.error || 'Une erreur est survenue'}`);
          }
      } catch (error) {
          console.error('Erreur:', error);
          alert('Une erreur est survenue lors de l\'ajout du logement');
      }
  }
});

// ----------------------- FILTERS -----------------------
function addPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    const placeCards = document.querySelectorAll('.place-card');

    if (priceFilter) {
        const prices = [10, 50, 100, 'Tous'];
        prices.forEach((price) => {
            const option = document.createElement('option');
            option.value = price;
            option.text = price;
            priceFilter.appendChild(option);
        });

        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;

            placeCards.forEach((card) => {
                const placePrice = parseInt(card.getAttribute('data-price'), 10);

                if (selectedPrice === 'Tous' || placePrice <= parseInt(selectedPrice, 10)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

function addCategoryFilter() {
    const categoryButtons = document.querySelectorAll('.filter-button');
    const placeCards = document.querySelectorAll('.place-card');

    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            const selectedCategory = button.getAttribute('data-category');

            placeCards.forEach(card => {
                if (card.getAttribute('data-category').includes(selectedCategory)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// Fonction pour afficher les messages d'erreur
function displayError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.getElementById('place-details').prepend(errorDiv);
}

// ----------------------- INITIALIZATION -----------------------
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    checkAuthentication();

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                alert('Veuillez remplir tous les champs avant de soumettre.');
                return;
            }

            const submitButton = loginForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Connexion en cours...';

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; secure; samesite=strict`;
                    alert('Connexion réussie ! Vous allez être redirigé.');
                    window.location.href = '/';
                } else {
                    const error = await response.json();
                    alert(`Erreur: ${error.message || 'Identifiants incorrects. Veuillez réessayer.'}`);
                }
            } catch (error) {
                console.error('Une erreur est survenue lors de la connexion:', error);
                alert('Une erreur est survenue. Veuillez réessayer plus tard.');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Se connecter';
            }
        });
    }
});
