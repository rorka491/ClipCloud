from src.dependency.factory import rate_limiter_factory


ws_chat_rate_limit = rate_limiter_factory('ws', 10, 5)
create_room_rate_limit = rate_limiter_factory('create_room', 10, 5)
get_room_rate_limit = rate_limiter_factory('get_room', 10, 5)