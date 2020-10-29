from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session, flash
from flask import current_app as flask_app

class Account():

    def __init__(self):
        self.user = User()
        return None

    def register(self, request):
        """ 
        Registration method. 
    
        Processes POST request, and registers user in Firebase on success

        Parameters: 
            request (obj): The POST request object
    
        Raises: 
            error (Exception): Error from failed Firebase request
    
        """

        # Extract required fields from POST request
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Validates required registration fields
        error = None
        if not email:
            error = 'An email is required.'
        elif not password:
            error = 'Password is required.'
        elif 6 > len(password):
            error = 'Your password must be at least 6 characters long.'
        elif not password_confirm:
            error = 'Password confirmation is required.'
        elif password != password_confirm:
            error = 'Password and password confirmation should match.'
        else:
            try:
                user_data = {
                    "localId": "",
                    "email": email,
                    "first_name": "",
                    "last_name": "",
                    "avatar": ""
                }
                # Attempt to process valid registration request
                database = Database()
                user_auth = database.register(user_data, password)
            except Exception as err:
                # Raise error from failed Firebase request
                error = err
        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            # Return on success
            return
        
    def login(self, request):
        """
        This takes the login form infomation fromthe view and gives it to the controller to be taken into the DB
        """
        if request.method == 'POST': #checks for request
            #makes sure there is enough data in request
            email = request.form['email']
            password = request.form['password']

            error = None
            #Gives error if there is any missign data
            if not email:
                error = 'An email is required.'
            elif not password:
                error = 'Password is required.'
            else:
                #runs if all the daata is avaliable
                try: #trys to give data to database
                    database = Database()
                    user = database.login(email, password)
                    # TODO Remove for production
                    #flask_app.logger.info(user)
                    self.user.set_user(user)
                except Exception as err: #gives errors if there is error with databse
                    error = err

        if error: #gives any errors to flask if there are any errors anywhere above
            raise Exception(error)
        else:
            return
        
    def update(self, request):
        """
        Used to update the users acount
        """
        if request.method == 'POST': # runns if there is a form entry
            #checks to make sure all data is in the form
            first_name = request.form['firstname']
            last_name = request.form['lastname']

            error = None
            #gives errors if any data is missing
            if not first_name:
                error = 'A first name is required.'
            elif not last_name:
                error = 'A last name is required.'
            else:
                #if all data is corect it trys to send data to database
                
                if 'avatar' in request.files: #first checks for a avatar change because this requres the uploader
                    file = request.files['avatar']
                    if file.filename: #usese the uploader to upload the image found in app/classes/Upload.py
                        uploader = Upload()
                        avatar = uploader.upload(file, session['user']['localId'])
                        session['user']['avatar'] = "/" + avatar.strip("/")
                try: #trys to give data to DB
                    session['user']['first_name'] = first_name
                    session['user']['last_name'] = last_name
                    database = Database()
                    user_auth = database.update_user(session['user'])
                    session.modified = True
                except Exception as err: #gives any errors if there is one while trying to acsess database
                    error = err

        if error: # handles the error if there is one above
            raise Exception(error)
        else:
            return
        
    def like(self, image_id, like, request):
        """
        This calss handles likes and sends them on to the data base if an image has been liked or unliked
        """
        changed = False
        likes = session['user']['likes']

        if like == 'true': #checks if image has been liked
            if image_id not in likes:
                likes.append(image_id)
                changed = True
        else: # Checks if image has been unliked
            if image_id in likes:
                likes.remove(image_id)
                changed = True

        if changed: # If the image has been liked or unliked it updates the database
            session['user']['likes'] = likes
            database = Database()
            database.update_user(session['user'])
            session.modified = True

        return changed #returns weather the database was changed or not
        
    def logout(self):
        """
        Logs the user out
        """
        self.user.unset_user()

