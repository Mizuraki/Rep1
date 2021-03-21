import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Firefox(executable_path=r'C:\Users\Mizuraki\PycharmProjects\Selenium\geckodriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('test_account@test.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('12345678')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    #if pytest.driver.find_element_by_tag_name('h1').text == "PetFriends":
    pytest.driver.get('http://petfriends1.herokuapp.com/my_pets')

    yield

    pytest.driver.quit()


def test_check_pets_photo():
    #Все с фото

    pytest.driver.implicitly_wait(10)

    images = pytest.driver.find_elements_by_xpath('//th/img')
    for i in range(len(images)):
        assert images[i].get_attribute('src') != '', "WARNING not all pets have a photo"


def test_check_pets_name_age_breed():
    #У всех питомцев есть имя, возраст и порода

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "all_my_pets"))
    )

    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    breed = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
    age = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')

    for i in range(len(names)):
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''


def test_check_pets_name():
    #У всех питомцев разные имена

    WebDriverWait(pytest.driver, 10).until(
        EC.title_contains('PetFriends: My Pets')
    )

    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    for i in range(len(names)):
        for j in range(i):
            assert names[i].text != names[j].text


def test_check_pets_all():
    #В списке нет повторяющихся питомцев

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "header_button"))
    )

    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    breed = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
    age = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')
    for i in range(len(names)):
        for j in range(i):
            if names[i].text == names[j].text:
                if breed[i].text == breed[j].text:
                    if age[i].text == age[j].text:
                        assert False

            else:
                assert True


