from datetime import datetime

def get_microtime():
    return datetime.utcnow().timestamp() * 1000000