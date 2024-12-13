import sys
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import os
import datetime


id = 0

dic = {
    "ID": None,
    "Olay": None,
    "Tarih": None,
    "Dosya_Yolu": None
}
diclist = []

def changer(type):
    print("changer")
    if type == "1":
        dic["Olay"] = "Dosya oluşturuldu."
    elif type == "2":
        dic["Olay"] = "Dosya değiştirildi."
    elif type == "3":
        dic["Olay"] = "Dosya silindi."
    elif type == "4":
        dic["Olay"] = "Dosya taşındı"


def jsoned(path):
    global id

    now = datetime.datetime.now()
    dic_copy = dic.copy()  
    dic_copy["ID"] = id  
    dic_copy["Tarih"] = now.strftime("%d-%m-%Y %H:%M:%S") + "." + str(now.microsecond)[:3]
    dic_copy["Dosya_Yolu"] = path
    id += 1  
    diclist.append(dic_copy)  
    jstring = json.dumps(diclist, ensure_ascii=False)

    with open(r"D:\Yazilim\Python\PythonWritten\BilisimAltyapi\logfile.json", "w", encoding="utf-8") as file:
        file.write(jstring)
    
    #silinebilir
    for i in diclist:
        print(i)


class MyHandler(LoggingEventHandler):
    def __init__(self):
        self.last_modified_time = datetime.datetime.now()  

    def on_created(self, event):
        print("\n\n\nDosya Oluşturuldu\n\n\n")
        changer("1")
        jsoned(event.src_path)

    def on_modified(self, event):

        time_diff = datetime.datetime.now() - self.last_modified_time
        if time_diff.total_seconds() < 1:  
            return
        print("\n\n\nDosya Değiştirildi\n\n\n")
        changer("2")
        jsoned(event.src_path)
        self.last_modified_time = datetime.datetime.now()  

    def on_deleted(self, event):
        print("\n\n\nDosya Silindi\n\n\n")
        changer("3")
        jsoned(event.src_path)

    def on_moved(self, event):
        print("\n\n\nDosya Taşındı\n\n\n")
        changer("4")
        jsoned(event.src_path)
        self.last_modified_time = datetime.datetime.now()  


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = "Dosya"  # Silinecek

    if not os.path.exists(path):
        print(f"Error: The path {path} does not exist.")
        sys.exit(1)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        print(f"Observing changes in: {path}")
        while observer.is_alive():
            print("observer")
            print("Len: ", len(diclist))
            observer.join(1)
    except KeyboardInterrupt:
        print("Process interrupted.")
    finally:
        observer.stop()
        observer.join()
