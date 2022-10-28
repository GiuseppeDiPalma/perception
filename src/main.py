from flask import Flask, request


@app.route('/titles', methods=['POST'])

def main():
    print("Iniziamo")
    print(request.form['POST'])
    return "Received"
