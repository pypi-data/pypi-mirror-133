from supercharge import Base, Charge


def test_subclass_no_super():
    class Parent(Base):
        @Charge
        def __init__(self):
            self.name = None

        @__init__.post
        def post_init(self):
            self.name = "Lorem Ipsum"

    class Child(Parent):
        pass

    assert Child().name == "Lorem Ipsum"


def test_subclass_with_super():
    class Parent(Base):
        @Charge
        def __init__(self):
            self.name = None

        @__init__.post
        def post_init(self):
            self.name = "Lorem Ipsum"

    class Child(Parent):
        def __init__(self):
            super(Child, self).__init__()

    assert Child().name == "Lorem Ipsum"


def test_subclass_without_super():
    class Parent(Base):
        def __init__(self):
            self.pre_state = False
            self.post_state = False

        @Charge
        def run(self):
            pass

        @run.pre
        def pre_run(self):
            self.pre_state = True

        @run.post
        def post_run(self):
            self.post_state = True

    class Child(Parent):
        def run(self):
            print("Hello World")

    child = Child()
    child.run()
    assert child.pre_state
    assert child.post_state


def test_subclass_without_pre_post():
    class Parent(Base):
        def __init__(self):
            self.state = False

        @Charge
        def run(self):
            pass

    class Child(Parent):
        def run(self):
            self.state = True

    child = Child()
    child.run()
    assert child.state


def test_subclass_not_implemented():
    class Parent(Base):
        def __init__(self):
            self.state = False

        @Charge
        def run(self):
            raise NotImplementedError

        @run.post
        def post_run(self):
            self.state = True

    class Child(Parent):
        def run(self):
            pass

    child = Child()
    child.run()
    assert child.state
