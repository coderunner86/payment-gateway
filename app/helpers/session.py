import redis
import uuid

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def create_session(user_id: int):

    session_id = str(uuid.uuid4())
    redis_client.set(session_id, user_id)
    redis_client.expire(session_id, 3600) 
    return session_id

def get_user_id_from_session(session_id: str):
    return redis_client.get(session_id)

