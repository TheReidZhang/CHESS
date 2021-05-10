FROM node:15.14.0-alpine3.13
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV BACKEND_PROXY "http://backend:5000"
RUN npm run build
EXPOSE 3000
CMD ["node", "server.js"]