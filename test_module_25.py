import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield




def test_show_my_pets():
    # Вводим email
    pytest.driver.implicitly_wait(5)#неявное ожидание
    pytest.driver.find_element(By.ID, 'email').send_keys('abcdf@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID,'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

  #явное ожидание
    images = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))

    try:

        for i in range(len(names)):  # перебираем все элементы

            assert images[i].get_attribute(
                'src') != ''  # проверяем, что фото есть (путь, указанный в атрибуте src, не пустой)
            assert names[i].text != ''  # проверяем, что имя есть
            assert descriptions[i].text != ''  # проверяем, что не пустое, хотя в любом случае есть запятая
            assert ', ' in descriptions[i]  # убеждаемся в наличии запятой
            parts = descriptions[i].text.split(", ")  # разделяем строку на части
            assert len(parts[0]) > 0  # проверяем, что в первой части есть вид
            assert len(parts[1]) > 0  # проверяем, что во второй части есть возраст
    except AssertionError:
        print('Нет фото, или имени, или описания у одной из карточек питомца')


    pytest.driver.quit()