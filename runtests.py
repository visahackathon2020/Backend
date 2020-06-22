#!/bin/bash

# This only works on unix systems

coverage run unittests.py
coverage report controller.py
coverage html controller.py
