
def fatal_error(msg:str):
    raise Exception(msg)


def assert_never(x,msg:str):
    raise Exception(msg)