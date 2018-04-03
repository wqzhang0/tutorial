from rest_framework.throttling import AnonRateThrottle


class MyThrottle(AnonRateThrottle):
    scope = 'test_model'
    # cache = get_cache('alternate')
