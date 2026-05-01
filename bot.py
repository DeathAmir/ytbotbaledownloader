import os, requests, time

BALE_TOKEN = os.getenv("BALE_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")
BASE = f"https://tapi.bale.ai/bot{BALE_TOKEN}/"
CHAT_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
IMG_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
PROMPT = "You are Kora, an intelligent assistant. "

def send_req(method, data, files=None):
    return requests.post(BASE + method, data=data, files=files, json=data if not files else None)

def get_updates(offset=None):
    r = requests.get(BASE + "getUpdates", params={"offset": offset})
    return r.json().get("result", [])

def chat(text):
    r = requests.post(CHAT_URL, headers=HEADERS, json={"inputs": f"{PROMPT} {text}"})
    return r.json()[0]["generated_text"].split("[/INST]")[-1]

def gen_img(text):
    r = requests.post(IMG_URL, headers=HEADERS, json={"inputs": text})
    return r.content

def run():
    offset = None
    while True:
        updates = get_updates(offset)
        for u in updates:
            offset = u["update_id"] + 1
            cid = u["message"]["chat"]["id"]
            txt = u["message"].get("text", "")
            if txt == "/start":
                send_req("sendMessage", {"chat_id": cid, "text": "کورا بارگذاری شد. سوال خود را بپرسید."})
            elif txt.startswith("/img "):
                img = gen_img(txt[5:])
                send_req("sendPhoto", {"chat_id": cid}, files={"photo": ("img.png", img)})
            else:
                send_req("sendMessage", {"chat_id": cid, "text": chat(txt)})
        time.sleep(2)

if __name__ == "__main__":
    run()
