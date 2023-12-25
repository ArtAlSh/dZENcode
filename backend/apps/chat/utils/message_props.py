import re
import base64
from io import BytesIO
from math import floor
from django.core.files import File
from django.contrib.auth.models import User
from django.db.models import Q
from PIL import Image
from .exceptions import MessageException


class HandleUser:
    username_pattern = re.compile(r"^[a-zA-Z0-9_\-]{4,15}$")
    email_pattern = re.compile(r".+@\w+\.+\w{2}")

    def __get__(self, instance, owner):
        if user := instance._user:
            return user

        username = instance.data.get("username")
        email = instance.data.get("email")

        self.check_username(username)
        self.check_email(email)

        users = User.objects.filter(Q(email=email) | Q(username=username))
        is_username_exist = False
        for user in users:
            if user.email == email:
                instance._user = user
                return user
            elif user.username == username and user.email != email:
                is_username_exist = True

        if is_username_exist:
            raise MessageException("Username already exist.")

        # user = User.objects.create_user(username=username, email=email)
        instance._user = None
        return user

    def __set__(self, instance, value):
        if (type(value) is User) or (type(value) is None):
            instance._user = value

    def check_username(self, username):
        if not username:
            raise MessageException("Username is empty.")
        if not bool(self.username_pattern.match(username)):
            raise MessageException("Username must be 5-15 characters long. Only symbols are allowed: A-Z, a-z, 0-9, _, -.")
        return True

    def check_email(self, email):
        if not email:
            raise MessageException("Email is empty.")
        if not bool(self.email_pattern.match(email)):
            raise MessageException("Wrong email.")


class HandleHomePage:
    homepage_pattern = re.compile(r"http[s]?:\/\/[a-z0-9_\-.]+\.[a-z0-9_\-\/]+")

    def __get__(self, instance, owner):
        homepage = instance.data.get("homepage")
        if homepage:
            if not bool(self.homepage_pattern.match(homepage)):
                raise MessageException("Wrong home page URL.")
        return homepage


class HandleMessage:
    forbidden_tags_pattern = re.compile(r"<(?!\/?code|\/?b|\/?a|\/?i)\s?.*?>")
    close_tags_pattern = re.compile(r"<(?P<tag>.+)\s?[^>^<]*>[^>^<]*<\/(?P=tag)>")
    check_tag_pattern = re.compile(r"<.*?>")

    def __get__(self, instance, owner):
        message = instance.data.get("message")
        if not message:
            raise MessageException("Message is empty.")
        self.check_forbidden_tags(message)
        self.check_close_tags(message)

        return message

    def check_forbidden_tags(self, message):
        text = message.replace("<br>", "")
        if self.forbidden_tags_pattern.search(text):
            raise MessageException("Allowed only tags: <a>, <b>, <i>, <code>.")

    def check_close_tags(self, message: str):
        text = message.replace("<br>", "")
        while self.close_tags_pattern.search(text):
            text = self.close_tags_pattern.sub("", text)

        if self.check_tag_pattern.search(text):
            raise MessageException("There are unclosed tags.")


class HandleFile:
    allowed_formats = ["txt"]
    max_size = 100_000     # bites

    def __get__(self, instance, owner):
        if instance._file:
            return instance._file

        file_name = instance.data.get("file_name")
        file_data = instance.data.get("file_data")

        if not file_name or not file_data:
            return None

        data = file_data.split(",")[-1]
        data = base64.b64decode(data)
        file_io = BytesIO(data)
        file = File(file_io, file_name)

        self.check_file(file)

        instance._file = file
        return file

    def check_file(self, file: File):
        if file.name.split(".")[-1] not in self.allowed_formats:
            raise MessageException(f"Forbidden file format. Allowed formats: {', '.join(self.allowed_formats)}")

        if file.size > self.max_size:
            raise MessageException(f"Max file size is {self.max_size} bites.")


class HandleImage:
    allowed_formats = ["jpg", "gif", "png"]
    max_width = 320
    max_height = 240

    def __get__(self, instance, owner):
        if instance._image:
            return instance._image

        image_name = instance.data.get("image_name")
        image_data = instance.data.get("image_data")

        if not image_name or not image_data:
            return None

        data = image_data.split(",")[-1]
        data = base64.b64decode(data)
        file_io = BytesIO(data)

        with Image.open(file_io, mode="r") as img:
            img: Image.Image
            if img.format.lower() not in self.allowed_formats:
                raise MessageException(f"Wrong image format. Allowed formats: {', '.join(self.allowed_formats)}")

            if img.height > self.max_height or img.width > self.max_width:
                new_size = self.get_new_size(img.width, img.height)
                r_img = img.resize(size=(new_size["width"], new_size["height"]))

                mod_file_io = BytesIO()
                r_img.save(mod_file_io, format=img.format)
                file_io = mod_file_io

                r_img.close()

        file = File(file_io, image_name)
        instance._image = file
        return file

    def get_new_size(self, width, height):
        if width / height > self.max_width / self.max_height:
            return {"width": self.max_width, "height": floor(height / width * self.max_width)}
        else:
            return {"width": floor(width / height * self.max_height), "height": self.max_height}
