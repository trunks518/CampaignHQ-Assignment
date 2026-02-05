# Optimization Changes
* Changed the csv reader to use pandas as this saved ~3-5 seconds on larger million record files.

# Fix
* I noticed the pytest wasnt working and the `__init__` file was missing