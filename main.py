import sys
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import datetime




id = 0
if_added = False
dic = {"ID": None, "Olay": None, "Tarih": None, "Eski_Dosya_Yolu": None,"Yeni_Dosya_Yolu":None}
diclist = []


def changer(type):

    print("changer")
    if type == "1":
        dic["Olay"] = "Dosya olusturuldu."
    elif type == "2":
        dic["Olay"] = "Dosya degistirildi."
    elif type == "3":
        dic["Olay"] = "Dosya silindi."
    elif type == "4":
        dic["Olay"] = "Dosya ismi veya konumu degistirildi."


def jsoned(path,npath):
    global id, diclist, if_added
    
    now = datetime.datetime.now()
    dic_copy = dic.copy()
    dic_copy["ID"] = id
    dic_copy["Tarih"] = (
        now.strftime("%d-%m-%Y %H:%M:%S") + "." + str(now.microsecond)[:3]
    )

    dic_copy["Eski_Dosya_Yolu"] = path
    dic_copy["Yeni_Dosya_Yolu"] = npath
    id += 1
    diclist.append(dic_copy)
    jstring = json.dumps(diclist, ensure_ascii=False)

    try:

        with open("/home/ubuntu/bsm/logs/logfile.json", "a+", encoding="utf-8") as file:

            file.seek(0)
            data = json.load(file)
            
            if not if_added:

                diclistcopy = diclist.copy()
                diclist.clear()
                
                for i in data:
                    
                    if i in diclistcopy:
                        continue
                    
                    diclist.append(i)
                diclist = diclist + diclistcopy
                if_added = True               
            jstring = json.dumps(diclist, ensure_ascii=False)
            file.seek(0)
            file.truncate()
            file.write(jstring)

    except (json.JSONDecodeError, FileNotFoundError):        
        with open("/home/ubuntu/bsm/logs/logfile.json", "w", encoding="utf-8") as file:
            file.write(jstring)



class MyHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_modified_time = datetime.datetime.now()

    def on_created(self, event):
        changer("1")
        jsoned(event.src_path,event.dest_path)
        self.last_modified_time = datetime.datetime.now()
        
    def on_modified(self, event):
        time_diff = datetime.datetime.now() - self.last_modified_time
        
        if time_diff.total_seconds() < 1:
            return

        changer("2")
        jsoned(event.src_path,event.dest_path)
        self.last_modified_time = datetime.datetime.now()

    def on_deleted(self, event):

        changer("3")
        jsoned(event.src_path,event.dest_path)
        self.last_modified_time = datetime.datetime.now()

    def on_moved(self, event):

        changer("4")
        jsoned(event.src_path,event.dest_path)
        self.last_modified_time = datetime.datetime.now()


if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    path = "/home/ubuntu/bsm/test"

    if not os.path.exists(path):
        print(f"Hata: Klasör: {path} bulunmuyor.")
        sys.exit(1)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:

        print(f"İzlenen konum: {path}")
        while observer.is_alive():
            observer.join(1)

    except KeyboardInterrupt:
        print("Süreç bozuldu.")

    finally:
        observer.stop()
        observer.join()
