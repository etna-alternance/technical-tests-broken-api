# broken-api

Pour démarrer la stack :

```
docker-compose up --build
```

> Pour lancer la stack en tâche de fond, on peut ajouter un `-d` à la commande ci-dessus.

Puis, pour exécuter les tests :

```
docker-compose exec -T tests python3 -m pytest .
```
