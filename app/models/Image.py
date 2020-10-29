from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app
import uuid, time

class Image():

    def __init__(self):
        '''
        Empty init
        '''
        return None

    def get_images(self, limit=20):
        '''
        Uses the database class to colect all the images
        '''
        error = None
        images = False

        try: #trys to acsess database
            database = Database()
            images = database.get_images(limit)

        except Exception as err: #gives error if DB unavaliable
            flask_app.logger.info(err)
            error = err

        if error: # passes error to flask
            raise Exception(error)
        else:
            return images

    def get_category_images(self, category, limit=20):
        '''
        Gets images for a specific catagory
        '''
        error = None
        images = False
        
        try: # trys to acsess database
            database = Database()
            images = database.get_category_images(category, limit)

        except Exception as err: #gets error if DB unavaliable
            flask_app.logger.info(err)
            error = err

        if error: # passes error to flask
            raise Exception(error)
        else:
            return images

    def get_image(self, image_id):
        '''
        Gets an individual image 
        '''
        error = None
        image = False
        
        try: #trys to get data from DB
            database = Database()
            image = database.get_image(image_id)

        except Exception as err: #gives error if DB unabaliable
            flask_app.logger.info(err)
            error = err

        if error: #hands error to flask
            raise Exception(error)
        else:
            return image #returns image if there arnt any isues

    def delete_image(self, image_id):
        '''
        This function handles images being deleted and consults DB
        '''
        error = None
        
        try: # trys to acsess DB
            database = Database()
            database.delete_image(image_id)

        except Exception as err: #takes any errors from DB
            flask_app.logger.info(err)
            error = err

        if error: #gives any erors to flask
            raise Exception(error)
        else: 
            return

    def get_user_images(self, limit=20):
        '''
        Gets the images from a specific user
        '''
        error = None
        images = False
        user_id = False
        if (session['user'] and session['user']['localId']): #gets the user
            user_id = session['user']['localId']
        try: #trys to get to DB
            database = Database()
            images = database.get_images(limit, user_id)

        except Exception as err: #handles errors with DB
            flask_app.logger.info(err)
            error = err

        if error: #passes errors to flask
            raise Exception(error)
        else:
            return images

    def upload(self, request):
        '''
        Handles sending a image upload to the DB
        '''
        image_id        = str(uuid.uuid1())
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']

        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']): #makes sure the user is logged in
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            error = 'You must be logged in to upload an image.'

        if 'image' not in request.files: #makes sure there is a file
            error = 'A file is required.'
        else:
            file = request.files['image']

        if not error:
            if file.filename == '': #teh following make sure that all of the infomation for teh form is there
                error = 'A file is required.'
            elif not name:
                error = 'An name is required.'
            elif not description:
                error = 'A description is required.'
            elif not category:
                error = 'A category is required.'
            else: #if all the infomation is there is trys to send data to DB
                try:
                    uploader = Upload()
                    upload_location = uploader.upload(file, image_id)
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      '/' + upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           int(time.time())
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err: #if theres a DB error
                    error = err
        if error: # logs errors to flask if there are any at some point during upload
            flask_app.logger.info('################ UPLOAD ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            return image_id

    def update(self, image_id, request):
        '''
        Updates infoamtion of an image (description, name, catagorie)
        '''
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']
        created_at      = request.form['created_at'] 
        upload_location = request.form['upload_location']  

        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']): # makes sure teh user is logged in
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            error = 'You must be logged in to update an image.'

        if not error: #makes sure all the form data is there
            if not name:
                error = 'An name is required.'
            elif not description:
                error = 'A description is required.'
            elif not category:
                error = 'A category is required.'
            else: # if all the form data is there try to acsess DB
                try:
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           created_at
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err: #handle DB errors
                    error = err
        if error: #if there is an error at any point hand it on to flask
            flask_app.logger.info('################ UPDATE ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else: #continue if there arnt any errors
            return