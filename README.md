# Image Management API

It is a Rest API for uploading an Image onto the server with lossless compression. You need to pass a access-token in order to 
upload file.

## API LIST

Authentication
```
1. auth/user/signup - POST
2. auth/user/signin - POST -- To Create Access Token
3. user/uploads - GET
```

Upload
```
1. service/image - POST, GET
2. service/image/{{upload_id}} - POST, GET
3. service/image?file=filename - GET
```

## Management Command
You can also register yourself and generate access key from command line
```
python manage.py generateToken
```

## Installation Of Project

1. clone repository first
2. create a env.py file
  ```
  HOST = 'localhost'
  DEBUG = True
  ```
  ```
  If your host is localhost, then let the host be same or change the host. It you want to run on production, set DEBUG = False.
  ```
3. pip install -r requirement.txt

## Running Migration
```
python manage.py makemigrations service
python manage migrate
```
