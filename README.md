# cs4400-gttravel

This application is designed to be a database of European cities and countries and various things you can do in them, supported by a robust reviewing system. This webapp is powered by Flask and was developed by Cole Bowers, Varun Gupta, Mehul Mohagaonkar, and Nancy Tao.
This was made for CS4400: Intro to Databases as a final project during a study abroad trip in Barcelona. The theme was inspired by all the travelling we did.

`snapshot.sql` contains the data export of the database. Run this script in MySQL to build the database. 

### Running this webapp
This is currently only supported in Python 2.7. 
```
git clone https://github.com/nancytao/cs4400-gttravel.git
cd cs4400-gttravel
pip install -r requirements.txt 
```
This application expects a `config.py` file in the root directory that contains the password of the root user of your MySQL database setup. You should create this file and write the following in it.
```
password = "your_password"
```
Replace `your_password` with your password. 

Once everything is set up, run `python GTTravel.py` to start a webserver on port 5000. 
