PyFrx
=====

A package to help convert currencies.


Details
-------

Simply, this package relies on current forex market rate to check conversion.


Package Usage
-------------

import pyfx

\# show supported currencies
pyfx.supported_currencies()

\# to just get the rate 
pyfx.rate('gbp','pkr')

\# to get amount conversion
pyfx.convert('gbp', 'pkr', 10)
