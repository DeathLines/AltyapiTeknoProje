import sys
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import os
import datetime

# Bilgisayarın yerel tarih ve saatini al
now = datetime.datetime.now()

# Gün, ay, yıl ve saati belirli bir formatta yazdır
formatted_time = now.strftime("%d-%m-%Y %H:%M:%S")




dic = {
    "FilePath" : None,
    "Date" : now.strftime("%d-%m-%Y %H:%M:%S"),
    "Event" : None
}

def changer(type,path):
    print("changer")
    if type == "1":
        dic["Event"] = "Dosya oluşturuldu."
        dic["FilePath"] = path
    elif type == "2":
        dic["Event"] = "Dosya değiştirildi."
        dic["FilePath"] = path
    elif type == "3":
        dic["Event"] = "Dosya silindi."
        dic["FilePath"] = path
    elif type == "4":
        dic["Event"] = "Dosya taşındı"
        dic["FilePath"] = path


def jsoned():
    with open("logfile.log","w+",encoding="utf-8") as file:
        jstring = json.dumps(dic)
        print("jstring: " +jstring)
        file.writelines(jstring)


class MyHandler(LoggingEventHandler):
    def on_created(self, event):
        print("created")
        changer("1",event.src_path)
        jsoned()

    def on_modified(self, event):
        changer("2",event.src_path)
        jsoned()

    def on_deleted(self, event):
        changer("3",event.src_path)
        jsoned()

    def on_moved(self, event):
        changer("4",event.src_path)
        jsoned()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'  

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
            observer.join(1)
    except KeyboardInterrupt:
        print("Process interrupted.")
    finally:
        observer.stop()
        observer.join()