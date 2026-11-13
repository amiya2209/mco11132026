choices and tradeoffs - 

Python 3.15.2 - backedn
html for frontend
Flask framework 
nginx - serves the page and forwards API requests to flask
SQLite - persistent storage
Podman Desktop
GitHub Actions

Ask - Reads a message from SQLite through the Flask API. Users can edit and save the message.

browser - nginx - Flask - SQLite - persist

Build and command run - 

podman info
podman compose version
podman compose up --build -d
podman compose restart web
podman compose ps
podman compose logs
podman compose down

http://localhost:8080

The firt message is Hello World. Enter a new message, click Save, and refresh the page.

SQLite stores the message in /data/message.db. The message-data named volume is mounted at /data.

The db file is outside the API container filesystem. Removing and recreating containers retains the volume.

CI pipeline
Code pushed - Checkout - Python 3.15.2 - Install Flask - Run tests - Pass/fail

K8s- 
Replicas - One API replica while SQLite is used. nginx can scale independently.
Services - Internal Services provide stable addresses for nginx and the API. Add ingress and TLS when external access is required.
PVCs - Mount a PVC at /data to retain SQLite across pod replacement. Verify storage permissions, filesystem, and backup restoration.
Configuration - Use a ConfigMap for nonsecret settings and nginx configuration. Package the HTML inside an nginx image instead of mounting local files.
Secrets - SQLite currently needs no password. Use Secrets with restricted access if credentials are introduced.
Rolling updates	- Use Recreate for the single SQLite API, accepting brief downtime. nginx can use rolling updates.

Time Spend - 3-4 hours