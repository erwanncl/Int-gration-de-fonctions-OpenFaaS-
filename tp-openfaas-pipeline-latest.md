
# TP – Intégration de fonctions OpenFaaS dans une chaîne de traitement de commandes

## Objectifs pédagogiques

Ce travail pratique a pour objectif de permettre aux étudiants de :

- Concevoir et déployer plusieurs fonctions OpenFaaS utilisant différents types de déclencheurs : HTTP, planification (CRON), file de messages (NATS) et traitement de fichiers via SFTP ;
- Automatiser une chaîne de traitement métier distribuée sur Kubernetes ;
- Intégrer des événements système dans une logique applicative conforme à des standards industriels.

---

## Contexte professionnel

L'entreprise **DataRetailX** est une plateforme spécialisée dans la gestion automatisée de commandes clients pour des sites de e-commerce. Dans le cadre d'un projet de modernisation de son système d'information, l'équipe technique souhaite adopter une architecture serverless en s'appuyant sur OpenFaaS et Kubernetes.

Chaque étudiant joue le rôle d'un développeur DevOps en charge d'automatiser le traitement des fichiers de commandes d'un client spécifique, identifié par un dossier SFTP personnel (USX, où X est le numéro du participant).

---

## Environnement de travail

- Cluster Kubernetes (local ou distant)
- OpenFaaS déployé sur le cluster
- faas-cli installé
- faas-nats activé
- Accès SFTP fourni par l’enseignant
- Un identifiant personnel de type `USX` attribué à chaque étudiant

---

## Architecture cible

Le traitement automatisé doit reposer sur trois fonctions :

### 1. Fonction planifiée `daily-fetcher`

- Déclenchée automatiquement tous les jours à 8h via une planification CRON.
- Simule l'arrivée d'une nouvelle commande en publiant un message JSON contenant la date du jour sur un topic NATS nommé `orders.import`.

### 2. Fonction `file-transformer`

- Déclenchée par la réception d'un message sur le topic `orders.import`.
- Se connecte au serveur SFTP dans le répertoire `/USX/data`, lit un fichier `input.csv`.
- Applique une transformation métier (upperCase la colonne `customers`    lowerCase `product` + créez les colonnes  `Processed-Date` i.e date +heure du traitement avec la lib datetime et colonne `process_by` avec votre identifiant).
- Enregistre le fichier transformé dans `/USX/depot` sous le nom `output.csv`.

### 3. Fonction `status-checker`

- Accessible via HTTP.
- Se connecte au SFTP et retourne le nombre de fichiers présents dans le répertoire `/USX/depot`.
- Permet de vérifier l’état d’avancement du traitement des fichiers.

---

## Variables d’environnement à configurer

```yaml
environment:
  USER_ID: "USX"
  SFTP_HOST: "ftp.heab7543.odns.fr"
  SFTP_USER: "formation_openfaas@heab7543.odns.fr"
  SFTP_PASS: "}{?Z]~Pxq!R9"
```

Ces variables sont à insérer dans le YAML de déploiement des fonctions `file-transformer` et `status-checker`.

---

## Évaluation attendue

### 1. Code source des trois fonctions (organisation claire)

**Réponse :**
```
[Prévoir ici un lien Git ou lister les répertoires de chaque fonction avec leur contenu : handler.py, YAML, etc.]
```

### 2. Démonstration fonctionnelle

**Réponse :**
```
Décrivez ici le fonctionnement : test CRON, message reçu par NATS, transformation réalisée, et résultat obtenu.
```

### 3. Analyse des logs / sorties attendues

**Réponse :**
```
Exemples de logs issus de la fonction de transformation, de la publication NATS, ou de la fonction HTTP.
```

### 4. Rapport synthétique (2 pages maximum)

**Réponse :**
```
Décrivez ici votre architecture, les choix techniques faits, les difficultés rencontrées, et les limites éventuelles.
```

---

## Délivrables

- Dépôt Git ou archive contenant les trois fonctions et un fichier `README.md`
- Rapport PDF accompagnant le code
- Captures éventuelles de l'exécution dans le cluster
