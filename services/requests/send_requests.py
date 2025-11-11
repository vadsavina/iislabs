import requests
import random
import time
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Адрес ML сервиса (имя сервиса в docker compose)
ML_SERVICE_URL = "http://ml_service:8000/api/prediction"

# Примеры данных для тестирования
test_data_examples = [
    {
        "mobile_id": 1,
        "item_features": {
            "battery_power": 842,
            "blue": 0,
            "clock_speed": 2.2,
            "dual_sim": 0,
            "fc": 1,
            "four_g": 0,
            "int_memory": 7,
            "m_dep": 0.6,
            "mobile_wt": 188,
            "n_cores": 2,
            "pc": 2,
            "px_height": 20,
            "px_width": 756,
            "ram": 2549,
            "sc_h": 9,
            "sc_w": 7,
            "talk_time": 19,
            "three_g": 0,
            "touch_screen": 0,
            "wifi": 1
        }
    },
    {
        "mobile_id": 2,
        "item_features": {
            "battery_power": 1500,
            "blue": 1,
            "clock_speed": 2.8,
            "dual_sim": 1,
            "fc": 5,
            "four_g": 1,
            "int_memory": 64,
            "m_dep": 0.5,
            "mobile_wt": 150,
            "n_cores": 8,
            "pc": 12,
            "px_height": 1920,
            "px_width": 1080,
            "ram": 3000,
            "sc_h": 15,
            "sc_w": 8,
            "talk_time": 20,
            "three_g": 1,
            "touch_screen": 1,
            "wifi": 1
        }
    },
    {
        "mobile_id": 3,
        "item_features": {
            "battery_power": 500,
            "blue": 0,
            "clock_speed": 1.0,
            "dual_sim": 0,
            "fc": 0,
            "four_g": 0,
            "int_memory": 4,
            "m_dep": 0.8,
            "mobile_wt": 200,
            "n_cores": 1,
            "pc": 1,
            "px_height": 480,
            "px_width": 320,
            "ram": 500,
            "sc_h": 5,
            "sc_w": 3,
            "talk_time": 10,
            "three_g": 0,
            "touch_screen": 0,
            "wifi": 0
        }
    },
    {
        "mobile_id": 4,
        "item_features": {
            "battery_power": 2000,
            "blue": 1,
            "clock_speed": 3.0,
            "dual_sim": 1,
            "fc": 8,
            "four_g": 1,
            "int_memory": 128,
            "m_dep": 0.3,
            "mobile_wt": 180,
            "n_cores": 8,
            "pc": 16,
            "px_height": 2560,
            "px_width": 1440,
            "ram": 4000,
            "sc_h": 16,
            "sc_w": 9,
            "talk_time": 24,
            "three_g": 1,
            "touch_screen": 1,
            "wifi": 1
        }
    }
]


def send_request():
    """Отправка случайного запроса к ML сервису"""
    try:
        # Выбираем случайный пример данных
        test_data = random.choice(test_data_examples)
        
        # Отправляем запрос
        response = requests.post(
            ML_SERVICE_URL,
            params={"mobile_id": test_data["mobile_id"]},
            json=test_data["item_features"],
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(
                f"Request successful | Mobile ID: {result['mobile_id']} | "
                f"Predicted price range: {result['price_range']}"
            )
        else:
            logger.error(
                f"Request failed | Status: {response.status_code} | "
                f"Response: {response.text}"
            )
            
    except requests.exceptions.ConnectionError:
        logger.error("Connection error: Unable to connect to ML service")
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


def main():
    """Главная функция - бесконечный цикл отправки запросов"""
    logger.info("Starting request service...")
    logger.info(f"Target URL: {ML_SERVICE_URL}")
    
    # Ждем, пока ML сервис поднимется
    time.sleep(5)
    
    request_count = 0
    
    while True:
        try:
            send_request()
            request_count += 1
            
            # Случайная пауза от 0 до 5 секунд
            sleep_time = random.uniform(0, 5)
            logger.info(f"Sleeping for {sleep_time:.2f} seconds... (Total requests: {request_count})")
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            logger.info("\nStopping request service...")
            break


if __name__ == "__main__":
    main()

