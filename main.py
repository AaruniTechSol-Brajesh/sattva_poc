import os
import jsonify
import requests
import numpy as np
import pandas as pd
import PyPDF2 as pdf
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, request
app = Flask(__name__, template_folder = 'Templates')
@app.route('/', methods = ['GET'])
def Home():    
    return render_template('home.html')
standard_to = StandardScaler()
@app.route('/extract', methods = ['POST'])
def extract():
    if request.method == 'POST':
        path = os.getcwd() + '\\Invoices\\'
        invoice_no, date, customer_id, name, company, address, contact, email, amount = [], [], [], [], [], [], [], [], []
        for i in os.listdir(path):
            file = open(os.getcwd() + '\\Invoices\\' + str(i), 'rb')
            file = pdf.PdfFileReader(file)
            file = file.getPage(0)
            file = file.extractText()
            file = file.split('\n')
            invoice_no.append(file[88])
            date.append(file[6])
            customer_id.append(file[93])
            name.append(file[9])
            company.append(file[10])
            address.append(', '.join(file[11 : 13]))
            contact.append(file[13])
            email.append(file[14])
            total = file[83]
            total = total.split(' ')
            total = ''.join(total)
            total = total.split(',')
            total = '.'.join(total)
            amount.append(total)
        data = {'Invoice No' : invoice_no, 'Date' : date, 'Customer ID' : customer_id, 'Name' : name, 'Company' : company, 'Address' : address, 'Contact' : contact, 'Email' : email, 'Amount' : amount}
        data = pd.DataFrame(data)
        df = pd.read_csv('Invoice Details.csv')
        df = pd.concat([df, data], axis = 0)
        df.to_csv('Invoice Details.csv', index = None)        
        return render_template('home.html')
    else:
        return render_template('home.html')
if __name__=="__main__":
    #app.run(host = '0.0.0.0', port = 8080)
    #app.run(debug = True)
    app.run()