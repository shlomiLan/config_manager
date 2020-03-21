from invoke import Context

from ..tasks import set_vars


def runner():
    context = Context()
    set_vars(context)
    print("Hello World!")


if __name__ == "__main__":
    runner()
