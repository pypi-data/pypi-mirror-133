import pytest

from supercharge import Charge


def test_pre_init():
    class HelloWorld:
        @Charge
        def __init__(self):
            self.name: str

        @__init__.pre
        def pre_init(self):
            self.name = "Lorem Ipsum"

    assert HelloWorld().name == "Lorem Ipsum"


def test_pre_init_same():
    pass
    # TODO allow for same name like with properties
    # class HelloWorld:
    #     @Charge
    #     def __init__(self):
    #         self.state = True
    #         self.name: str
    #
    #     @__init__.pre
    #     def __init__(self):
    #         self.name = "Lorem Ipsum"
    #
    # assert HelloWorld().state
    # assert HelloWorld().name == "Lorem Ipsum"


def test_post_init():
    class HelloWorld:
        @Charge
        def __init__(self):
            self.name = None

        @__init__.post
        def post_init(self):
            self.name = "Lorem Ipsum"

    assert HelloWorld().name == "Lorem Ipsum"


def test_pre_and_post_init():
    class HelloWorld:
        @Charge
        def __init__(self):
            self.first_name: str
            self.second_name: str

        @__init__.pre
        def pre_init(self):
            self.first_name = "Lorem"

        @__init__.post
        def post_init(self):
            self.second_name = "Ipsum"

    assert HelloWorld().first_name == "Lorem"
    assert HelloWorld().second_name == "Ipsum"


def test_custom_method():
    class HelloWorld:
        def __init__(self):
            self.name = None

        @Charge
        def my_method(self):
            pass

        @my_method.pre
        def pre_my_method(self):
            self.name = "Lorem Ipsum"

    hello_world = HelloWorld()
    hello_world.my_method()
    assert hello_world.name == "Lorem Ipsum"


def test_custom_method_with_kwargs():
    class HelloWorld:
        def __init__(self):
            self.name = None
            self.state = False

        @Charge
        def my_method(self, name):
            self.name = name

        @my_method.pre
        def pre_my_method(self):
            self.state = True

    hello_world = HelloWorld()
    hello_world.my_method(name="Lorem Ipsum")
    assert hello_world.name == "Lorem Ipsum"
    assert hello_world.state


def test_custom_return():
    class HelloWorld:
        def __init__(self):
            self.name = None

        @Charge
        def my_method(self):
            return self.name

        @my_method.pre
        def pre_my_method(self):
            self.name = "Lorem Ipsum"

        @my_method.post
        def post_my_method(self):
            self.name = "dolor sit amet"

    hello_world = HelloWorld()
    assert hello_world.my_method() == "Lorem Ipsum"
    assert hello_world.name == "dolor sit amet"


def test_pre_method_with_kwargs():
    class HelloWorld:
        @Charge
        def __init__(self):
            pass

        @__init__.pre
        def pre_init(self, name):
            pass

    with pytest.raises(TypeError):
        HelloWorld()


def test_post_method_with_kwargs():
    class HelloWorld:
        @Charge
        def __init__(self):
            pass

        @__init__.post
        def post_init(self, name):
            pass

    with pytest.raises(TypeError):
        HelloWorld()


def test_multiple_charges():
    class HelloWorld:
        @Charge
        def __init__(self):
            self.state = False
            self.name = None
            self.run_state = False

        @__init__.post
        def post_init(self):
            self.state = True

        @Charge
        def run(self):
            self.run_state = True

        @run.post
        def post_run(self):
            self.name = "Lorem Ipsum"

    hello_world = HelloWorld()
    hello_world.run()

    assert hello_world.state
    assert hello_world.run_state
    assert hello_world.name == "Lorem Ipsum"


def test_staticmethod():
    # currently, not supported
    pass


def test_pre_decorator():
    # currently, not supported
    pass


def test_apply_decorator():
    # currently, not supported
    pass
