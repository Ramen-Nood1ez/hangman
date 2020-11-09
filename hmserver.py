# Hang Man Server program
import socket
import sys
import logging
import re
import os.path
import time
import threading, queue
import tkinter as tk


runServer = True
q = queue.Queue()
logclientip = False


def mainServer():
    words = []
    hmwordsfile = "hmwords.csv"
    if os.path.exists("hmwords.csv"):
        file = open("hmwords.csv", "r")
        for x in file:
            words.append(re.sub(r"\n", "", x))
        # print(words)
        file.close()
    else:
        logging.critical("%s doesn't exist, aborting", hmwordsfile)
        print("An error has occurred... look at the log for details...")
        sys.exit(-1)
    logging.info("Main Server: starting")
    q.task_done()
    Host = ""
    Port = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((Host, Port))
    s.listen(1)
    while runServer:
        client_num = 0
        item = q.get()
        try:
            conn, addr = s.accept()
            if logclientip: logging.info("%s: connected", addr)
            else:
                client_num = client_num + 1
                logging.info("Client #%s: connected", client_num)
            # print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    if logclientip: logging.info("%s: disconnected", addr)
                    else: logging.info("Client %s: disconnected", client_num)
                    if not q.empty():
                        q.task_done()
                        q.put(addr)
                    break
                logging.info("%s sent: %a", addr, re.sub("b*'", "", repr(data)))
                if repr(data) == "b'getwords'":
                    sendwords = ""
                    for x in words:
                        if sendwords == "":
                            sendwords = words[0] + ", "
                        else:
                            sendwords = sendwords + x + ", "
                    conn.sendall(b'Here are the words: ' + bytes(sendwords, encoding="utf-8"))
                    q.put(addr)
                elif repr(data) == "b'addwords'":
                    pass
                else:
                    conn.sendall(bytes(data) + b' is not a valid option...')
                    logging.warning("%s sent: %a, which isn't a valid option", addr, repr(data))
                    break
                # conn.sendall(data)
            conn.close()
        except KeyboardInterrupt:
            logging.info("Main Server: stopping")
            q.task_done()
            sys.exit(0)
        except ConnectionResetError:
            pass
    logging.info("Main Server: stopped")


def pre_init():
    if os.path.exists("latest.log"):
        localtime = time.localtime()
        time_str = time.strftime("%m-%d-%Y", localtime)
        if os.path.exists(time_str + "-1.log"):
            i = 2
            while True:
                if os.path.exists(time_str + "-" + str(i) + ".log"):
                    i = i + 1
                    continue
                else:
                    os.rename(r"latest.log", (time_str + "-" + str(i) + ".log"))
                    break
        else:
            os.rename(r"latest.log", (time_str + "-1.log"))
    format = "%(levelname)s %(asctime)s: %(message)s"
    logging.basicConfig(filename="latest.log", level=logging.DEBUG, format=format, datefmt="%H:%M:%S")
    try:
        mainServer()
    except:
        logging.exception(sys.exc_info())


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        var1 = tk.IntVar()

    def create_widgets(self):
        self.start_server = tk.Button(self)
        self.start_server["text"] = "Start Server"
        self.start_server["command"] = self.startserver
        self.start_server.pack(side="top")

        self.stop_server = tk.Button(self)
        self.stop_server["text"] = "Stop Server"
        self.stop_server["command"] = self.stopserver
        self.stop_server.pack(side="top")

        self.logclientip = tk.Checkbutton(root, text="Log Client Ip's", command=self.togglevar)
        self.logclientip.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.quit_app)
        self.quit.pack(side="bottom")

    @staticmethod
    def startserver():
        global runServer
        runServer = True
        threading.Thread(target=pre_init, daemon=True).start()
        q.put_nowait(1)
        # q.join()

    @staticmethod
    def stopserver():
        global runServer
        runServer = False

    def quit_app(self):
        global runServer
        if runServer:
            runServer = False
        self.master.destroy()

    def togglevar(self):
        global logclientip
        logclientip = not logclientip


root = tk.Tk()
root.title("Hangman Word Server")
root.geometry("100x100")
app = Application(master=root)
app.mainloop()
