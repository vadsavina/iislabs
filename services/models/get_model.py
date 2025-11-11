import mlflow
import cloudpickle as pkl

# Работаем с MLflow локально
TRACKING_SERVER_HOST = "127.0.0.1"
TRACKING_SERVER_PORT = 5001

registry_uri = f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}"
tracking_uri = f"http://{TRACKING_SERVER_HOST}:{TRACKING_SERVER_PORT}"

mlflow.set_tracking_uri(tracking_uri)   
mlflow.set_registry_uri(registry_uri)   

# Загружаем последнюю Production модель по алиасу
MODEL_NAME = 'estate_model_rf'
loaded_model = mlflow.sklearn.load_model(f'models:/{MODEL_NAME}@production')

with open('model.pkl', 'wb') as f:
    pkl.dump(loaded_model, f)