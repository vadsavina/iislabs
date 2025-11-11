from fastapi import FastAPI, Response
from api_handler import FastAPIHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, REGISTRY, generate_latest, CONTENT_TYPE_LATEST
import uvicorn

app = FastAPI()
handler = FastAPIHandler()

# Метрика histogram для предсказаний модели
prediction_histogram = Histogram(
    'model_predictions',
    'Histogram of model price range predictions',
    buckets=[0, 1, 2, 3, 4],
    registry=REGISTRY
)

# Подключаем Prometheus instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app)


@app.get('/metrics')
def metrics():
    """Endpoint для метрик Prometheus"""
    return Response(content=generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)


@app.get('/')
def root_dir():
    return {'Hello': 'World'}


@app.post('/api/prediction')
def make_prediction(mobile_id: int, item_features: dict):
    prediction = handler.predict(item_features)[0]
    prediction_value = int(prediction)
    
    # Записываем предсказание в histogram
    prediction_histogram.observe(prediction_value)
    
    return {
        'mobile_id': mobile_id,
        'price_range': prediction_value
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)