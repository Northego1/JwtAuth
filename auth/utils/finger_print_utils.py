import hashlib

from fastapi import Request



def get_finger_print_hash(request: Request) -> str:
    user_agent = request.headers.get('user-agent')
    hash_value = hashlib.sha256(user_agent.encode()).hexdigest()
    return hash_value




