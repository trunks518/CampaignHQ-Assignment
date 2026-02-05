# Optimization Changes
* Changed the csv reader to use pandas as this saved ~3-5 seconds in time on larger million record files (About 20% decrease in time).
* Changed frontend to use Tailwind as stated in readme
* Only slightly gave the frontend a facelift (still could be improved)

# Fix
* I noticed the pytest wasnt working and the `__init__` file was missing
* Noticed the readme mentioned tailwind but I did not see it and styling was not workorking so I installed and imported it according to the Tailwind docs