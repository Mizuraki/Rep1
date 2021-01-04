from api import PetFriends
from settings import valid_email, valid_password

#19.7. Итоговое практическое задание#

pf = PetFriends()


def test_get_api_key_for_nonvalid_user(email='error_mail@mail.ru', password='error_pass'):
    '''не правильный логин и пароль'''

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_empty_user(email='', password=''):
    '''пустой логин и пароль'''

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_nonvalid_key(filter=''):
    '''не верный ключ аутентификации'''
    auth_key = {'key': 'ERROR_KEY'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


def test_post_new_pets_without_photo_longname(name='T'*255, animal_type='Nothing2',
                                  age=20):
    '''длинное значение имени'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200
    

def test_post_new_pets_without_photo_longtype(name='Test_name2', animal_type='N'*255,
                                  age=20):
    '''длинное значение типа животного'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200
    

def test_post_new_pets_without_photo_longage(name='Test_name2', animal_type='Nothing2',
                                  age=20**200):
    '''длинное значение возраста'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200
    

def test_post_new_pets_without_photo_emptydata(name='', animal_type='',
                                  age=''):
    '''пустые значения имени, типа, возраста'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200


def test_post_new_pets_with_photo_emptydata(name='', animal_type='',
                                  age='', pet_photo='images\lis.jpg'):
    '''пустые данные, кроме фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status != 200
    

def test_update_info_pet_longname(name='P'*255, animal_type='Put_Tes', age=88):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, get_pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(get_pet_id['pets']) > 0:
        pet_id = get_pet_id['pets'][0]['id']

        status, result = pf.put_update_info_pet(auth_key, pet_id, name, animal_type, age)

        assert status == 200
    else:
        raise Exception('My pets not found')


def test_update_info_pet_longtype(name='Put_tes', animal_type='N'*255, age=88):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, get_pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(get_pet_id['pets']) > 0:
        pet_id = get_pet_id['pets'][0]['id']

        status, result = pf.put_update_info_pet(auth_key, pet_id, name, animal_type, age)

        assert status != 200
    else:
        raise Exception('My pets not found')


def test_update_info_pet_longage(name='Put_tes', animal_type='Put_Tes', age=88**200):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, get_pet_id = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(get_pet_id['pets']) > 0:
        pet_id = get_pet_id['pets'][0]['id']

        status, result = pf.put_update_info_pet(auth_key, pet_id, name, animal_type, age)

        assert status != 200
    else:
        raise Exception('My pets not found')
