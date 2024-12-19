from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade
from app.models.place import Place
from app.models import storage
import os
from werkzeug.utils import secure_filename
from app import allowed_file

api = Namespace('places', description="Operations related to places")

place_model = api.model('Place', {
    'title': fields.String(
        required=True, description='Title', example="Macao"
    ),
    'description': fields.String(
        description='Description', example="very good"
    ),
    'price': fields.Float(
        required=True, description='Price per night', example=120.23
    ),
    'latitude': fields.Float(
        required=True, description='Latitude', example=33.33
    ),
    'longitude': fields.Float(
        required=True, description='Longitude', example=44.44
    ),
    'amenities': fields.List(
        fields.String, description="Amenities IDs", example=["BBQ"]
    )
})

facade = HBnBFacade()


@api.route('/')
class PlaceList(Resource):
    @api.doc('get_places')
    @api.response(200, 'Success')
    @api.response(404, 'Not found')
    def get(self):
        try:
            places = storage.get_all(Place)
            if not places:
                return {"message": "No places found"}, 404
            return [
                place.to_dict() for place in places if isinstance(place, Place)
            ], 200
        except Exception as e:
            return {"error": str(e)}, 500

    @api.doc('create_place')
    @jwt_required()
    @api.response(201, 'Created')
    @api.response(400, 'Bad request')
    @api.response(401, 'Unauthorized')
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            form_data = request.form
            files = request.files.getlist('photos')

            # Validate required fields
            title = form_data.get('title')
            description = form_data.get('description')

            # Validate and convert numeric fields
            try:
                price = float(form_data.get('price', 0))
                latitude = float(form_data.get('latitude', 0))
                longitude = float(form_data.get('longitude', 0))
            except (ValueError, TypeError):
                return {
                    'error': (
                        'Prix, lati et longi doivent être des nombres valides'
                    )
                }, 400

            if not all([title, description, price > 0]):
                return {
                    'error': 'Titre, description et un prix < à 0 sont requis'
                }, 400

            place_data = {
                'title': title,
                'description': description,
                'price': price,
                'latitude': latitude,
                'longitude': longitude,
                'owner_id': current_user_id,
                'photos': [],
                'amenities': form_data.getlist('amenities')
            }

            # Handle file uploads
            if files:
                uploads_dir = current_app.config['UPLOAD_FOLDER']
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)

                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(uploads_dir, filename)
                        file.save(filepath)
                        place_data['photos'].append(f'uploads/{filename}')

            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<string:place_id>')
@api.param('place_id', 'Place identifier')
class PlaceDetail(Resource):
    @api.doc('get_place')
    @api.response(200, 'Success')
    @api.response(404, 'Not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.doc('update_place')
    @jwt_required()
    @api.response(200, 'Success')
    @api.response(400, 'Bad request')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    def put(self, place_id):
        try:
            current_user = get_jwt_identity()
            place = facade.get_place(place_id)

            if not place:
                return {"error": "Place not found"}, 404
            if place.owner_id != current_user['id']:
                return {"error": "Unauthorized"}, 403

            form_data = request.form
            files = request.files.getlist('photos')

            # Validate and convert numeric fields
            try:
                price = float(form_data.get('price', place.price))
                latitude = float(form_data.get('latitude', place.latitude))
                longitude = float(form_data.get('longitude', place.longitude))
            except (ValueError, TypeError):
                return {
                    'error': (
                        'Prix, lati et longi doivent être des nombres valides'
                    )
                }, 400

            place_data = {
                'title': form_data.get('title', place.title),
                'description': form_data.get('description', place.description),
                'price': price,
                'latitude': latitude,
                'longitude': longitude,
                'photos': place.photos[:],  # Keep existing photos
                'amenities': form_data.getlist('amenities', place.amenities)
            }

            # Handle new photos
            if files:
                uploads_dir = current_app.config['UPLOAD_FOLDER']
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(uploads_dir, filename)
                        file.save(filepath)
                        place_data['photos'].append(f'uploads/{filename}')

            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.doc('delete_place')
    @jwt_required()
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not found')
    def delete(self, place_id):
        try:
            current_user = get_jwt_identity()
            place = facade.get_place(place_id)

            if not place:
                return {"error": "Place not found"}, 404
            if place.owner_id != current_user['id']:
                return {"error": "Unauthorized"}, 403

            # Delete associated photos
            for photo_path in place.photos:
                try:
                    full_path = os.path.join(
                        current_app.static_folder, photo_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                except Exception as e:
                    print(f"Error deleting photo {photo_path}: {str(e)}")

            facade.delete_place(place_id)
            return {"message": "Place deleted successfully"}, 200

        except Exception as e:
            return {"error": str(e)}, 400
