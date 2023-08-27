import glob
import subprocess
import threading

# Initialize a lock object
lock = threading.Lock()


def _sync_internal():
    """
    The internal sync function that performs the actual work.
    This function is intended to be called by the sync() function
    within a thread.
    """
    print("Start sync data")
    image_files = glob.glob("images/*.jpg")
    file_count = len(image_files)
    print(f"Images: {file_count}")

    subprocess.run("wsl sh sync.sh", shell=True)
    print("Done!\n")

    # Release the lock
    lock.release()


def sync():
    """
    The public sync function that is intended to be imported and used.
    """
    global lock

    # Acquire the lock if it's free and proceed, otherwise do nothing
    if lock.acquire(False):  # The 'False' parameter means it won't block
        thread = threading.Thread(target=_sync_internal)
        thread.start()


if __name__ == '__main__':
    sync()
