BASE_URL = http://127.0.0.1:8000/api/
## Auth API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | http://127.0.0.1:8000/api/auth/register/ | Créer un compte utilisateur | ❌ |
| POST | http://127.0.0.1:8000/api/auth/login/ | Se connecter et obtenir JWT (access + refresh) | ❌ |
| POST | http://127.0.0.1:8000/api/auth/token/refresh/ | Rafraîchir un access token avec refresh token | ❌ |


## Products API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | /products/ | Liste de tous les produits | ❌ |
| GET | /products/{id}/ | Détail d’un produit | ❌ |
| GET | /products/available/ | Liste des produits disponibles | ❌ |
| POST | /products/ | Créer un produit (admin seulement) | ✅ |
| PUT | /products/{id}/ | Mettre à jour un produit (admin) | ✅ |
| PATCH | /products/{id}/ | Mettre à jour partiellement (admin) | ✅ |
| DELETE | /products/{id}/ | Supprimer un produit (admin) | ✅ |

---

## Cart API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | /cart/ | Voir le panier de l’utilisateur | ✅ |
| POST | /cart/add/ | Ajouter un produit au panier | ✅ |
| PUT | /cart/update_item/ | Mettre à jour la quantité d’un produit | ✅ |
| DELETE | /cart/remove/ | Supprimer un produit du panier | ✅ |
| POST | /cart/checkout/ | Passer une commande et vider le panier | ✅ |

---

## Orders API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | /orders/ | Lister toutes les commandes de l’utilisateur | ✅ |
| GET | /orders/{id}/ | Détail d’une commande | ✅ |
| POST | /orders/ | Créer une commande (checkout via cart) | ✅ |
| PUT | /orders/{id}/ | Modifier une commande (optionnel) | ✅ |
| DELETE | /orders/{id}/ | Supprimer une commande (optionnel) | ✅ |

---

## Favorites API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | /favorites/ | Lister les produits favoris de l’utilisateur | ✅ |
| POST | /favorites/ | Ajouter un produit aux favoris (product_id) | ✅ |
| DELETE | /favorites/{id}/ | Supprimer un produit des favoris | ✅ |

---

## Headers Authentification JWT

Pour toutes les requêtes nécessitant auth :