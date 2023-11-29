# sqalchemy-challenge

### Overview
I need a vacation. It's not in the cards right now, but this activity helped me dream. The goal of the exercise was to perform analysis on the weather patterns in Hawaii, using two separate tables in an SQLite database. 

The assignment is broken up into two parts: 1) Data Analysis that pulls data from the SQLite DB, into a Jupyter notebook, and 2) A Flask application that created an API that linked to the data. 

### Part 1: Data Analysis
Data was extracted using SQLite ORM. Multiple queries were run on two tables (measurements and stations) to bring the data into the Jupyter notebook. The queries and their syntax were new, but once the data was present and converted into DataFrames, the analysis followed the same methodology from previous modules. Percipitation and temperature figures (bar and histogram, respectively) were generated from the data. If more time was available, those would be saved and stored to a figures folder within the repo. The requirements did not call for this so it was skipped, this time. 

Functions were paired with the queries to calculate min, max and averages. Another way to get the information would have been to pull in the entire tables and do the calculations using Pandas syntax from previous modules. It was fun learning to do it this way but would most likely utilize Pandas in a work setting. This would ease the code review process. 

### Part 2: Climate App
Once the analysis was complete, Flask was used to create a local API that exposed the data in the form of a JSON API. Queries were again written and Jsonify was used as the final step to expose the data. 

This took the bulk of the development time. Flask is a new tool to me and debugging it required some effort. That said, I can see how it could be incredibly useful for exposing data, especially from custom applications. 

### Conclusion
The code is contained within the 'hang_10' directory in two files: 1) main_scripts.ipynb, and 2) app.py. I was able to run both of them successfully. 

Please reach out if there are issues accessing any of the code. 

