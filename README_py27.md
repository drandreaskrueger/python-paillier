# python 2.7 backport attempt

(incomplete!) 

### disclaimer
Our time was very limited, so we stopped when our tests went through fine, so:

* might be incorrect.
* is definitely incomplete.

Please continue from here, and keep us in the loop, thanks:

* [https://github.com/drandreaskrueger](https://github.com/drandreaskrueger)
* [https://github.com/zlevas](https://github.com/zlevas)


### preparations

    sudo apt-get install python-virtualenv
    virtualenv env
    source env/bin/activate
    pip install pytest tox numpy click gmpy2
    

### run tests 

via tox = makes sure that python 2.7 is used:

    tox -e py27 -- -x -v tests/test_homomorphic_encryption.py

or with:

    pytest -v -k homomorphic_encryption




### history

we have changed these files:

* phe/\_\_init\_\_.py
* phe/paillier.py
* phe/command_line.py

we have added these files:

* phe/tests/homomorphic_encryption.py
* phe/tests/test_homomorphic_encryption.py
* tox.ini
* README_py27.md


## python 3

original [README.rst](README.rst)

