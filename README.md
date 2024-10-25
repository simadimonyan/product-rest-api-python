# Products API

## Description

Product REST API is development test assignment for an interview

- Python
- Fast API
- SQLAlchemy
- Docker 
- Git

## Installation

```bash
   sudo docker compose up
```

![alt text](image.png)

![development test assignment](Task.pdf)

## API

### Request product by ID

**URL:** `GET /api/products/product/{id}`

**Parameters:**
- `id` (str): product identifier.

**Request:**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/products/product/f51e8cdd187ec3c32df13f318b0e92ca505ad154eaf38faa1aff931116241c08' \
  -H 'accept: application/json'
```

**Response:**
```json
[
  {
    "id": "f51e8cdd187ec3c32df13f318b0e92ca505ad154eaf38faa1aff931116241c08",
    "category": "Laptops",
    "name": "Laptop",
    "cost": 150000,
    "amount": 10,
    "currency": "Rubles"
  }
]
```

### Request all products

**URL:** `GET /api/products/`

**Parameters:**
- `category` (str, optional): Filter by product category.
- `name` (str, optional): Filter by product name.
- `max_price` (float, optional): Filter by maximum price.
- `min_price` (float, optional): Filter by minimum price.
- `amount` (int, optional): Filter by product amount.
- `currency` (str, optional): Filter by product currency.

**Request:**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/products/?category=Laptops&min_price=50000' \
  -H 'accept: application/json'
```

**Response:**
```json
[
  {
    "id": "f51e8cdd187ec3c32df13f318b0e92ca505ad154eaf38faa1aff931116241c08",
    "category": "Laptops",
    "name": "Macbook 14 Pro",
    "cost": 150000,
    "amount": 10,
    "currency": "Rubles"
  },
  {
    "id": "363c288a13f467dea92eaa95144fae17810f5f1f1f136e2da0fbde937336a8bd",
    "category": "Laptops",
    "name": "Lenovo Flip",
    "cost": 100000,
    "amount": 7,
    "currency": "Rubles"
  }
]
```

### Product Creation

**URL:** `POST /api/products/product/`

**Request:**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/products/product/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
   "category": "Electronics",
   "name": "New Product",
   "amount": 10,
   "cost": 50.0,
   "currency": "USD"
}'
```

**Response:**
```json
{
  "message": "The product created successfully",
  "product": {
    "id": "957f4526545431479b2d654899753854fd446b12a2e1f64b315583b4dd919d6c",
    "category": "Electronics",
    "name": "New Product",
    "cost": 50,
    "amount": 10,
    "currency": "USD"
  }
}
```

### Creating multiple products

**URL:** `POST /api/products/products/`

**Request:**
```json
curl -X 'POST' \
  'http://localhost:8000/api/products/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
        "category": "Electronics",
        "name": "New Product 1",
        "amount": 10,
        "cost": 50.0,
        "currency": "USD"
    },
    {
        "category": "Electronics",
        "name": "New Product 2",
        "amount": 10,
        "cost": 50.0,
        "currency": "USD"
    }
]'
```

**Reponse:**
```json
{
  "message": "Products created successfully",
  "products": [
    {
      "id": "db8477152a6511bac6db0362b98dd81890f6ebf7f5af4cd0d4abfeb7cbfee4ee",
      "category": "Electronics",
      "name": "New Product 1",
      "cost": 50,
      "amount": 10,
      "currency": "USD"
    },
    {
      "id": "54d5be67acc3912d1d754e6caaac22bada757be77915e12fcfee038938811556",
      "category": "Electronics",
      "name": "New Product 2",
      "cost": 50,
      "amount": 10,
      "currency": "USD"
    }
  ]
}
```

### Deleting multiple products

**URL:** `DELETE /api/products/products/`

**Parameters:**
- `ids` (list[str]): Product identifiers list.

**Request:**
```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/products/products/?ids=db8477152a6511bac6db0362b98dd81890f6ebf7f5af4cd0d4abfeb7cbfee4ee&ids=54d5be67acc3912d1d754e6caaac22bada757be77915e12fcfee038938811556' \
  -H 'accept: application/json'
```

**Пример ответа:**
```json
{
  "message": "Products deleted successfully",
  "products": [
    {
      "id": "db8477152a6511bac6db0362b98dd81890f6ebf7f5af4cd0d4abfeb7cbfee4ee",
      "category": "Electronics",
      "name": "New Product 1",
      "cost": 50,
      "amount": 10,
      "currency": "USD"
    },
    {
      "id": "54d5be67acc3912d1d754e6caaac22bada757be77915e12fcfee038938811556",
      "category": "Electronics",
      "name": "New Product 2",
      "cost": 50,
      "amount": 10,
      "currency": "USD"
    }
  ]
}
```

### Delete product

**URL:** `DELETE /api/products/product/{id}`

**Parameters:**
- `id` (str): Product ID.

**Request:**
```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/products/product/957f4526545431479b2d654899753854fd446b12a2e1f64b315583b4dd919d6c' \
  -H 'accept: application/json'
```

**Response:**
```json
{
  "message": "The product deleted successfully",
  "product": {
    "id": "957f4526545431479b2d654899753854fd446b12a2e1f64b315583b4dd919d6c",
    "category": "Electronics",
    "name": "New Product",
    "cost": 50,
    "amount": 10,
    "currency": "USD"
  }
}
```

### Product update

**URL:** `PUT /api/products/product/{id}`

**Parameters:**
- `id` (str): Product ID.

**Request:**
```json
curl -X 'PUT' \
  'http://localhost:8000/api/products/product/f51e8cdd187ec3c32df13f318b0e92ca505ad154eaf38faa1aff931116241c08' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "category": "Laptops",
  "name": "MacBook 16 Pro ",
  "amount": 1,
  "cost": 20000,
  "currency": "Rubles"
}'
```

**Reponse:**
```json
{
  "message": "The product updated successfully",
  "product": {
    "id": "6863efd1c074b3335e0c01b086ef7f75be858bdde26e4324de522918a896f7fc",
    "category": "Laptops",
    "name": "MacBook 16 Pro ",
    "cost": 20000,
    "amount": 1,
    "currency": "Rubles"
  }
}
```

## Contact

- **Name:** Dimitri Simonyan
- **Email:** simadimonyan@gmail.com
- **URL:** [GitHub](https://github.com/simadimonyan)
