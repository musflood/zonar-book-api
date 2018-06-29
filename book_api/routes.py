def includeme(config):
    config.add_route('signup', '/signup')
    config.add_route('book-list', '/books')
    config.add_route('book-id', '/books/{id:\d+}')
