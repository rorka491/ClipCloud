from src.dependency.factory import rate_limiter_factory



create_room_rate_limit = rate_limiter_factory('create_room', 10, 5)
get_room_rate_limit = rate_limiter_factory('get_room', 10, 5)
get_history_rate_limit = rate_limiter_factory('hisotry', 10, 5)
default_rate_limit = rate_limiter_factory('default', 10, 5, test_mode=True)