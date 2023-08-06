<img src="img/logo.png" width="70"> DOLfYN
=======================
![Build](https://github.com/jmcvey3/dolfyn/actions/workflows/build.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/jmcvey3/dolfyn/badge.svg?branch=master)](https://coveralls.io/github/jmcvey3/dolfyn?branch=master)
[![Documentation Status](https://readthedocs.org/projects/dolfyn-xarray/badge/?version=latest)](https://dolfyn-xarray.readthedocs.io/en/latest/?badge=latest)

DOLfYN is the Doppler Oceanography Library for pYthoN.

It is designed to read and work with Acoustic Doppler Velocimeter
(ADV) and Acoustic Doppler Profiler (ADP/ADCP) data. DOLfYN includes
libraries for reading binary Nortek(tm) and Teledyne RDI(tm) data
files.
* Read in binary data files from acoustic Doppler instruments
* Clean data
* Rotate vector data through coordinate systems (i.e. beam - instrument - Earth frames of reference)
* Motion correction for buoy-mounted ADV velocity measurements (via onboard IMU data)
* Bin/ensemble averaging
* Calculate turbulence statistics

Documentation
-------------

For details visit the 
[DOLfYN homepage](https://dolfyn-xarray.readthedocs.io/en/latest/).  

Installation
------------

DOLfYN requires Python 3.6 or later and a number of dependencies. See the 
[install page](https://dolfyn-xarray.readthedocs.io/en/latest/install.html)
for greater details.

License
-------

DOLfYN is copyright through the National Renewable Energy Laboratory, 
Pacific Northwest National Laboratory, and Sandia National Laboratories. 
The software is distributed under the Revised BSD License.
See the [license](LICENSE.txt) for more information.

