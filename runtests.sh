#!/bin/bash

# This only works on unix systems

coverage run unittests.py
coverage report server.py invoices.py merchants.py db.py
coverage html controller.py invoices.py merchants.py db.py
