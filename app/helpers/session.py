import redis
import uuid

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def create_session(user_id: int):
    """
    Creates a session for the specified user ID.

    Args:
        user_id (int): The ID of the user for whom the session is being created.

    Returns:
        tuple: A tuple containing the session ID (str) and the user ID (int).
    """

    session_id = str(uuid.uuid4())
    redis_client.set(session_id, user_id)
    redis_client.expire(session_id, 3600)
    return session_id, user_id


def get_user_id_from_session(session_id: str):
    """
    Retrieve the user ID associated with the given session ID from the Redis database.

    Args:
        session_id (str): The session ID for which to retrieve the user ID.

    Returns:
        bytes or None: The user ID associated with the session ID, or None if the session ID is not found.
    """
    return redis_client.get(session_id)
