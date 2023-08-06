|build| |license| |code style| |coverage|

Supercharge
-----------

This package allows you to automatically run code before and after a given class method.
Furthermore, this behaviour can be enforced on child classes as well.

Example
=======

.. code-block:: py

    from supercharge import Charge

    class HelloWorld:
        def __init__(self):
            self.run_prepared = False
            self.run_state = False

        @Charge
        def run(self):
            if self.run_prepared:
                print("running ...")

        @run.pre
        def pre_run(self):
            self.run_prepared = True

        @run.post
        def post_run(self):
            self.run_state = True


If this is behaviour is desired in subclassed runs one must use the `Base` class.

.. code-block:: py

    from supercharge import Charge, Base

    class HelloWorld(Base):
        def __init__(self):
            self.run_prepared = False
            self.run_state = False

        @Charge
        def run(self):
            raise NotImplementedError

        @run.pre
        def pre_run(self):
            self.run_prepared = True

        @run.post
        def post_run(self):
            self.run_state = True

    class Child(HelloWorld):
        def run(self):
            if self.run_prepared:
                print("running ...")

.. badges

.. |build| image:: https://github.com/zincware/supercharge/actions/workflows/pytest.yaml/badge.svg
    :alt: Build tests passing
    :target: https://github.com/zincware/py-test/blob/readme_badges/


.. |license| image:: https://img.shields.io/badge/License-EPL-purple.svg?style=flat
    :alt: Project license
    :target: https://www.eclipse.org/legal/epl-2.0/faq.php

.. |code style| image:: https://img.shields.io/badge/code%20style-black-black
    :alt: Code style: black
    :target: https://github.com/psf/black/
    
.. |coverage| image:: https://coveralls.io/repos/github/zincware/supercharge/badge.svg
    :alt: Code coverage
    :target: https://coveralls.io/github/zincware/supercharge