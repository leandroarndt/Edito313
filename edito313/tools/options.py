_registered = []

# TODO: make options.register() a decorator
def register(option_cls, model_cls):
    global _registered
    
    _registered.append((option_cls, model_cls))
    
    return option_cls
