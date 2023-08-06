#####################
dual tape ez - v1.0.0
#####################

*****
About
*****
This python module "dual_tape_ez" is an `Esolang <https://esolangs.org/wiki/Main_Page>`_.

*******************
Python Installation
*******************
.. code-block:: bash

   pip install dual_tape_ez

*****************
Console Interface
*****************
.. code-block:: bash

   dual_tape_ez hello_world.dte

.. code-block:: text

   dual_tape_ez

   positional arguments:
     file           path to dual_tape_ez script

   optional arguments:
     -h, --help     show this help message and exit
     -a, --author   get author of dual_tape_ez
     -v, --version  get version of dual_tape_ez
     -l, --log      enables debug log
     --timeout TIMEOUT  max number of instructions that can run

*************
Documentation
*************
* `Documentation <https://esolangs.org/wiki/dual_tape_ez>`_
* `Raw Documentation <https://github.com/cmcmarrow/dual_tape_ez/blob/master/DOCUMENTATION.txt>`_

****************
Build Executable
****************
.. code-block:: bash

   git clone https://github.com/cmcmarrow/dual_tape_ez.git
   pip install -e .[dev]
   python build.py

***
API
***
``dual_tape_api.py``

.. code-block:: text

   info: API to dual_tape_ez
   :param: inputs: Optional[Union[Tuple[str, ...], List[str]]]
   :param: sys_output: bool
   :param: catch_output: bool
   :param: log: bool
   :return: Generator[vm.VMState, None, None]
