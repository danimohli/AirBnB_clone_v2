#!/usr/bin/env bash
# Install Nginx if not already installed

if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared /data/web_static/current

# Create a fake HTML file for testing
sudo echo "<html>
  <head>
  </head>
  <body>
    <p>Test HTML file for Nginx configuration setup.</p>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link /data/web_static/current if it exists
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current
config="server {
    listen 80;
    listen [::]:80;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
        internal;
    }
}"

# Remove default configuration and replace with new configuration
sudo rm -f /etc/nginx/sites-enabled/default
sudo echo "$config" | sudo tee /etc/nginx/sites-available/web_static
sudo ln -sf /etc/nginx/sites-available/web_static /etc/nginx/sites-enabled/

# Restart Nginx to apply changes
sudo service nginx restart

# Exit successfully
exit 0
