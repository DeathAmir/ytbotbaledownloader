import os, requests, re, subprocess, json, time

TOKEN=os.getenv("BALE_TOKEN")
BASE="https://tapi.bale.ai/bot"+TOKEN+"/"

def get_updates(offset=None):
    r=requests.get(BASE+"getUpdates",params={"offset":offset})
    return r.json()["result"]

def send_message(chat_id,text):
    requests.post(BASE+"sendMessage",json={"chat_id":chat_id,"text":text})

def send_video(chat_id,path):
    files={"video":open(path,"rb")}
    requests.post(BASE+"sendVideo",data={"chat_id":chat_id},files=files)

def download_youtube(url,output):
    subprocess.run(["yt-dlp","-f","best","-o",output,url],check=True)

def run():
    last=None
    while True:
        updates=get_updates(last)
        for u in updates:
            last=u["update_id"]+1
            msg=u.get("message",{})
            cid=msg.get("chat",{}).get("id")
            text=msg.get("text","")
            if re.match(r'^https?://(www\.)?youtube\.com|youtu\.be',text):
                send_message(cid,"دانلود در حال انجامه...")
                try:
                    output="/tmp/video.mp4"
                    download_youtube(text,output)
                    send_video(cid,output)
                    send_message(cid,"تمام شد ✅")
                except Exception as e:
                    send_message(cid,str(e))
        time.sleep(3)

if __name__=="__main__":
    run()
