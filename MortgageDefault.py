# -*- coding: utf-8 -*-
"""
	Default Mortgage Predictions
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	An example web application for making predicions using a saved WLM model
	using Flask and the IBM WLM APIs.

	Created by Rich Tarro
	May 2017
"""

import os, urllib3, requests, json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/MortgageDefault'
#postgres://admin:XZLNWWMRNZHWXOCK@bluemix-sandbox-dal-9-portal.8.dblayer.com:26360/mydb
db = SQLAlchemy(app)

class mortgagedefault(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	FirstName = db.Column(db.String(20))
	LastName = db.Column(db.String(20))
	Income = db.Column(db.Integer)
	AppliedOnline = db.Column(db.String(3))
	Residence = db.Column(db.String(20))
	YearCurrentAddress = db.Column(db.Integer)
	YearsCurrentEmployer = db.Column(db.Integer)
	NumberOfCards = db.Column(db.Integer)
	CCDebt = db.Column(db.Integer)
	Loans = db.Column(db.Integer)
	LoanAmount = db.Column(db.Integer)
	SalePrice = db.Column(db.Integer)
	Location = db.Column(db.Integer)
	prediction = db.Column(db.Numeric)
	probability = db.Column(db.Numeric)
	
	def __init__(self, FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location,
		prediction, probability):
		self.FirstName = FirstName
		self.LastName = LastName
		self.Income = Income
		self.AppliedOnline = AppliedOnline
		self.Residence = Residence
		self.YearCurrentAddress = YearCurrentAddress
		self.YearsCurrentEmployer = YearsCurrentEmployer
		self.NumberOfCards = NumberOfCards
		self.CCDebt = CCDebt
		self.Loans = Loans
		self.LoanAmount = LoanAmount
		self.SalePrice = SalePrice
		self.Location = Location
		self.prediction = prediction
		self.probability = probability

	def __repr__(self):
		return '<mortgagedefault%r>' % self.Income

def saveDB(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location,
		prediction, probability):
	record = mortgagedefault(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location,
		prediction, probability)
	db.session.add(record)
	db.session.commit()


def predictDefault(ID, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location):
	
	service_path = 'https://ibm-watson-ml.mybluemix.net'
	username = '37a6c710-9576-456e-a8be-5cf859ccb7e9'
	password = '9eb88d5d-6e5e-4e85-b089-2e6c5ab579b3'

	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')
	header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
	scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2264"
	payload_scoring = ({"record":[ID, Income, AppliedOnline, Residence, YearCurrentAddress,
		YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location]})
	response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
	return response_scoring


@app.route('/',  methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		ID = 999
		#Income = 47422.0
		#AppliedOnline = 'YES'
		#Residence = 'Owner Occupier'
		#YearCurrentAddress = 11.0
		#YearsCurrentEmployer = 12.0
		#NumberOfCards = 2.0
		#CCDebt = 2010.0
		#Loans = 1.0
		#LoanAmount = 12315.0
		#SalePrice = 330000
		#Location = 100


		Income = int(request.form['Income'])
		AppliedOnline = request.form['AppliedOnline']
		Residence = request.form['Residence']
		YearCurrentAddress = int(request.form['YearCurrentAddress'])
		YearsCurrentEmployer = int(request.form['YearsCurrentEmployer'])
		NumberOfCards = int(request.form['NumberOfCards'])
		CCDebt = int(request.form['CCDebt'])
		Loans = int(request.form['Loans'])
		LoanAmount = int(request.form['LoanAmount'])
		SalePrice = int(request.form['SalePrice'])
		Location = int(request.form['Location'])

		session['Income'] = Income
		session['AppliedOnline'] = AppliedOnline
		session['Residence'] = Residence
		session['YearCurrentAddress'] = YearCurrentAddress
		session['YearsCurrentEmployer'] = YearsCurrentEmployer
		session['NumberOfCards'] = NumberOfCards
		session['CCDebt'] = CCDebt
		session['Loans'] = Loans
		session['LoanAmount'] = LoanAmount
		session['SalePrice'] = SalePrice
		session['Location'] = Location


		response_scoring = predictDefault(ID, Income, AppliedOnline, Residence, YearCurrentAddress,
		   YearsCurrentEmployer, NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location)

		prediction = response_scoring.json()["result"]["prediction"]
		probability = response_scoring.json()["result"]["probability"]["values"][0]

		session['prediction'] = prediction
		session['probability'] = probability

		flash('Successful Prediction')
		return render_template('scoreSQL.html', response_scoring=response_scoring, request=request)


	else:
		return render_template('input.html')

@app.route('/saveData', methods=['POST'])
def saveData():
	FirstName = request.form['FirstName']
	LastName = request.form['LastName']

	Income = session['Income']
	AppliedOnline = session['AppliedOnline']
	Residence = session['Residence']
	YearCurrentAddress = session['YearCurrentAddress']
	YearsCurrentEmployer = session['YearsCurrentEmployer']
	NumberOfCards = session['NumberOfCards']
	CCDebt = session['CCDebt']
	Loans = session['Loans']
	LoanAmount = session['LoanAmount']
	SalePrice = session['SalePrice']
	Location = session['Location']
	prediction = session['prediction']
	probability = session['probability']

	#print(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress, YearsCurrentEmployer, NumberOfCards,
	#   CCDebt, Loans, LoanAmount, SalePrice, Location)

	saveDB(FirstName, LastName, Income, AppliedOnline, Residence, YearCurrentAddress,YearsCurrentEmployer,
		NumberOfCards, CCDebt, Loans, LoanAmount, SalePrice, Location, prediction, probability)

	flash('Prediction Successfully Stored in Database')

	return render_template('save.html')

@app.route('/scoretest', methods=['GET', 'POST'])
def scoretest():
	
	service_path = 'https://ibm-watson-ml.mybluemix.net'
	username = '37a6c710-9576-456e-a8be-5cf859ccb7e9'
	password = '9eb88d5d-6e5e-4e85-b089-2e6c5ab579b3'

	headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
	url = '{}/v2/identity/token'.format(service_path)
	response = requests.get(url, headers=headers)
	mltoken = json.loads(response.text).get('token')
	header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
	scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/2264"
	payload_scoring = {"record":[999,47422.000000,"YES","Owner Occupier",11.000000,12.000000,2.000000,2010.000000,1.000000,12315.000000,330000,100]}
	response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
	
	result = response_scoring.text
	return render_template('scoretest.html', result=result, response_scoring=response_scoring)

#if __name__ == '__main__':
#   app.run()
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
