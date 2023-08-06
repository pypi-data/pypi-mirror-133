import logging

from supercharge.charge import Charge

log = logging.getLogger(__name__)


class Base:
    """Base class to enforce pre/post with class inheritance

    Examples
    --------

    >>> class Parent(Base):
    >>> @Charge
    >>> def run(self):
    >>>     raise NotImplementedError
    >>> @run.post
    >>> def post_run(self):
    >>>     # do something after run in the child class
    >>>  class Child(Parent):
    >>>     def run(self):
    >>>         # do something
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__bases__:
            for name, obj in vars(base).items():
                if isinstance(obj, Charge):
                    setattr(cls, name, Charge._from_charge(obj, cls))
