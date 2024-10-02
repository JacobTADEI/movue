# Utiliser une image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de ton projet dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 (port par défaut de Flask)
EXPOSE 5000

# Définir la commande pour exécuter l'application
CMD ["python", "app.py"]