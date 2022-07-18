import sys
sys.path.append("/python-service")
from app import warehouse_app # Flask instance of the API

def clear_db():
    warehouse_app.test_client().get('/clear_db')

def test_add_and_get_product():
    clear_db()
    product = {
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
    }
    response1 = warehouse_app.test_client().post('/product', json = product)
    assert response1.status_code == 200

    response2 = warehouse_app.test_client().get('/product?name=Dining Chair')
    assert response2.status_code == 200
    data = response2.json
    assert data['name'] == product['name']
    for i, art in enumerate(product['contain_articles']):
        assert data['contain_articles'][i]['art_id'] == art['art_id']
        assert data['contain_articles'][i]['amount_of'] == int(art['amount_of'])

def test_delete_and_get_product():
    clear_db()

    # Add object to db
    product = {
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
    }
    response1 = warehouse_app.test_client().post('/product', json = product)
    assert response1.status_code == 200

    # Delete object from db
    response2 = warehouse_app.test_client().delete('/product?name=Dining Chair')
    assert response2.status_code == 200
    assert response2.json['message'] == 'Product deleted successfully!'

    # Check if object does not exists
    response3 = warehouse_app.test_client().get('/product?name=Dining Chair')
    assert response3.status_code == 200
    data = response3.json
    assert None == data

def test_update_product():
    clear_db()

    # Add object to db
    product = {
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
    }
    response1 = warehouse_app.test_client().post('/product', json = product)
    assert response1.status_code == 200

    # Update object in db
    new_product = {
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
    }
    response2 = warehouse_app.test_client().put('/product?name=Dining Chair', json = new_product)
    assert response2.status_code == 200
    assert response2.json['message'] == 'Product updated successfully!'

    # Check if object does not exists
    response3 = warehouse_app.test_client().get('/product?name=Dining Chair')
    assert response3.status_code == 200
    data = response3.json
    assert data['name'] == product['name']
    for i, art in enumerate(product['contain_articles']):
        assert data['contain_articles'][i]['art_id'] == art['art_id']
        assert data['contain_articles'][i]['amount_of'] == int(art['amount_of'])

def test_upload_product_json():
    clear_db()

    # Upload product json
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response1 = warehouse_app.test_client().post(
        '/product_upload',
        data= {'file': open('/python-service/test/products.json', 'rb')},
        headers=headers, content_type='multipart/form-data')
    assert response1.status_code == 200

    # Upload inventory json
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response1 = warehouse_app.test_client().post(
        '/inventory_upload',
        data= {'file': open('/python-service/test/inventory.json', 'rb')},
        headers=headers, content_type='multipart/form-data')
    assert response1.status_code == 200

    # Check if object does not exists
    expected_products = [
        {
            "name": "Dining Chair",
            "inventory":
            [
                {
                    "art_id": "1",
                    "amount_of": 4,
                    "name": "leg",
                    "stock": 12
                },
                {
                    "art_id": "2",
                    "amount_of": 8,
                    "name": "screw",
                    "stock": 17
                },
                {
                    "art_id": "3",
                    "amount_of": 1,
                    "name": "seat",
                    "stock": 2
                }
            ],
            "quantity": 2.0
        },
        {
            "name": "Dinning Table",
            "inventory":
            [
                {
                    "art_id": "1",
                    "amount_of": 4,
                    "name": "leg",
                    "stock": 12
                },
                {
                    "art_id": "2",
                    "amount_of": 8,
                    "name": "screw",
                    "stock": 17
                },
                {
                    "art_id": "4",
                    "amount_of": 1,
                    "name": "table top",
                    "stock": 1
                }
            ],
            "quantity": 1.0
        }
    ]
    response3 = warehouse_app.test_client().get('/product_all?name=Dining Chair')
    assert response3.status_code == 200
    data = response3.json
    for i, ex_prod in enumerate(expected_products):
        assert data[i]['name'] == ex_prod['name']
        assert int(data[i]['quantity']) == int(ex_prod['quantity'])
        for j, art in enumerate(ex_prod['inventory']):
            assert data[i]['inventory'][j]['art_id'] == art['art_id']
            assert data[i]['inventory'][j]['amount_of'] == int(art['amount_of'])
            assert data[i]['inventory'][j]['name'] == art['name']
            assert data[i]['inventory'][j]['stock'] == int(art['stock'])

def test_sell_json():
    clear_db()

    # Upload product json
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response1 = warehouse_app.test_client().post(
        '/product_upload',
        data= {'file': open('/python-service/test/products.json', 'rb')},
        headers=headers, content_type='multipart/form-data')
    assert response1.status_code == 200

    # Upload inventory json
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response1 = warehouse_app.test_client().post(
        '/inventory_upload',
        data= {'file': open('/python-service/test/inventory.json', 'rb')},
        headers=headers, content_type='multipart/form-data')
    assert response1.status_code == 200

    # Check if object does not exists
    expected_products = [
        {
            "name": "Dining Chair",
            "inventory":
            [
                {
                    "art_id": "1",
                    "amount_of": 4,
                    "name": "leg",
                    "stock": 8
                },
                {
                    "art_id": "2",
                    "amount_of": 8,
                    "name": "screw",
                    "stock": 9
                },
                {
                    "art_id": "3",
                    "amount_of": 1,
                    "name": "seat",
                    "stock": 1
                }
            ],
            "quantity": 1.0
        },
        {
            "name": "Dinning Table",
            "inventory":
            [
                {
                    "art_id": "1",
                    "amount_of": 4,
                    "name": "leg",
                    "stock": 8
                },
                {
                    "art_id": "2",
                    "amount_of": 8,
                    "name": "screw",
                    "stock": 9
                },
                {
                    "art_id": "4",
                    "amount_of": 1,
                    "name": "table top",
                    "stock": 1
                }
            ],
            "quantity": 1.0
        }
    ]



    response3 = warehouse_app.test_client().get('/product_sell/Dining Chair')
    assert response3.status_code == 200

    response4 = warehouse_app.test_client().get('/product_all?name=Dining Chair')
    assert response4.status_code == 200
    data = response4.json

    for i, ex_prod in enumerate(expected_products):
        assert data[i]['name'] == ex_prod['name']
        assert int(data[i]['quantity']) == int(ex_prod['quantity'])
        for j, art in enumerate(ex_prod['inventory']):
            assert data[i]['inventory'][j]['art_id'] == art['art_id']
            assert data[i]['inventory'][j]['amount_of'] == int(art['amount_of'])
            assert data[i]['inventory'][j]['name'] == art['name']
            assert data[i]['inventory'][j]['stock'] == int(art['stock'])