from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_BASE_URL = "https://project-consulting-function-app.azurewebsites.net/api"

@app.route("/")
def home():
  return redirect(url_for('list_customers'))

@app.route("/customers")
def list_customers():
  try:
    response = requests.get(f"{API_BASE_URL}/customers")

    if response.status_code == 200:
      customers = response.json()
      return render_template("index.html", customers=customers)
    else:
      return f"API Error: {response.text}", 500
  except Exception as e:
    return f"An unknown error occured: {str(e)}", 500

@app.route("/customer/<int:customer_id>")
def get_customer(customer_id):
  try:
    response = requests.get(f"{API_BASE_URL}/customer/{customer_id}")

    if response.status_code == 200:
      data = response.json()
      customer = Customer(
        ID=data.get("ID", ""),
        FirstName=data.get("FirstName", ""),
        LastName=data.get("LastName", ""),
        Street=data.get("Street", ""),
        HouseNumber=data.get("HouseNumber", ""),
        PostalCode=data.get("PostalCode", ""),
        City=data.get("City", ""),
        Country=data.get("Country", ""),
        Mail=data.get("Mail", ""),
        Telephone=data.get("Telephone", "")
      )
      
      return render_template("customer/index.html", customer=customer.to_dict())
    else:
      return f"API Error: {response.text}", 500
  except Exception as e:
    return f"An error occured: {str(e)}", 500

@app.route("/customer/matching", methods=["GET", "POST"])
def search_or_create_customer():
    if request.method == "POST":
        data = {
            "FirstName": request.form.get("FirstName", "").strip(),
            "LastName": request.form.get("LastName", "").strip(),
            "Street": request.form.get("Street", ""),
            "HouseNumber": request.form.get("HouseNumber"),
            "PostalCode": request.form.get("PostalCode"),
            "City": request.form.get("City", "").strip(),
            "Country": request.form.get("Country", "").strip(),
            "Mail": request.form.get("Mail", "").strip(),
            "Telephone": request.form.get("Telephone", ""),
        }
        try:
          response = requests.post(f"{API_BASE_URL}/matching", json=data)
          response.raise_for_status()

          result = response.json()
          
          return render_template('customer/matching.html', response_data = result)
        
        except requests.exceptions.RequestException as e:
          return render_template('customer/matching.html', error=str(e), form=data)

    # For GET, just render the matching page
    return render_template("customer/matching.html")

class Customer:
  def __init__(self, ID=None, FirstName=None, LastName=None, Street=None, HouseNumber=None, PostalCode=None, City=None, Country=None, Mail=None, Telephone=None):
    self.ID = ID or ""
    self.FirstName = FirstName or ""
    self.LastName = LastName or ""
    self.Street = Street or ""
    self.HouseNumber = HouseNumber
    self.PostalCode = PostalCode
    self.City = City or ""
    self.Country = Country or ""
    self.Mail = Mail or ""
    self.Telephone = Telephone

  def to_dict(self):
    return {
      "ID": self.ID,
      "FirstName": self.FirstName,
      "LastName": self.LastName,
      "Street": self.Street,
      "HouseNumber": self.HouseNumber,
      "PostalCode": self.PostalCode,
      "City": self.City,
      "Country": self.Country,
      "Mail": self.Mail,
      "Telephone": self.Telephone
    }
  
  def __str__(self):
    return f"Customer(ID={self.ID}, FirstName={self.FirstName}, LastName={self.LastName}, Street={self.Street}, HouseNumber={self.HouseNumber}, PostalCode={self.PostalCode}, City={self.City}, Country={self.Country}, Mail={self.Mail}, Telephone={self.Telephone})"

if __name__ == "__main__":
  app.run(debug=False)

#test