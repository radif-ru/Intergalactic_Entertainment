FROM nginx:1.21.4-alpine

#COPY . /var/www/
RUN rm /etc/nginx/conf.d/default.conf
#COPY ./etc/nginx/sites-available /etc/nginx/sites-available
#COPY ./etc/nginx/sites-enabled /etc/nginx/sites-enabled
COPY ./nginx.conf /etc/nginx/nginx.conf
#COPY ./etc/letsencrypt /etc/letsencrypt
