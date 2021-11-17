FROM my-nginx-with-lua

# RUN apt-get update && apt-get upgrade
# RUN apt-get install lua-md5 
# RUN apt-get install lua-md5-dev

RUN mkdir /lua
COPY purge.lua /lua/
# COPY md5.lua /lua/

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
