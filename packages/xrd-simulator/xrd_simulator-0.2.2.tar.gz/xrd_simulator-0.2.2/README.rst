.. image:: https://github.com/AxelHenningsson/xrd_simulator/blob/main/docs/source/images/logo.png?raw=true

.. image:: https://img.shields.io/pypi/pyversions/xrd-simulator.svg?
	:target: https://pypi.org/project/xrd-simulator/

.. image:: https://github.com/AxelHenningsson/xrd_simulator/actions/workflows/python-package-conda-linux-py38.yml/badge.svg?
	:target: https://github.com/AxelHenningsson/xrd_simulator/actions/workflows/

.. image:: https://github.com/AxelHenningsson/xrd_simulator/actions/workflows/python-package-conda-macos-py38.yml/badge.svg?
	:target: https://github.com/AxelHenningsson/xrd_simulator/actions/workflows/

.. image:: https://github.com/AxelHenningsson/xrd_simulator/actions/workflows/pages/pages-build-deployment/badge.svg?
	:target: https://github.com/AxelHenningsson/xrd_simulator/actions/workflows/pages/pages-build-deployment/

.. image:: https://badge.fury.io/py/xrd-simulator.svg?
	:target: https://pypi.org/project/xrd-simulator/

.. image:: https://anaconda.org/axiomel/xrd_simulator/badges/installer/conda.svg?
	:target: https://anaconda.org/axiomel/xrd_simulator/

.. image:: https://anaconda.org/axiomel/xrd_simulator/badges/platforms.svg?
	:target: https://anaconda.org/axiomel/xrd_simulator/

.. image:: https://anaconda.org/axiomel/xrd_simulator/badges/latest_release_relative_date.svg?
	:target: https://anaconda.org/axiomel/xrd_simulator/

===================================================================================================
Simulate X-ray Diffraction from Polycrystals in 3D.
===================================================================================================

The **X**-**R** ay **D** iffraction **SIMULATOR** package defines polycrystals as a mesh of tetrahedral single crystals
and simulates diffraction as collected by a 2D discretized detector array while the sample is rocked
around an arbitrary rotation axis.

``xrd_simulator`` was originally developed with the hope to answer questions about measurement optimization in
scanning x-ray diffraction experiments. However, ``xrd_simulator`` can simulate a wide range of experimental
diffraction setups. The essential idea is that the sample and beam topology can be arbitrarily specified,
and their interaction simulated as the sample is rocked. This means that standard "non-powder" experiments
such as `scanning-3dxrd`_ and full-field `3dxrd`_ (or HEDM if you like) can be simulated as well as more advanced
measurement sequences such as helical scans for instance. It is also possible to simulate `powder like`_
scenarios using orientation density functions as input.

===================================================================================================
Documentation
===================================================================================================
Before reading all the boring documentation (`which is hosted here`_) let's dive into some end to end
examples to get us started on a good flavour.

The ``xrd_simulator`` is built around four python objects which reflect a diffraction experiment:

   * A **beam** of xrays (using the ``xrd_simulator.beam`` module)
   * A 2D area **detector** (using the ``xrd_simulator.detector`` module)
   * A 3D **polycrystal** sample (using the ``xrd_simulator.polycrystal`` module)
   * A rigid body sample **motion** (using the ``xrd_simulator.motion`` module)

Once these objects are defined the it is possible to let the **detector** collect scattering of the **polycrystal**
as the sample undergoes the prescribed rigid body **motion** while being illuminated by the xray **beam**.

Let's go ahead and build ourselves some x-rays:

   <beam example goes here>

We will also need to define a detector:

   <detector example goes here>

Next we go ahead and produce a sample:

   <polycrystal example goes here>

And finally we define some motion of the sample over which to integrate the diffraction signal:

   <motion example goes here>

Ok, so now we got ourselves an experimental setup, about time to collect some diffraction:

   <diffract and rendering example goes here>


======================================
Installation
======================================

Anaconda installation
===============================
The preferred way to install the xrd_simulator package is via anaconda::

   conda install -c conda-forge -c axiomel xrd_simulator

This is meant work across OS-systems and requires no prerequisites except, of course,
that of `Anaconda`_ itself.

.. note::
   ``xrd_simulator`` works on python versions =>3.8<3.9. Make sure your conda environment has the right
   python version before installation. For instance, running ``conda install python=3.8`` before 
   installation should ensure correct behavior.

Pip Installation
======================================
Pip installation is possible, however, external dependencies of `pygalmesh`_ must the be preinstalled
on your system. Installation of these will be OS dependent and documentation
`can be found elsewhere.`_::

   pip install xrd-simulator

Source installation
===============================
Naturally one may also install from the sources::

   git clone https://github.com/AxelHenningsson/xrd_simulator.git
   cd xrd_simulator
   python setup.py install

This will then again require the `pygalmesh`_ dependencies to be resolved beforehand.

.. _Anaconda: https://www.anaconda.com/products/individual

.. _pygalmesh: https://github.com/nschloe/pygalmesh

.. _can be found elsewhere.: https://github.com/nschloe/pygalmesh#installation

.. _scanning-3dxrd: https://doi.org/10.1107/S1600576720001016

.. _3dxrd: https://en.wikipedia.org/wiki/3DXRD

.. _powder like: https://en.wikipedia.org/wiki/Powder_diffraction

.. _which is hosted here: https://axelhenningsson.github.io/xrd_simulator/