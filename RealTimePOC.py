import threading
import time

class ScriptThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    
    def run(self):
        FPS = 1
        is_running = True

        tick = time.time()
        loop = 0
        while is_running is True:
            if time.time() >= tick+(1/FPS):
                tick = time.time()
                print(loop)
                time.sleep(1/FPS)
                loop += 1
                if loop >= 10:
                    is_running = False
            else:
                continue

#Make thread
thread = ScriptThread(1, "thread")
thread.start()