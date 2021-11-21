# Homework #7 for Highload:Projector

NGINX with caching static files config. 

On command PURGE cache item will be removed.


Done with Lua script https://scene-si.org/2016/11/02/purging-cached-items-from-nginx-with-lua/

using md5 library https://github.com/kikito/md5.lua

## Installation

Building the NGINX with Lua conatinar 
```
git clone https://github.com/nginxinc/docker-nginx.git
cd docker-nginx/modules
docker build --build-arg ENABLED_MODULES="ndk lua" -t my-nginx-with-lua .
```

Building server containers
```
git clone https://github.com/god-of-north/highload-homework-7.git
cd highload-homework-7
docker-compose build
```

## Running caching tests

Running the containers
```
docker-compose up -d
```

Getting files
```
> curl -D - -X GET http://localhost:1337/test/hello.jpg

HTTP/1.1 200 OK
Server: nginx/1.21.4
Date: Thu, 18 Nov 2021 07:49:00 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 626
Connection: keep-alive
Last-Modified: Wed, 17 Nov 2021 19:21:24 GMT
Cache-Control: public, max-age=43200
Expires: Thu, 18 Nov 2021 19:49:00 GMT
ETag: "1637176884.2470965-626-304746084"
X-Cache-Status: MISS

██╗  ██╗███████╗██╗     ██╗      ██████╗
██║  ██║██╔════╝██║     ██║     ██╔═══██╗
███████║█████╗  ██║     ██║     ██║   ██║
██╔══██║██╔══╝  ██║     ██║     ██║   ██║
██║  ██║███████╗███████╗███████╗╚██████╔╝
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝

>curl -D - -X GET http://localhost:1337/test/world.jpg

HTTP/1.1 200 OK
Server: nginx/1.21.4
Date: Thu, 18 Nov 2021 07:49:10 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 680
Connection: keep-alive
Last-Modified: Wed, 17 Nov 2021 19:21:53 GMT
Cache-Control: public, max-age=43200
Expires: Thu, 18 Nov 2021 19:49:10 GMT
ETag: "1637176913.2618897-680-317984376"
X-Cache-Status: MISS

██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝

```

Checking is it cached by header flag
```
>curl -D - -X GET http://localhost:1337/test/hello.jpg

HTTP/1.1 200 OK
Server: nginx/1.21.4
Date: Thu, 18 Nov 2021 07:51:19 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 626
Connection: keep-alive
Last-Modified: Wed, 17 Nov 2021 19:21:24 GMT
Cache-Control: public, max-age=43200
Expires: Thu, 18 Nov 2021 19:49:00 GMT
ETag: "1637176884.2470965-626-304746084"
X-Cache-Status: HIT

██╗  ██╗███████╗██╗     ██╗      ██████╗
██║  ██║██╔════╝██║     ██║     ██╔═══██╗
███████║█████╗  ██║     ██║     ██║   ██║
██╔══██║██╔══╝  ██║     ██║     ██║   ██║
██║  ██║███████╗███████╗███████╗╚██████╔╝
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝
```

Reset the cache item for **hello.txt**
```
curl -D - -X PURGE http://localhost:1337/test/hello.jpg
```

Getting files to check caching flags
```
>curl -D - -X GET http://localhost:1337/test/hello.jpg

HTTP/1.1 200 OK
Server: nginx/1.21.4
Date: Thu, 18 Nov 2021 07:53:32 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 626
Connection: keep-alive
Last-Modified: Wed, 17 Nov 2021 19:21:24 GMT
Cache-Control: public, max-age=43200
Expires: Thu, 18 Nov 2021 19:53:32 GMT
ETag: "1637176884.2470965-626-304746084"
X-Cache-Status: MISS

██╗  ██╗███████╗██╗     ██╗      ██████╗
██║  ██║██╔════╝██║     ██║     ██╔═══██╗
███████║█████╗  ██║     ██║     ██║   ██║
██╔══██║██╔══╝  ██║     ██║     ██║   ██║
██║  ██║███████╗███████╗███████╗╚██████╔╝
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝

>curl -D - -X GET http://localhost:1337/test/world.jpg

HTTP/1.1 200 OK
Server: nginx/1.21.4
Date: Thu, 18 Nov 2021 07:53:35 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 680
Connection: keep-alive
Last-Modified: Wed, 17 Nov 2021 19:21:53 GMT
Cache-Control: public, max-age=43200
Expires: Thu, 18 Nov 2021 19:49:10 GMT
ETag: "1637176913.2618897-680-317984376"
X-Cache-Status: HIT

██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝
```


Files that do not mach the image extension filter will not be cached.
```
>curl -D - -X GET http://localhost:1337/test/planet.txt

HTTP/1.1 200 OK
Server: nginx/1.21.4
Date: Sun, 21 Nov 2021 18:32:33 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 1008
Connection: keep-alive
Last-Modified: Wed, 17 Nov 2021 19:23:54 GMT
Cache-Control: public, max-age=43200
Expires: Mon, 22 Nov 2021 06:32:33 GMT
ETag: "1637177034.7351947-1008-558698196"

              _-o#&&*''''?d:>b\_
          _o/"`''  '',, dMF9MMMMMHo_
       .o&#'        `"MbHMMMMMMMMMMMHo.
     .o"" '         vodM*$&&HMMMMMMMMMM?.
    ,'              $M&ood,~'`(&##MMMMMMH\
   /               ,MMMMMMM#b?#bobMMMMHMMML
  &              ?MMMMMMMMMMMMMMMMM7MMM$R*Hk
 ?$.            :MMMMMMMMMMMMMMMMMMM/HMMM|`*L
|               |MMMMMMMMMMMMMMMMMMMMbMH'   T,
$H#:            `*MMMMMMMMMMMMMMMMMMMMb#}'  `?
]MMH#             ""*""""*#MMMMMMMMMMMMM'    -
MMMMMb_                   |MMMMMMMMMMMP'     :
HMMMMMMMHo                 `MMMMMMMMMT       .
?MMMMMMMMP                  9MMMMMMMM}       -
-?MMMMMMM                  |MMMMMMMMM?,d-    '
 :|MMMMMM-                 `MMMMMMMT .M|.   :
  .9MMM[                    &MMMMM*' `'    .
   :9MMk                    `MMM#"        -
     &M}                     `          .-
      `&.                             .
        `~,   .                     ./
            . _                  .-
              '`--._,dd###pp=""'
```
