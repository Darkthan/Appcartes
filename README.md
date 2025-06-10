# Appcartes

Application Flask de gestion de demandes de cartes pour les étudiants. Elle fournit une interface d'administration, une interface pour l'imprimeur et une borne d'information. L'authentification peut être déléguée à Authelia via le reverse proxy Nginx.

## Fonctionnalités

- Gestion des utilisateurs avec rôles (`admin`, `printer` ou `user`).
- Import de listes d'étudiants au format CSV.
- Saisie d'une demande de carte pour un étudiant.
- Suivi des statuts d'impression (`Demande`, `En cours`, `Disponible`).
- Affichage en mode kiosque des cartes prêtes ou en cours de préparation.

## Démarrage rapide

1. Cloner le dépôt puis construire et lancer les conteneurs :

```bash
docker-compose up --build
```

2. Le site est alors accessible sur `http://localhost:8080` via Nginx qui passe les requêtes par Authelia pour l'authentification (sauf pour `/kiosk`).

3. Les comptes par défaut sont définis dans `authelia/users.yml`. Connectez-vous en tant qu'`admin` pour créer d'autres utilisateurs dans l'application.

## Configuration

- `SECRET_KEY` : clé secrète Flask (variable d'environnement dans `docker-compose.yml`).
- `DATABASE_URL` : URL SQLAlchemy (par défaut `sqlite:///app.db`).
- Les paramètres d'Authelia se trouvent sous `authelia/` (fichiers `configuration.yml` et `users.yml`).
- Le proxy Nginx est configuré via `nginx.conf` pour protéger toutes les routes à l'exception de `/kiosk`.

## Structure du projet

```
app/               Code Flask
  __init__.py      Création de l'application et base de données
  models.py        Modèles SQLAlchemy (User, Student, CardRequest)
  routes.py        Vues Flask protégées par connexion
  templates/       Templates Jinja2
Dockerfile         Image de l'application
nginx.conf         Configuration du reverse proxy
authelia/          Configuration et comptes Authelia
```

## Exécution sans Docker

Il est aussi possible d'exécuter l'application localement :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app
export SECRET_KEY=changeme
flask run
```

La base SQLite `app.db` sera créée automatiquement au démarrage.

## Licence

Ce projet est distribué sous licence Apache 2.0. Voir le fichier `LICENSE` pour plus d'informations.

