# Installation Guide for Website Deployment on Ubuntu 22.04 LTS

This guide provides step-by-step instructions for deploying this website on a clean Ubuntu 22.04 LTS installation, including setting up autostart capabilities.

## 1. Initial System Setup
```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv nginx supervisor
```

## 2. Create Project Directory and Setup
```bash
# Create project directory
sudo mkdir -p /var/www/mywebsite
cd /var/www/mywebsite

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
```

## 3. Deploy Website Files
```bash
# Copy all your website files to /var/www/mywebsite/
# You can use scp, git clone, or any other method
# Here's an example structure of how files should be organized:
/var/www/mywebsite/
├── venv/
├── app.py
├── wsgi.py
├── requirements.txt
├── static/
│   ├── script.js
│   └── styles.css
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── services.html
│   ├── booking.html
│   └── contact.html
└── data/
    ├── appointments.json
    └── contact_messages.json
```

## 4. Install Dependencies
```bash
# Make sure you're in the virtual environment
source /var/www/mywebsite/venv/bin/activate

# Install required Python packages
pip install -r requirements.txt
```

## 5. Configure Supervisor
Create a supervisor configuration file:
```bash
sudo nano /etc/supervisor/conf.d/mywebsite.conf
```

Add the following content:
```ini
[program:mywebsite]
directory=/var/www/mywebsite
command=gunicorn --workers 4 --bind unix:/var/www/mywebsite/mywebsite.sock wsgi:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/mywebsite/mywebsite.err.log
stdout_logfile=/var/log/mywebsite/mywebsite.out.log

[supervisord]
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid
```

Create log directory:
```bash
sudo mkdir -p /var/log/mywebsite
sudo chown -R www-data:www-data /var/log/mywebsite
```

## 6. Configure Nginx
Create an Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/mywebsite
```

Add the following content:
```nginx
server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain or IP address

    location / {
        proxy_pass http://unix:/var/www/mywebsite/mywebsite.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/mywebsite/static;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/mywebsite /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # Remove default site
```

## 7. Set Permissions
```bash
# Set proper ownership and permissions
sudo chown -R www-data:www-data /var/www/mywebsite
sudo chmod -R 755 /var/www/mywebsite
```

## 8. Start and Enable Services
```bash
# Reload supervisor to read new configuration
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mywebsite

# Test Nginx configuration and restart
sudo nginx -t
sudo systemctl restart nginx

# Enable services to start on boot
sudo systemctl enable supervisor
sudo systemctl enable nginx
```

## 9. Verify Installation
```bash
# Check if services are running
sudo supervisorctl status mywebsite
sudo systemctl status nginx

# Check logs if there are issues
sudo tail -f /var/log/mywebsite/mywebsite.err.log
sudo tail -f /var/log/mywebsite/mywebsite.out.log
```

## Additional Security Considerations

### Firewall Setup
```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### SSL Configuration with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

## Troubleshooting Guide

If you encounter any issues, follow these steps:

1. Check the logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   sudo tail -f /var/log/mywebsite/mywebsite.err.log
   ```

2. Restart services:
   ```bash
   sudo supervisorctl restart mywebsite
   sudo systemctl restart nginx
   ```

3. Check permissions:
   ```bash
   sudo chown -R www-data:www-data /var/www/mywebsite
   sudo chmod -R 755 /var/www/mywebsite
   ```

4. Fixing "Errno 13 Permission denied" Error:
   If you encounter a "Permission denied" error when running the website, it's typically related to file permissions. Follow these steps:
   ```bash
   # Give ownership of the data directory and its contents to www-data
   sudo chown -R www-data:www-data /var/www/mywebsite/data
   
   # Ensure proper permissions for data files
   sudo chmod -R 664 /var/www/mywebsite/data/*.json
   
   # Ensure the data directory itself is executable
   sudo chmod 775 /var/www/mywebsite/data
   
   # If using log files, ensure proper permissions
   sudo chown -R www-data:www-data /var/log/mywebsite
   sudo chmod -R 664 /var/log/mywebsite/*.log
   ```
   
   If the error persists, verify that:
   - The application has write permissions to any directories where it needs to create/modify files
   - The user running the application (www-data) has proper access to all required directories
   - SELinux or AppArmor are not blocking access (if applicable)

## Accessing Your Website

After completing the installation, you can access your website through:
- `http://your_domain.com` (if you have a domain)
- `http://your_server_ip` (if using IP address)

Remember to replace `your_domain.com` with your actual domain name or server IP address in the Nginx configuration.

## Notes

- The website will automatically start when the system boots up
- Nginx serves as a reverse proxy
- Gunicorn is used as the WSGI server
- Supervisor manages automatic restarts
- Proper logging is configured for troubleshooting

For any additional help or issues, please check the logs mentioned in the troubleshooting section or consult the official documentation of the respective services. 