from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    print(result)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.get_list_of_pets(auth_key, filter)
    print(auth_key)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_new_pets_with_photo(name='Test_name', animal_type='Nothing',
                                  age=10, pet_photo='images\man.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_post_new_pets_without_photo(name='Test_name2', animal_type='Nothing2',
                                  age=20):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_post_set_photo_pet_id(pet_photo='images\man.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, get_pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(get_pet_id['pets']) > 0:
        pet_id = get_pet_id['pets'][0]['id']

        status, result = pf.post_add_photo_of_pet(auth_key, pet_id, pet_photo)

        assert status == 200
    else:
        raise Exception('My pets not found')


def test_delete_pet_by_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, get_pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(get_pet_id['pets']) > 0:
        pet_id = get_pet_id['pets'][0]['id']

        status, result = pf.delete_pet_by_pet_id(auth_key, pet_id)

        assert status == 200
        assert get_pet_id['pets'][:-1]['id'] != pet_id

    else:
        raise Exception('My pets not found')


def test_update_info_pet_by_pet_id(name='Put_tes', animal_type='Put_Tes', age=88):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, get_pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(get_pet_id['pets']) > 0:
        pet_id = get_pet_id['pets'][0]['id']

        status, result = pf.put_update_info_pet(auth_key, pet_id, name, animal_type, age)

        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == str(age)
    else:
        raise Exception('My pets not found')