import threading, signal, time, os

N=10 #change this to change ammount of guests
no_of_students=0
lock_p = threading.Lock()
threads = []
cv_hostess=threading.Condition()
cv_student=threading.Condition()
def openDoor(cv):
    print("Hostess opens doors!")
    with cv:
        cv.notifyAll()

def student_thread(cv,tid, itemId=None, threshold=None):
    global no_of_students
    lock_p.acquire()
    no_of_students+=1
    lock_p.release()
    global N
    print("Student arrives and he's number: ", tid)
    with cv:
        cv.wait()
    print("Student enters house his id is: ", tid)

def hostess_thread(cv,do):
    while no_of_students<N:
        print("Hostess won't let you in yet!")
    openDoor(cv)

    

if __name__ == '__main__':    
    print("Starting all threads...")    
    for i in range(N):
        thread=threading.Thread(target=student_thread, args=(cv_hostess,i,str(i),60))
        thread.start()
        threads.append(thread)

    thread=threading.Thread(target=hostess_thread,args=(cv_hostess,0))
    thread.start()
    threads.append(thread)

    while(no_of_students<N):
        time.sleep(1)

    for thread in threads:
        thread.join()
 
    print("All threads stopped.")