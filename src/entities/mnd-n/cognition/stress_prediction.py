# src/entities/mnd-n/cognition/stress_prediction.py

from transformers import pipeline


class StressPredictor:

    def __init__(self):

        try:
            self.classifier = pipeline(
                "sentiment-analysis"
            )

            self.available = True

        except Exception as e:

            print(f"[StressPredictor] load failed: {e}")

            self.available = False

    def predict(self, text: str):

        if not self.available:
            return self.rule_based(text)

        result = self.classifier(text)[0]

        label = result["label"].lower()
        score = float(result["score"])

        return self.map_result(label, score)

    def map_result(self, label, score):

        if "negative" in label:
            return {
                "stress": min(score, 1.0),
                "emotion": "anxiety"
            }

        if "positive" in label:
            return {
                "stress": 0.1,
                "emotion": "positive"
            }

        return {
            "stress": 0.3,
            "emotion": "neutral"
        }

    def rule_based(self, text):

        text = text.lower()

        if "불안" in text:
            return {
                "stress": 0.8,
                "emotion": "anxiety"
            }

        if "외롭" in text:
            return {
                "stress": 0.6,
                "emotion": "loneliness"
            }

        return {
            "stress": 0.2,
            "emotion": "neutral"
        }