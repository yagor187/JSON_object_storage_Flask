import threading
from application import app
from cache import open_file, check_ttl
from application import object_storage


if __name__ == '__main__':
    cleanup_thread = threading.Thread(target=check_ttl, args=(object_storage,))
    cleanup_thread.daemon = True
    cleanup_thread.start()
    app.run(host="0.0.0.0", port=8002, debug=False)
