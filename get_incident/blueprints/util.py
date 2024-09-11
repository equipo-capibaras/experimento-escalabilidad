def class_route(self, rule, **options):
    def decorator(cls):
        self.add_url_rule(rule, view_func=cls.as_view(cls.__name__), **options)
        return cls

    return decorator
