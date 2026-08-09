import requests
import base64
import cv2
import numpy as np

class VisualReasoner:
    def __init__(self, model_name="llava"):
        self.api_url = "http://localhost:11434/api/generate"
        self.model_name = model_name

    def analyze_frame(self, frame, geometric_data):
        """
        이미지와 수치 데이터를 결합하여 시각적 맥락을 분석합니다.
        """
        # 1. 이미지를 base64 문구로 변환 (Ollama API 규격)
        _, buffer = cv2.imencode('.jpg', frame)
        img_str = base64.b64encode(buffer).decode('utf-8')

        # 2. 논문의 M-CoT 기법을 적용한 프롬프트 구성
        prompt = f"""
        당신은 전문 스포츠 코치입니다.
        현재 관절 각도 데이터: {geometric_data}
        
        작업 지침:
        1. 이미지와 수치 데이터를 비교하여 자세의 불일치를 찾으세요.
        2. 발꿈치 들림, 시선 처리, 허리 말림 등 숫자로 알기 어려운 맥락적 문제를 분석하세요.
        3. 분석 결과를 바탕으로 사용자에게 한 문장의 짧고 강렬한 교정 피드백을 한국어로 제공하세요.
        """

        # 3. Ollama 로컬 서버에 요청
        try:
            response = requests.post(self.api_url, json={
                "model": self.model_name,
                "prompt": prompt,
                "images": [img_str],
                "stream": False
            }, timeout=10)
            return response.json().get('response', "").strip()
        except Exception as e:
            return f"비전 분석 오류: {str(e)}"