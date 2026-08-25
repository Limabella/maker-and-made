import requests

def ask_ollama(prompt, model="llama3.1"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    return data.get("response", "")

    if __name__ == "__main__":

        answer = ask_ollama("안녕, 너는 누구니?")

        print(answer)

# 다른 터미널에서 아래 명령어 사용시 상태 확인
# curl http://localhost:11434
