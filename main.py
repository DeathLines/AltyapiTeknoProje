import sys
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import os
import datetime




id = 0
if_added = False
dic = {"ID": None, "Olay": None, "Tarih": None, "Dosya_Yolu": None}
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
        dic["Olay"] = "Dosya tasindi veya ismi degistirildi."


def jsoned(path):
    global id, diclist, if_added
    
    now = datetime.datetime.now()
    dic_copy = dic.copy()
    dic_copy["ID"] = id
    dic_copy["Tarih"] = (
        now.strftime("%d-%m-%Y %H:%M:%S") + "." + str(now.microsecond)[:3]
    )

    dic_copy["Dosya_Yolu"] = path
    id += 1
    diclist.append(dic_copy)
    jstring = json.dumps(diclist, ensure_ascii=False)
    # diclist = [a,b,a]

    try:

        with open("D:\Yazilim\Python\PythonWritten\BilisimAltyapi\log.json", "a+", encoding="utf-8") as file:
            # "/home/ubuntu/bsm/logs/logfile.json"
            # "D:\Yazilim\Python\PythonWritten\BilisimAltyapi\log.json"

                #  file = [a]
                #  data = [a]
                #  if_added = False
            print("\n\n\TRY\n\n\n")
            file.seek(0)
            data = json.load(file)
            
            if not if_added:

                diclist = diclist + data
                if_added = True
                
            jstring = json.dumps(diclist, ensure_ascii=False)
            print("Tip:", type(data))
            print("Data:", data)
            file.seek(0)
            file.truncate()
            file.write(jstring)
            print("JSTRING",jstring)
    except (json.JSONDecodeError, FileNotFoundError):
        print("\n\n\EXCEPT\n\n\n")
        
        with open("D:\Yazilim\Python\PythonWritten\BilisimAltyapi\log.json", "w", encoding="utf-8") as file:
            # "/home/ubuntu/bsm/logs/logfile.json"
            # "D:\Yazilim\Python\PythonWritten\BilisimAltyapi\log.json"
            file.write(jstring)
            # [a]

    # silinebilir

    for i in diclist:
        print(i)


class MyHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_modified_time = datetime.datetime.now()

    def on_created(self, event):
        print("\n\n\nDosya Olusturuldu\n\n\n")
        changer("1")
        jsoned(event.src_path)
        self.last_modified_time = datetime.datetime.now()
        
    def on_modified(self, event):
        time_diff = datetime.datetime.now() - self.last_modified_time
        
        if time_diff.total_seconds() < 1:
            return

        print("\n\n\nDosya Degistirildi\n\n\n")
        changer("2")
        jsoned(event.src_path)
        self.last_modified_time = datetime.datetime.now()

    def on_deleted(self, event):

        print("\n\n\nDosya Silindi\n\n\n")
        changer("3")
        jsoned(event.src_path)
        self.last_modified_time = datetime.datetime.now()

    def on_moved(self, event):

        print("\n\n\nDosya Tasindi\n\n\n")
        changer("4")
        jsoned(event.src_path)
        self.last_modified_time = datetime.datetime.now()


if __name__ == "__main__":

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    # path = "Dosya"  # Silinecek
    path = r"D:\Yazilim\Python\PythonWritten\BilisimAltyapi\Dosya"
    # "/home/ubuntu/bsm/test"
    # r"D:\Yazilim\Python\PythonWritten\BilisimAltyapi\Dosya"
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
