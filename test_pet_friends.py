from api import PetFriends
from settings import valid_email, valid_password, notvalid_email, notvalid_age
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_notvalid_user(email=notvalid_email, password=valid_password):
    status = pf.get_api_key(email, password)
    assert status != 200

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(filter=""):
    _, auth_key = pf.get_api_key(notvalid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200


def test_add_new_pet_with_valid_data(name='Olivia', animal_type='labrador',
                                     age='3', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_notvalid_age(name='Kisa', animal_type='siberian cat',
                                      age=notvalid_age, pet_photo='images/cat.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result[age] is int


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Gerry", "snail", '5', "images/snail.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Gerry', animal_type='snail',
                                         age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    else:
        raise Exception("There is no my pets")
def test_add_new_pet_no_photo_with_valid_data(name='Kot', animal_type='catynich',
                                              age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] is ''


def test_successful_update_self_pet_photo(pet_photo='images/cat.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] is not ''
    else:
        raise Exception("There is no my pets")