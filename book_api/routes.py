def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('signup', '/signup')
    config.add_route('book-list', '/books')
    config.add_route('book-id', '/books/{id:\d+}')
