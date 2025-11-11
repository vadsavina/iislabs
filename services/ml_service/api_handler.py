import logging
import os
import pandas as pd
import cloudpickle as pkl

logger = logging.getLogger("uvicorn.error")


class FastAPIHandler:
    
    def __init__(self):
        logger.warning('Loading model...')
        
        # Определяем путь относительно текущего файла
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Проверяем оба пути: Docker (/models) и локальный (относительно api_handler.py)
        docker_path = '/models/model.pkl'
        local_path = os.path.join(current_dir, '..', 'models', 'model.pkl')
        local_path = os.path.abspath(local_path)
        
        model_path = docker_path if os.path.exists(docker_path) else local_path
        
        if not os.path.exists(model_path):
            error_msg = f'Model file not found. Checked paths:\n  - {docker_path}\n  - {local_path}\nPlease run get_model.py first to download the model.'
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            self.model = pkl.load(open(model_path, 'rb'))
            logger.info(f'Model is loaded from {model_path}')
        except Exception as e:
            logger.error(f'Error loading model from {model_path}: {e}')
            raise

    def predict(self, item_features: dict):
        item_df = pd.DataFrame(data=item_features, index=[0])
        prediction = self.model.predict(item_df)
        return prediction