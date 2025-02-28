import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Функция для генерации случайного значения rand (например, "0.123456789")
def generate_rand():
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(12))
    return f"0.{random_digits}"

def main():
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)

    # Формируем URL с фильтрами
    base_url = ("https://www.reg.ru/domain/new/rereg?"
                "rand={rand}&filter_dnames=&filter_expiring_from=2025-03-03&"
                "filter_expiring_to=2025-03-07&filter_current_bid_from=&"
                "filter_current_bid_to=&filter_age_from=&filter_age_to=&"
                "filter_symbols_from=&filter_symbols_to=")
    
    rand_value = generate_rand()
    url = base_url.format(rand=rand_value)
    driver.get(url)
    
    # Пытаемся нажать на кнопку согласия с куки, если она появляется
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 
            ".ds-promo-button.ds-promo-button_theme_secondary.ds-promo-button_size_s.b-policy-info__button"
        )))
        cookie_button.click()
        print("[INFO] Нажата кнопка согласия с куки")
    except Exception as e:
        print(f"[INFO] Кнопка согласия с куки не найдена или возникла ошибка: {e}")

    output_file = "domains.txt"
    
    # Открываем файл для дозаписи доменов
    with open(output_file, "a", encoding="utf-8") as f:
        while True:
            try:
                # Ждем появления элементов с доменами
                wait.until(EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "p-domain-new-rereg__link")
                ))
                
                # Добавляем дополнительный вывод: сколько элементов найдено
                domain_elements = driver.find_elements(By.CLASS_NAME, "p-domain-new-rereg__link")
                print(f"[DEBUG] Найдено элементов с доменами: {len(domain_elements)}")
                
                # Задержка 30-60 секунд для имитации парсинга страницы
                page_delay = random.uniform(30, 60)
                print(f"[INFO] Ожидание {page_delay:.2f} секунд для парсинга страницы...")
                time.sleep(page_delay)

                # Собираем домены и записываем их в файл
                for elem in domain_elements:
                    domain = elem.text.strip()
                    if domain:
                        f.write(domain + "\n")
                        f.flush()  # Принудительно сбрасываем данные в файл
                        print(f"[DATA] {domain}")
                
                # Поиск кнопки "Next" по атрибуту aria-label="Next"
                next_buttons = driver.find_elements(By.XPATH, "//a[@aria-label='Next']")
                if next_buttons:
                    # Задержка 10-30 секунд перед переходом на следующую страницу
                    next_delay = random.uniform(10, 30)
                    print(f"[INFO] Ожидание {next_delay:.2f} секунд перед переходом на следующую страницу...")
                    time.sleep(next_delay)

                    next_button = next_buttons[0]
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    next_button.click()
                    
                    # Дополнительная задержка после клика для загрузки следующей страницы (30-60 секунд)
                    post_click_delay = random.uniform(30, 60)
                    print(f"[INFO] Ожидание {post_click_delay:.2f} секунд для загрузки следующей страницы...")
                    time.sleep(post_click_delay)
                else:
                    print("[INFO] Кнопка 'Next' не найдена. Завершение работы.")
                    break

            except Exception as e:
                print(f"[ERROR] Произошла ошибка: {e}")
                break

    driver.quit()

if __name__ == "__main__":
    main()
