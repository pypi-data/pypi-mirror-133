from __future__ import annotations

import functools


class BaseCharge:
    def __init__(self, func, parent=None):
        self._func = func
        self._name = None

    def __repr__(self):
        return f"{self.__class__.__name__}<{self._name}>"

    def __set_name__(self, owner, name):
        self._name = name

    def __call__(self, obj, *args, **kwargs):
        return self._func(obj, *args, **kwargs)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        # TODO add functools.wraps(self._func) somehow
        return functools.partial(self.__call__, obj)


def get_func(obj, name: str):
    """Get the function

    Either from functools.partial or directly a <function>

    Parameters
    ----------
    obj: class instance
    name: name of the function

    Returns
    -------

    function

    """
    try:
        # if partial from previous charger obj
        return getattr(obj, name).func
    except AttributeError:
        return getattr(obj, name)


class Charge(BaseCharge):
    """Main Decorator for the supercharge functionality

    Examples
    --------
    >>> class HelloWorld:
    >>> @Charge
    >>> def run(self):
    >>>     # do something
    >>> @run.pre
    >>> def pre_run(self):
    >>>     # do something before run
    >>> @run.post
    >>> def post_run(self):
    >>>     # do something after run

    """

    def __init__(self, func):
        """Constructor of the Charge decorator

        Parameters
        ----------
        func: The charged function
        """
        super(Charge, self).__init__(func)
        self._pre_func = None
        self._post_func = None

        self._force_pre = False
        self._force_post = False

    @classmethod
    def _from_charge(cls, charger: Charge, obj) -> Charge:
        """Create a new charge object for class inheritance

        Parameters
        ----------
        charger: Charge
            A charge object from the parent class
        obj: class type of the child class (not instance!)

        Returns
        -------
        new charge object
        """
        new_charger = cls(get_func(obj, charger._name))

        if charger._pre_func is not None:
            new_charger._pre_func = get_func(obj, charger._pre_func._name)

        if charger._post_func is not None:
            new_charger._post_func = get_func(obj, charger._post_func._name)

        return new_charger

    def __call__(self, obj, *args, **kwargs):
        """Function Call

        Parameters
        ----------
        obj: instance of the function
        args
        kwargs

        Returns
        -------
        the return value of the charged function

        """
        if self._pre_func is not None:
            try:
                self._pre_func(obj)
            except TypeError:
                raise TypeError(
                    f"Method {self._pre_func} can not take keyword arguments!"
                )
        parsed_func = self._func(obj, *args, **kwargs)
        if self._post_func is not None:
            try:
                self._post_func(obj)
            except TypeError:
                raise TypeError(
                    f"Method {self._post_func} can not take keyword arguments!"
                )
        return parsed_func

    def pre(self, func):
        """Add a function to be called before the charged object

        Parameters
        ----------
        func: Callable
            Any function to run before the charged object

        Returns
        -------
        Returns the function
        """
        self._pre_func = BaseCharge(func)
        return self._pre_func

    def post(self, func):
        """Add a function to be called after the charged object

        Parameters
        ----------
        func: Callable
            Any function to run after the charged object

        Returns
        -------
        Returns the function
        """
        self._post_func = BaseCharge(func)
        return self._post_func
