import sys
import logging
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import os



log_file_path = r'logfile.log'
log = logging.getLogger(__name__)
holder = ""
# logging.basicConfig(filename=holder, level=logging.INFO, format='%(asctime)s tarihinde şu konumda %(message)s')

logging.basicConfig(filename="logfile.log", level=logging.INFO, format='{"Tarih": "%(asctime)s","Konum": "%(message)s"}')


def jsoned():
    print("holder: " +holder)
    with open("logfile.log","w+",encoding="utf-8") as file:
        jstring = json.dumps(holder)
        print("jstring: " +jstring)
        file.writelines(jstring)

# logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# class MyHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         if not event.is_directory:
#             logging.info(f"File modified: {event.src_path}")

#     def on_created(self, event):
#         if not event.is_directory:
#             logging.info(f"File created: {event.src_path}")

#     def on_deleted(self, event):
#         if not event.is_directory:
#             logging.info(f"File deleted: {event.src_path}")

class MyHandler(LoggingEventHandler):
    
    def on_created(self, event):
        # print(super().on_created(event))
        logging.info(f"dosya oluşturuldu: {event.src_path}")
        jsoned()
    def on_modified(self, event):
        logging.info(f"dosya modifiye edildi: {event.src_path}")
    def on_deleted(self, event):
        logging.info(f"dosya silindi: {event.src_path}")
    def on_moved(self, event):
        logging.info(f"dosya silindi: {event.src_path}")


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
            observer.join(1)
    except KeyboardInterrupt:
        print("Process interrupted.")
    finally:
        observer.stop()
        observer.join()