import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app as flask_app
from app import SITE_ROOT

class Upload():
    """
    Takes the image and saves it into the website file system so it can be displayed
    """
    def __init__(self):
        # initulisation and sets suported file types
        self.extensions = {'png', 'jpg', 'jpeg', 'gif'}

    def upload(self, file, filename):
        """
        Makes sure file is the right type of file and then saves it to the os
        """
        allowed_extension = self.allowed_file(file.filename)
        if allowed_extension:
            fullname = filename + '.' + allowed_extension
            destination = os.path.join('static/uploads', fullname)
            file.save(os.path.join(SITE_ROOT, destination)) #this line specifically saves to the OS using the os library
            return destination
        else: # handles errors if the filetype isnt correct
            raise Exception("Only allowed filetypes: ".join(self.extensions.values()))

    def allowed_file(self, filename): #specifically runs through the file types and makes sure they are readable
        if ('.' in filename and filename.rsplit('.', 1)[1].lower() in self.extensions):
            return filename.rsplit('.', 1)[1].lower()
        return False