from fastapi import FastAPI
from api_handler import FastAPIHandler
import uvicorn

app = FastAPI()
handler = FastAPIHandler()


@app.get('/')
def root_dir():
    return {'Hello': 'World'}


@app.post('/api/prediction')
def make_prediction(mobile_id: int, item_features: dict):
    prediction = handler.predict(item_features)[0]
    
    return {
        'mobile_id': mobile_id,
        'price_range': int(prediction)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)