from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import text
import json
import os

Base = declarative_base()

#init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test3000.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

#Init ma
ma = Marshmallow(app)



#entitati

class Pacient(db.Model):
    __tablename__ = 'pacienti'
    id_pacient = db.Column(db.Integer, primary_key = True)
    nume_pacient = db.Column(db.String(100))
    copil = relationship("Disease")

    def __init__(self, id_pacient, nume_pacient):
        self.id_pacient = id_pacient
        self.nume_pacient = nume_pacient



class Disease(db.Model):
    __tablename__ = 'boli'
    id_boala = db.Column(db.Integer, primary_key = True)
    id_pacient = Column(db.Integer, ForeignKey('pacienti.id_pacient'))
    nume = db.Column(db.String(50))
    descriere = db.Column(db.String(100))

    def __init__(self, id_boala, id_pacient, nume, descriere):
        self.id_boala = id_boala
        self.id_pacient = id_pacient
        self.nume = nume
        self.descriere = descriere


class PacientDoctorTable(db.Model):
    __tablename__ = "asocieri"
    id = db.Column(db.Integer, primary_key = True)
    id_doctor  = db.Column(db.Integer, ForeignKey('doctor.doctor_id'))
    id_pacient = db.Column(db.Integer, ForeignKey('pacienti.id_pacient'))

    def __init__(self,id_doctor, id_pacient):
        self.id_doctor = id_doctor
        self.id_pacient = id_pacient

# class PacientDiseaseTable:
#     __tablename__ = 'asociere_boala_pacient'
#     id_boala= db.Column(db.Integer, ForeignKey('boli.id_boala'))
#     id_pacient = db.Column(db.Integer, ForeignKey('pacient.id_pacient'))   

#     def __init__(self, id_boala, id_pacient):
#         self.id_boala = id_boala
#         self.id_pacient = id_pacient


class Doctor(db.Model):

    doctor_id = db.Column(db.Integer, primary_key = True)
    nume = db.Column(db.String(100))
    specializare = db.Column(db.String(50))
    email = db.Column(db.String(50))
    parola = db.Column(db.String(50))
 
    def __init__(self,doctor_id, nume,specializare,email, parola):
        self.doctor_id = doctor_id
        self.nume = nume
        self.specializare = specializare
        self.email = email
        self.parola = parola

 #sfarsit entitati       



class DoctorSchema(ma.Schema):
    class Meta:
        fields = ('doctor_id', 'nume','specializare','email','parola')

class DiseaseSchema(ma.Schema):
    class Meta:
        fields = ('id_boala','id_pacient','nume','descriere')

class PacientSchema(ma.Schema):
    class Meta:
        fields = ('id_pacient','nume_pacient')        

class DoctorPatientSchema(ma.Schema):
    class Meta:
        fields = ('id_doctor', 'id_pacient')


doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

disease_schema = DiseaseSchema()
diseases_schema = DiseaseSchema(many = True)


patient_schema = PacientSchema()
patients_schema = PacientSchema(many=True)

patient_doctor_single = DoctorPatientSchema()
patient_doctor_schema = DoctorPatientSchema(many = True)


#ruta verificare doctor pacient
@app.route('/relatii', methods = ['GET'])
def getRelatie():
    relatii = PacientDoctorTable.query.all()

    result = patient_doctor_schema.dump(relatii)

    return jsonify(result)

#ruta de logare
@app.route('/doctor/<e>/<p>', methods=['GET'])
def get_doctor(e, p):
    query = "select * from doctor WHERE email  = :em LIMIT 1"
  
    doctor = db.session.query(Doctor).filter_by(email = e).filter(parola = p).first()
    db.session.commit()
    dt = doctor_schema.dump(doctor)
    print(dt)
    fl = open('cookie.json','w')
    json.dump(dt,fl)
    return jsonify(dt)

@app.route('/isLoggedIn',methods=['GET'])
def isLoggedIn():
    fl = open('cookie.json','r')
    txt_Data=fl.read()
    if txt_Data != '':
        txt_Data = json.loads(txt_Data)
    else:
        txt_Data = json.loads('{}')
    return jsonify(txt_Data)

#ruta de selectare a pacientilor in functie de doctorul care este logat
@app.route('/myPacients/<doctor_id>')
def get_my_doctors(doctor_id):
    
    query_asociere = db.session.query(PacientDoctorTable).filter_by(id_doctor = doctor_id)

    #array 
    result = patient_doctor_schema.dump(query_asociere)

    pacient_arr = []
    pacienti = []
    for i in result:
        query_pt = db.session.query(Pacient).filter_by(id_pacient = i['id_pacient'])
        # db.session.commit()
        res = patients_schema.dump(query_pt)
        # print(res)
        if len(res) > 0:
            pacienti.append(res[0])

    return jsonify(pacienti)

#ruta pentru register
@app.route('/addDoctor', methods=['POST'])
def add_doctor():
    doctor_id = request.json['doctor_id']
    nume = request.json['nume']
    specializare = request.json['specializare']
    email = request.json['email']
    password = request.json['parola']
  
    new_doctor = Doctor(doctor_id, nume, specializare,email, password)

    db.session.add(new_doctor)
    db.session.commit()

    return doctor_schema.jsonify(new_doctor)



#ruta de popularea a tabelei de asociere intre doctor si pacient
@app.route('/insertRelationship', methods = ['POST'])
def insert_relationship():
    id_doctor = request.json['id_doctor']
    id_patient = request.json['id_pacient']

    rel = PacientDoctorTable(id_doctor,id_patient)

    db.session.add(rel)
    db.session.commit()


    return patient_doctor_single.jsonify(rel)


#ruta de creare a pacientului
@app.route('/addPacient', methods=['POST'])
def addPacient():
    pacient_id = request.json['id_pacient']
    nume = request.json['nume_pacient']

    pacient = Pacient(pacient_id, nume)
    db.session.add(pacient)
    db.session.commit()

    return patient_schema.jsonify(pacient)


#ruta de creeare a unei boli
@app.route('/addDisease', methods=['POST'])
def addDisease():
    id_boala = request.json['id_boala']
    id_pacient = request.json['id_pacient']
    nume = request.json['nume']
    descriere = request.json['descriere']

    disease = Disease(id_boala, id_pacient, nume, descriere)

    db.session.add(disease)
    db.session.commit()

    return disease_schema.jsonify(disease)


#route for test
@app.route('/', methods=['GET'])
def hello():
    return "Hello World"


#ruta de selectare a tuturor doctorilor
@app.route('/doctors', methods=['GET'])
def get_doctors():
    all_doctors = Doctor.query.all()
    
    result = doctors_schema.dump(all_doctors)

    return jsonify(result)


#ruta de selectare a pecientilor
@app.route('/pacients', methods=['GET'])
def get_patients():
    all_patients = Pacient.query.all()

    result = patients_schema.dump(all_patients)

    return jsonify(result)


#ruta de selectare a bolilor
@app.route('/diseases', methods=['GET'])
def get_diseases():
    all_diseases = Disease.query.all()

    result = diseases_schema.dump(all_diseases)

    return jsonify(result)


#run server


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)
