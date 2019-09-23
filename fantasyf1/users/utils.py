import os
import secrets
import requests
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from fantasyf1 import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pictures", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)

    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password reset for fantasyf1",
        sender="noreply@fantasyf1.com",
        recipients=[user.email],
        body=f""" To reset your password, visit the following link:
                {url_for('users.reset_token', token=token, _external=True)}

                If you did not request a password change, simply ignore this message.
                """,
    )
    mail.send(msg)


def get_driver_list():
    headers = {"Content-Type": "application/json"}
    request = requests.post('https://safe-bayou-28242.herokuapp.com/graphql/', json={'query': '{driverstandings {driverId {forename surname}}}'}, headers=headers)
    if request.status_code == 200:
        data = request.json()
        driver_list = [[" ".join([driver['driverId']['forename'],driver['driverId']['surname']]), " ".join([driver['driverId']['forename'],driver['driverId']['surname']])] for driver in data['data']['driverstandings']]
        return sorted(driver_list, key= lambda x: x[0])
    else:
        raise Exception("Query failed to run by returning code of {}".format(request.status_code))


def get_constructor_list():
    headers = {"Content-Type": "application/json"}
    request = requests.post('https://safe-bayou-28242.herokuapp.com/graphql/', json={'query': '{constructorstandings {constructorId {name}}}'}, headers=headers)
    if request.status_code == 200:
        data = request.json()
        constructor_list = [[constructor['constructorId']['name'], constructor['constructorId']['name']] for constructor in data['data']['constructorstandings']]
        return sorted(constructor_list, key=lambda x: x[0])
    else:
        raise Exception("Query failed to run by returning code of {}".format(request.status_code))