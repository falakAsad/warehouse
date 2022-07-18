**Get Inventory**
----
  Get Inventory item by article id

* **URL**

    <host>/inventory?art_id=<art_id>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `art_id=[article id]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "{
    "art_id": "1",
    "name": "leg",
    "stock": 12
    }`


**Update Inventory Item**
----
  Update Inventory item by article id

* **URL**

    <host>/inventory?art_id=<art_id>

* **Method:**

  `PUT`

*  **URL Params**

   **Required:**

   `art_id=[article id]`

* **Data Params**

   `{
    "art_id": "1",
    "name": "leg",
    "stock": "12"
    }`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "inventory item updated successfully!",
    "ok": true
}`

**Add Inventory Item**
----
  Add a new inventory item

* **URL**

    <host>/inventory

* **Method:**

  `DELETE`

* **Data Params**

   `{
    "art_id": "1",
    "name": "leg",
    "stock": "12"
    }`


* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "inventory item created successfully!",
    "ok": true
}`


**Delete Inventory**
----
  Delete inventory item by article id

* **URL**

    <host>/inventory?art_id=<art_id>

* **Method:**

  `DELETE`

*  **URL Params**

   **Required:**

   `art_id=[article id]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "inventory item deleted successfully!",
    "ok": true
}`


**Upload Inventory Item List**
----
  Upload list of inventory using json file

* **URL**

    <host>/inventory_upload

* **Method:**

  `POST`

*  **URL Params**

   **Required:**

   `file=[file as multipart form]`
   `replace_stock=[true to replace existing stock amount with the one contained in JSON file]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "Inventory Uploaded",
    "ok": true
}`

**Remove Inventory Stock**
----
  Add stock to specific inventory item

* **URL**

    <host>/inventory_remove_stock/<art_id>/<amount_of_stock>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `art_id=[article id]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "{
    "message": "Inventory item stock changed to: 112",
    "ok": true
}`

**Add Inventory Stock**
----
  Add stock to specific inventory item

* **URL**

    <host>/inventory_add_stock/<art_id>/<amount_of_stock>

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `art_id=[article id]`
   `amount_of_stock=[amount of stock]`

* **Success Response:**

  * **Code:** 200
    **Content:** `{
    "message": "Inventory item stock changed to: 12",
    "ok": true
}`

**Get all Inventory**
----
  Get Inventory item by article id

* **URL**

    <host>/inventory_all

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200
    **Content:** `[
    {
        "art_id": "2",
        "name": "screw",
        "stock": 17
    },
    {
        "art_id": "3",
        "name": "seat",
        "stock": 2
    },
    {
        "art_id": "4",
        "name": "table top",
        "stock": 1
    },
    {
        "art_id": "1",
        "name": "leg",
        "stock": 12
    }
]`




