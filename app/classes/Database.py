import os
import tempfile
import pyrebase
import requests
import json
from collections import OrderedDict
from flask import current_app as flask_app
from app import SITE_ROOT

class Database():
    """ 
    Database Class. 
  
    Class to interact with Firebase Realtime Database. 
  
    """

    def __init__(self):
        """ 
        Initialise class with configuration 
    
        """
        # Load Firebase config data, including Service Account file
        firebase_config_file = os.path.join(SITE_ROOT, 'firebase.json')
        firebase_config = json.load(open(firebase_config_file))
        firebase_config["serviceAccount"] = os.path.join(SITE_ROOT, 'firebase.admin.json')
        
        # Initialize Firebase auth and database
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        # Create readable errors based on Firebase errors
        self.readable_errors = {
            "INVALID_PASSWORD": "This is an invalid password",
            "EMAIL_NOT_FOUND": "This email has not been registered",
            "EMAIL_EXISTS": "This email already exists. Try logging in instead.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts, please try again later",
            "USER_DISABLED": "This account has been disabled by an administrator.",
        }

    # Image Requests
    def get_images(self, limit=20, user_id=False):
        
        try: #trys to get images from DB
            if (user_id):
                images = self.db.child("images").order_by_child("user_id").equal_to(user_id).limit_to_first(limit).get()
            else:
                images = self.db.child("images").order_by_child("user_id").limit_to_first(limit).get()

            # Logs a braker for the cmd output
            flask_app.logger.info('####################### images val #####################')
            flask_app.logger.info(images.val())
            if isinstance(images.val(), OrderedDict): # Sends all images
                return images
            else:
                return False
            
        except Exception as err: # Handles errors to prevent crashes and passes errors back
            self.process_error(err)
    
    # Gets the images for a specific imag catagory and limits to 20 images
    def get_category_images(self, category, limit=20):
        # trys to get images
        try:
            images = self.db.child("images").order_by_child("category").equal_to(category).limit_to_first(limit).get()

            if isinstance(images.val(), OrderedDict):
                return images
            else:
                return False
            
        except Exception as err: #takes error and passes error on to error handler
            self.process_error(err)
        
    def get_image(self, image_id):
        """
        Gets specific imag acording to image id
        """
        error = None
        image = False
        
        try: # trys to get the image
            image = self.db.child("images").child(image_id).get()

        except Exception as err:
            flask_app.logger.info(err)
            error = err # Gets error and sends onwards
        
        #raises exception with error
        if error:
            raise Exception(error)
        else:
            return image.val()

    def save_image(self, image_data, image_id):
        """
        Saves any changes made to the image via the edit image page
        """
        try: #trys to save the changes
            self.db.child("images").child(image_id).set(image_data)
        except Exception as err: # Handles errors
            self.process_error(err)

    def delete_image(self, image_id):
        """
        Is used to remove image from data base if the user decided to delet the image
        """
        try: #trys to delet image
            self.db.child("images").child(image_id).remove()
        except Exception as err: #handles any errors with deleting image
            self.process_error(err)

    def remove_matching_value(self, data, value):
        """
        I have absolutly no idea howver i asume it will remove any matching values
        """
        return_data = []
        for key in data:
            if key != value:
                return_data.append(key)
        return return_data


    # User and Account Requests
    def register(self, user_data, password):
        """
        Used for the register form to put any new acounts into the database
        """
        try: #trys to add to data base
            user_auth = self.auth.create_user_with_email_and_password(user_data['email'], password)
            user_data['localId'] = user_auth['localId']
            self.db.child("users").child(user_auth['localId']).set(user_data)
            return user_auth
        except Exception as err: # handles errors with database
            self.process_error(err)

    def login(self, email, password):
        """
        Used for login form to acsess DB
        """
        try: #trys to acsess DB
            user_auth = self.auth.sign_in_with_email_and_password(email, password)
            user = self.db.child("users").child(user_auth['localId']).get().val()
            return user
        except Exception as err: #gives error if DB is inacsessable
            self.process_error(err)

    def update_user(self, user_data):
        """
        Used to make changes to a users acount 
        """
        try: #trys to acsess DB
            self.db.child("users").child(user_data['localId']).update(user_data)
            return
        except Exception as err: #returns error if there is error with DB
            self.process_error(err)
 
    def process_error(self, error):
        """
        Is callled in all of the other try excepts in the functions above
        This takes the error up to the flask app so it can be displayed in the console
        """
        flask_app.logger.info(error)
        readable_error = self.get_readable_error(error)
        raise Exception(readable_error)

    def get_readable_error(self, error):
        """
        Gives a specific readable message to the function above to be sent to flask
        """
        error_json = error.args[1]
        error_messsage = json.loads(error_json)['error']['message']
        if error_messsage in self.readable_errors.keys(): 
            return self.readable_errors[error_messsage]
        else: 
            return "There was a problem with your request."