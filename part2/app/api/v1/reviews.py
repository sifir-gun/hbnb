from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Création du namespace pour les opérations sur les avis (reviews)
api = Namespace('reviews', description='Review operations')

# Définition du modèle de données d'une review pour la validation et la documentation des entrées
review_model = api.model('Review', {
    # Le texte de l'avis
    'text': fields.String(required=True, description='Text of the review'),
    # La note de l'avis (1-5)
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    # L'ID de l'utilisateur ayant rédigé l'avis
    'user_id': fields.String(required=True, description='ID of the user'),
    # L'ID du lieu associé à l'avis
    'place_id': fields.String(required=True, description='ID of the place')
})

# Initialisation de la façade HBnB pour gérer la logique métier
facade = HBnBFacade()


@api.route('/')
class ReviewList(Resource):
    """
    Ressource pour gérer la liste des avis.
    Permet de créer un nouvel avis (POST) ou de récupérer tous les avis (GET).
    """

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Créer un nouvel avis.
        
        Cette méthode utilise les données de l'avis fournies dans la requête pour créer un nouvel avis. 
        Retourne l'avis créé avec un statut HTTP 201 en cas de succès ou une erreur 400 si les données sont invalides.
        """
        review_data = api.payload  # Récupère les données JSON de la requête
        # Appelle la façade pour créer l'avis
        review, error = facade.create_review(review_data)
        if error:
            # Retourne une erreur en cas de problème
            return {'error': error}, 400
        # Retourne les détails de l'avis créé avec un code HTTP 201
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Récupérer la liste de tous les avis.
        
        Retourne une liste d'avis avec le statut HTTP 200.
        """
        reviews = facade.get_all_reviews()  # Appelle la façade pour récupérer tous les avis
        # Formate les avis pour la réponse
        review_list = [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in reviews
        ]
        return review_list, 200  # Retourne la liste d'avis avec un code HTTP 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Ressource pour gérer un avis spécifique par son ID.
    Permet de récupérer (GET), mettre à jour (PUT), ou supprimer (DELETE) un avis.
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Récupérer les détails d'un avis par ID.
        
        Retourne les détails de l'avis avec le statut HTTP 200 ou une erreur 404 si l'avis n'existe pas.
        """
        review = facade.get_review(
            review_id)  # Récupère l'avis depuis la façade
        if not review:
            # Retourne une erreur si l'avis n'existe pas
            return {'error': 'Review not found'}, 404
        # Retourne les détails de l'avis avec un code HTTP 200
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """
        Mettre à jour les informations d'un avis.
        
        Reçoit des données JSON pour mettre à jour l'avis et retourne l'avis mis à jour avec un code HTTP 200.
        Retourne une erreur 400 si les données sont invalides ou une erreur 404 si l'avis n'est pas trouvé.
        """
        review_data = api.payload  # Récupère les nouvelles données de l'avis
        # Met à jour l'avis via la façade
        review = facade.update_review(review_id, review_data)
        if not review:
            # Retourne une erreur si l'avis n'existe pas
            return {'error': 'Review not found'}, 404
        # Retourne les détails de l'avis mis à jour avec un code HTTP 200
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Supprimer un avis par son ID.
        
        Retourne un message de confirmation avec un statut HTTP 200 si la suppression est réussie ou une erreur 404 si l'avis n'existe pas.
        """
        success = facade.delete_review(
            review_id)  # Supprime l'avis via la façade
        if not success:
            # Retourne une erreur si l'avis n'existe pas
            return {'error': 'Review not found'}, 404
        # Retourne un message de succès avec un code HTTP 200
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Ressource pour gérer les avis associés à un lieu spécifique.
    Permet de récupérer tous les avis pour un lieu donné par son ID.
    """

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Récupérer tous les avis associés à un lieu spécifique.
        
        Retourne une liste d'avis pour le lieu spécifié avec le statut HTTP 200 ou une erreur 404 si le lieu n'existe pas.
        """
        # Vérifie si le lieu existe via la façade
        place = facade.place_repo.get(place_id)
        if not place:
            # Retourne une erreur si le lieu n'existe pas
            return {'error': 'Place not found'}, 404

        # Récupère tous les avis associés à ce lieu
        reviews = facade.get_reviews_by_place(place_id)
        # Formate les avis pour la réponse
        review_list = [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            } for review in reviews
        ]
        return review_list, 200  # Retourne la liste d'avis avec un code HTTP 200
