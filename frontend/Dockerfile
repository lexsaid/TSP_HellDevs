# Usamos la imagen oficial de Nginx ligera
FROM nginx:alpine

# 1. Eliminamos el archivo de configuración que trae Nginx por defecto
RUN rm /etc/nginx/conf.d/default.conf

# 2. Copiamos tu archivo nginx.conf personalizado hacia donde Nginx lo va a leer
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 3. Copiamos todos tus archivos (css, html, js) a la carpeta pública de Nginx
COPY . /usr/share/nginx/html

# Exponemos el puerto 80 (aunque ya lo hace la imagen base, es buena práctica)
EXPOSE 80

# Arrancamos Nginx
CMD ["nginx", "-g", "daemon off;"]