# Robot Data Collector — API Documentation

API Flask minimaliste pour collecter et stocker des snapshots de données robot + personnes dans une base MySQL (JSON natif).

---

## Démarrage rapide

```bash
docker-compose up -d
```

| Service     | URL                        |
|-------------|----------------------------|
| API Flask   | http://localhost:5000      |
| phpMyAdmin  | http://localhost:8080      |

---

## Endpoint

### `POST /api/data`

Enregistre un snapshot des données robot + personnes dans la base MySQL.

#### Headers

| Clé            | Valeur             |
|----------------|--------------------|
| `Content-Type` | `application/json` |

#### Corps de la requête

```json
{
  "bot": {
    "x": 1.231212,
    "y": 0.2565,
    "z": 45,
    "orientation": 1455,
    "vitesse": 1.5,
    "acceleration": 2.5,
    "trajectoire_courante": ["node1", "node2"],
    "trajectoire_planifiee": ["node3", "node4"],
    "cout_navigation": 122
  },
  "persons": [
    { "x": 1.23, "y": 0.25, "z": 45, "position": "node2" },
    { "x": 0.80, "y": 1.10, "z": 45, "position": "node1" }
  ],
  "datetime": "2026-05-30:17:10"
}
```

#### Description des champs

| Champ                      | Type        | Requis | Description                          |
|----------------------------|-------------|--------|--------------------------------------|
| `bot`                      | objet JSON  | Oui    | État complet du robot                |
| `bot.x / y / z`            | float       | —      | Position 3D                          |
| `bot.orientation`          | float       | —      | Orientation en degrés                |
| `bot.vitesse`              | float       | —      | Vitesse courante                     |
| `bot.acceleration`         | float       | —      | Accélération courante                |
| `bot.trajectoire_courante` | any         | —      | Trajectoire en cours (format libre)  |
| `bot.trajectoire_planifiee`| any         | —      | Trajectoire planifiée (format libre) |
| `bot.cout_navigation`      | float       | —      | Coût de navigation                   |
| `persons`                  | tableau JSON| Oui    | Liste des obstacles/personnes        |
| `persons[].x / y / z`     | float       | —      | Position 3D de la personne           |
| `persons[].position`       | string      | —      | Nœud de trajectoire occupé           |
| `datetime`                 | string      | Oui    | Horodatage du snapshot               |

#### Réponses

**201 Created** — données enregistrées :

```json
{ "message": "Données enregistrées avec succès", "id": 42 }
```

**400 Bad Request** — corps invalide ou champs manquants :

```json
{ "error": "Champs requis manquants: bot, persons, datetime" }
```

---

## Exemple cURL

```bash
curl -X POST http://localhost:5000/api/data \
  -H "Content-Type: application/json" \
  -d '{
    "bot": {
      "x": 1.231212, "y": 0.2565, "z": 45,
      "orientation": 1455, "vitesse": 1.5,
      "acceleration": 2.5,
      "trajectoire_courante": ["node1", "node2"],
      "trajectoire_planifiee": ["node3", "node4"],
      "cout_navigation": 122
    },
    "persons": [
      { "x": 1.23, "y": 0.25, "z": 45, "position": "node2" }
    ],
    "datetime": "2026-05-30:17:10"
  }'
```

---

## Modèle en base — table `robot_data`

| Colonne      | Type MySQL        | Description                  |
|--------------|-------------------|------------------------------|
| `id`         | INT AUTO_INCREMENT| Clé primaire                 |
| `bot`        | JSON              | Données du robot             |
| `persons`    | JSON              | Données des personnes        |
| `datetime`   | VARCHAR(50)       | Horodatage fourni            |
| `created_at` | DATETIME          | Heure d'insertion en base    |

---

## Exporter la base via phpMyAdmin

1. Ouvrir [http://localhost:8080](http://localhost:8080)
2. Sélectionner la base `robotdb`
3. Cliquer sur la table `robot_data`
4. Onglet **Exporter** → choisir le format (SQL, CSV, JSON…)

---

## Structure du projet

```
projet/
├── app/
│   ├── __init__.py          # Factory Flask + init SQLAlchemy
│   ├── models.py            # Modèle RobotData
│   └── routes.py            # Route POST /api/data
├── config.py                # Configuration base de données
├── run.py                   # Point d'entrée
├── requirements.txt
├── Dockerfile
├── docker-compose.yml       # MySQL + phpMyAdmin + API
└── Jenkinsfile              # Pipeline CI/CD minimal
```
