**Get Product**
----
  Get product by name

* **URL**

    <host>/product?name=<name>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `name=[string]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "contain_articles": [
        {
            "amount_of": 4,
            "art_id": "1"
        },
        {
            "amount_of": 8,
            "art_id": "2"
        },
        {
            "amount_of": 1,
            "art_id": "3"
        }
    ],
    "name": "Dining Chair"
}`


**Update Product**
----
  Update product by name

* **URL**

    <host>/product?name=<name>

* **Method:**

  `PUT`

*  **URL Params**

   **Required:**

   `name=[string]`

* **Data Params**

    `{ "name": "Dining Chair", "contain_articles": [ { "art_id": "1", "amount_of": "4" }, { "art_id": "2", "amount_of": "8" }, { "art_id": "3", "amount_of": "1" } ] }`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "Product updated successfully!",
    "ok": true
}`

**Add Product**
----
  Add a new product

* **URL**

    <host>/product>

* **Method:**

  `DELETE`

* **Data Params**

  `{
    "name": "Dining Chair",
    "contain_articles": [
    {
        "art_id": "1",
        "amount_of": "4"
    },
    {
        "art_id": "2",
        "amount_of": "8"
    },
    {
        "art_id": "3",
        "amount_of": "1"
    }
    ]
}`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "Product created successfully!",
    "ok": true
}`


**Delete Product**
----
  Delete product by name

* **URL**

    <host>/product?name=<name>

* **Method:**

  `DELETE`

*  **URL Params**

   **Required:**

   `name=[string]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
        "message": "Product deleted successfully!",
        "ok": true
    }`


**Upload Product List**
----
  Upload list of products using json file

* **URL**

    <host>/product_upload

* **Method:**

  `POST`

*  **URL Params**

   **Required:**

   `file=[JSON file as multipart form]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "Products Uploaded",
    "ok": true
}`

**Get all Products**
----
  List all products with quantity available

* **URL**

    <host>/product_all

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200
    **Content:** `[
    {
        "inventory": [
            {
                "amount_of": 4,
                "art_id": "1",
                "name": "leg",
                "stock": 12
            },
            {
                "amount_of": 8,
                "art_id": "2",
                "name": "screw",
                "stock": 17
            },
            {
                "amount_of": 1,
                "art_id": "3",
                "name": "seat",
                "stock": 2
            }
        ],
        "name": "Dining Chair",
        "quantity": 2.0
    },
    {
        "inventory": [
            {
                "amount_of": 4,
                "art_id": "1",
                "name": "leg",
                "stock": 12
            },
            {
                "amount_of": 8,
                "art_id": "2",
                "name": "screw",
                "stock": 17
            },
            {
                "amount_of": 1,
                "art_id": "4",
                "name": "table top",
                "stock": 1
            }
        ],
        "name": "Dinning Table",
        "quantity": 1.0
    }
]`


