# Applause

A clap-based analytics system

### Track audience approval

Users can clap for an article to indicate approval, if they found it useful or interesting.

### Gain invaluable user behavior insights

Applause will tell you where your users are coming from, and how long they spend reading your content.

# For developers

## Database initialization, migration, and upgrade

Initialize the database:

```
flask db init
```

Migrate the database:

```
flask db migrate
```

Upgrade the database and apply the changes from a migration:

```
flask db upgrade
```

## Example nginx reverse proxy configuration

This app uses the connecting client's IP address to track information about claps and page views. Therefore, if you are using a reverse proxy, you must configure the proxy to forward headers with the appropriate remote address information. 

```
server {
  listen 80;
  server_name myapplauseserver.com;
  return 301  https://$server_name$request_uri? permanent;
}

server {
  listen 443 ssl;
  server_name myapplauseserver.com;
  ssl_certificate /etc/nginx/ssl/myapplauseserver.com.crt;
  ssl_certificate_key /etc/nginx/ssl/myapplauseserver.com.key;

  location / {
    proxy_set_header  X-Forwarded-For $remote_addr;
    proxy_pass        http://127.0.0.1:1234;
  }
}
```
