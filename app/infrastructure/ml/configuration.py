from app.infrastructure.ml.model.model import GoldPredictor

# This is the place where a machine learning model will be configured,
# after I write a regression selection model picker?


# klasa z metodami (predict, train) dzialajaca tylko dla pojedynczych walut lub zlota.
# request: https://localhost:3000/USD/predict/?date=2023-10-10
# request: https://localhost:3000/gold/predict/?date=2023-10-10
# if date <= date.today(): return nbp request
# if date > date.today(): return model prediction


gold_predictor = GoldPredictor()
