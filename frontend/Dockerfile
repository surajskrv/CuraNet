# ---------- Build Stage ----------
FROM node:18-alpine AS build

WORKDIR /app

# Copy dependency files
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build Vue app
RUN npm run build

# ---------- Production Stage ----------
FROM nginx:stable-alpine

# Copy built files to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose nginx port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
