import sys
sys.path.append("/python-service")
from app import warehouse_app # Flask instance of the API

def clear_db():
    response = warehouse_app.test_client().get('/clear_db')

def test_add_and_get_inventory():
    clear_db()
    inventory = {
        "art_id": "1",
        "name": "leg",
        "stock": "12"
    }
    response1 = warehouse_app.test_client().post('/inventory', json = inventory)
    assert response1.status_code == 200

    response2 = warehouse_app.test_client().get('/inventory?art_id=1')
    assert response2.status_code == 200
    data = response2.json
    assert data['art_id'] == inventory['art_id']
    assert data['name'] == inventory['name']
    assert data['stock'] == int(inventory['stock'])

def test_delete_and_get_inventory():
    clear_db()

    # Add object to db
    inventory = {
        "art_id": "1",
        "name": "leg",
        "stock": "12"
    }
    response1 = warehouse_app.test_client().post('/inventory', json = inventory)
    assert response1.status_code == 200

    # Delete object from db
    response2 = warehouse_app.test_client().delete('/inventory?art_id=1')
    assert response2.status_code == 200
    assert response2.json['message'] == 'inventory item deleted successfully!'

    # Check if object does not exists
    response3 = warehouse_app.test_client().get('/inventory?art_id=1')
    assert response3.status_code == 200
    data = response3.json
    assert None == data

def test_update_inventory():
    clear_db()

    # Add object to db
    inventory = {
        "art_id": "1",
        "name": "leg",
        "stock": "12"
    }
    response1 = warehouse_app.test_client().post('/inventory', json = inventory)
    assert response1.status_code == 200

    # Update object in db
    new_inventory = {
        "art_id": "1",
        "name": "leg",
        "stock": "5"
    }
    response2 = warehouse_app.test_client().put('/inventory?art_id=1', json = new_inventory)
    assert response2.status_code == 200
    assert response2.json['message'] == 'inventory item updated successfully!'

    # Check if object does not exists
    response3 = warehouse_app.test_client().get('/inventory?art_id=1')
    assert response3.status_code == 200
    data = response3.json
    assert data['art_id'] == new_inventory['art_id']
    assert data['name'] == new_inventory['name']
    assert data['stock'] == int(new_inventory['stock'])

def test_upload_inventory_json():
    clear_db()

    # Upload json
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    response1 = warehouse_app.test_client().post(
        '/inventory_upload',
        data= {'file': open('/python-service/test/inventory.json', 'rb')},
        headers=headers, content_type='multipart/form-data')
    assert response1.status_code == 200

    # Check if object does not exists
    expected_inevntory = [
        {
            "art_id": "1",
            "name": "leg",
            "stock": "12"
        },
        {
            "art_id": "2",
            "name": "screw",
            "stock": "17"
        },
        {
            "art_id": "3",
            "name": "seat",
            "stock": "2"
        },
        {
            "art_id": "4",
            "name": "table top",
            "stock": "1"
        }
    ]
    response3 = warehouse_app.test_client().get('/inventory_all?art_id=1')
    assert response3.status_code == 200
    data = response3.json
    for i, ex_inve in enumerate(expected_inevntory):
        assert data[i]['art_id'] == ex_inve['art_id']
        assert data[i]['name'] == ex_inve['name']
        assert data[i]['stock'] == int(ex_inve['stock'])

def test_add_inventory():
    clear_db()

    # Add object to db
    inventory = {
        "art_id": "1",
        "name": "leg",
        "stock": "12"
    }
    response1 = warehouse_app.test_client().post('/inventory', json = inventory)
    assert response1.status_code == 200

    # Increase inventory stock object in db
    response2 = warehouse_app.test_client().get('/inventory_add_stock/1/10')
    assert response2.status_code == 200
    assert response2.json['message'] == 'Inventory item stock changed to: 22'

    # Check if object updated successfully
    response3 = warehouse_app.test_client().get('/inventory?art_id=1')
    assert response3.status_code == 200
    data = response3.json
    assert data['stock'] == 22

def test_remove_inventory():
    clear_db()

    # Add object to db
    inventory = {
        "art_id": "1",
        "name": "leg",
        "stock": "12"
    }
    response1 = warehouse_app.test_client().post('/inventory', json = inventory)
    assert response1.status_code == 200

    # Increase inventory stock object in db
    response2 = warehouse_app.test_client().get('/inventory_remove_stock/1/5')
    assert response2.status_code == 200
    assert response2.json['message'] == 'Inventory item stock changed to: 7'

    # Check if object updated successfully
    response3 = warehouse_app.test_client().get('/inventory?art_id=1')
    assert response3.status_code == 200
    data = response3.json
    assert data['stock'] == 7

