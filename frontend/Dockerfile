FROM node:16-buster

WORKDIR /app
COPY . .

RUN npm install -g http-server && \
    npm install && \
    npm run build

CMD http-server dist -a 0.0.0.0 -p 8080
EXPOSE 8080
