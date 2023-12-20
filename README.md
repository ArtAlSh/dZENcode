## Setup app
```
git clone https://github.com/ArtAlSh/dZENcode.git
cd ./dZENcode/backend
cp .env.sample .env
```
> Fill out the fields ***EMAIL_HOST_USER*** and ***EMAIL_HOST_PASSWORD*** <br>
> [!IMPORTANT]
> EMAIL_HOST_USER must be Gmail. <br>
> EMAIL_HOST_PASSWORD must be an app password https://myaccount.google.com/apppasswords (require 2FA)

## Run server
```
cd ..   # to the 'dZENcode' folder
docker-compose up --build
```
## Open site
```http://localhost:8080/```
