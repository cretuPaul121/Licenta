from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import text
from flask_cors import CORS
import json
import os

Base = declarative_base()

#init app
app = Flask(__name__)
CORS(app)

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
    # copil = relationship("Disease")

    def __init__(self, id_pacient, nume_pacient):
        self.id_pacient = id_pacient
        self.nume_pacient = nume_pacient



class Disease(db.Model):
    __tablename__ = 'boli'
    id_boala = db.Column(db.Integer, primary_key = True)
    nume = db.Column(db.String(60))
    descriere = db.Column(db.String(150))

    def __init__(self, nume, descriere):
        # self.id_boala = id_boala
        self.nume = nume
        self.descriere = descriere


class Ecg(db.Model):
    __tablename__ = 'ecg'
    id_ecg = db.Column(db.Integer, primary_key = True)
    id_pacient = db.Column(db.Integer)
    data = db.Column(db.String(60))
    continut = db.Column(db.String(750))

    def __init__(self, id_pacient, data, continut):
        self.id_pacient = id_pacient
        self.data = data
        self.continut = continut

class PacientDoctorTable(db.Model):
    __tablename__ = "asocieri"
    id = db.Column(db.Integer, primary_key = True)
    id_doctor  = db.Column(db.Integer, ForeignKey('doctor.doctor_id'))
    id_pacient = db.Column(db.Integer, ForeignKey('pacienti.id_pacient'))

    def __init__(self,id_doctor, id_pacient):
        self.id_doctor = id_doctor
        self.id_pacient = id_pacient

class PacientDiseaseTable(db.Model):
    __tablename__ = "pacientiboli"
    id = db.Column(db.Integer,primary_key = True)
    id_pacient = db.Column(db.Integer, ForeignKey('pacienti.id_pacient'))
    id_boala = db.Column(db.Integer,ForeignKey('boli.id_boala'))

    def __init__(self,id_pacient,id_boala):
        self.id_pacient = id_pacient
        self.id_boala = id_boala

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
        fields = ('id_boala','nume','descriere')

class PacientSchema(ma.Schema):
    class Meta:
        fields = ('id_pacient','nume_pacient')        

class DoctorPatientSchema(ma.Schema):
    class Meta:
        fields = ('id_doctor', 'id_pacient')

class PacientDiseaseSchema(ma.Schema):
    class Meta:
        fields = ('id_pacient','id_boala')

class EcgSchema(ma.Schema):
    class Meta:
        fields = ('id_pacient','data','continut')

currPac_Id = -1

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

disease_schema = DiseaseSchema()
diseases_schema = DiseaseSchema(many = True)


patient_schema = PacientSchema()
patients_schema = PacientSchema(many=True)

patient_doctor_single = DoctorPatientSchema()
patient_doctor_schema = DoctorPatientSchema(many = True)

patient_disease_single = PacientDiseaseSchema()
patient_disease_many = PacientDiseaseSchema(many=True)

ecg_schema = EcgSchema()

#ruta verificare doctor pacient
@app.route('/relatii', methods = ['GET'])
def getRelatie():
    relatii = PacientDoctorTable.query.all()

    result = patient_doctor_schema.dump(relatii)

    return jsonify(result)

@app.route('/logout',methods = ['GET'])
def delogare():
    fl = open('cookie.json','w')
    fl.write('')
    resp = dict()
    resp['status'] = 'LoggedOut'
    return json.dumps(resp)

#ruta de logare
@app.route('/doctor/<e>/<p>', methods=['GET'])
def get_doctor(e, p):
    query = "select * from doctor WHERE email  = :em LIMIT 1"
    doctor = db.session.query(Doctor).filter_by(email = e).filter_by(parola = p).first()
    db.session.commit()
    dt = doctor_schema.dump(doctor)
    print(dt)
    fl = open('cookie.json','w')
    json.dump(dt,fl)
    return jsonify(dt)

@app.route('/setPacient/<v>',methods=['GET'])
def set_Pacient(v):
    global currPac_Id
    currPac_Id = v
    d = dict()
    d['status'] = 'done'
    return jsonify(d)

@app.route('/getCurrPacient',methods=['GET'])
def getCurrPacient():
    d = dict()
    d['id'] = currPac_Id
    return jsonify(d)

@app.route('/isLoggedIn',methods=['GET'])
def isLoggedIn():
    fl = open('cookie.json','r')
    txt_Data=fl.read()
    if txt_Data != '':
        txt_Data = json.loads(txt_Data)
    else:
        txt_Data = json.loads('{}')
    return jsonify(txt_Data)

@app.route('/diseases',methods=['GET'])
def get_Disease():
    fl = open('cookie.json','r')
    txt_Data = fl.read()
    if txt_Data != '':
        diseases = db.session.query(Disease).all()
        db.session.commit()
        print(diseases)
        result = []
        for i in diseases:
            result.append(disease_schema.dump(i))
        # dt = disease_schema.dump(diseases)
        return jsonify(result)

@app.route('/pacientDiseases/<pacient_id>',methods=['GET'])
def get_pacientDiases(pacient_id):
    fl = open('cookie.json','r')
    txt_Data = fl.read()
    if txt_Data != '':
        pacient_Diseases = db.session.query(PacientDiseaseTable).filter_by(id_pacient=pacient_id).all()
        db.session.commit()
        result = []
        for i in pacient_Diseases:
            result.append(patient_disease_single.dump(i))
        resultDis = []
        for i in result:
            disease = db.session.query(Disease).filter_by(id_boala=i['id_boala'])
            db.session.commit()
            for j in disease:
                resultDis.append(disease_schema.dump(j))
            print(resultDis)
        return jsonify(resultDis)

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

@app.route('/patient/<i>',methods=['GET'])
def get_PatientAt(i):
    query_asoc = db.session.query(Pacient).filter_by(id_pacient=i).first()
    res = patient_schema.dump(query_asoc)
    return jsonify([res])

@app.route('/ecg/<id_pacient>',methods=['GET'])
def get_Ecg(id_pacient):
    query_ecg = db.session.query(Ecg).filter_by(id_pacient=id_pacient).first()
    print(query_ecg)
    result = ecg_schema.dump(query_ecg)
    return jsonify(result)

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

@app.route('/addDisease',methods=['POST'])
def add_Disease():
    nume = request.json['nume_boala']
    descr = request.json['descriere']
    boala = Disease(nume,descr)
    db.session.add(boala)
    db.session.commit()
    return disease_schema.jsonify(boala)

@app.route('/addEcg',methods=['POST'])
def add_Ecg():
    id_pacient = request.json['id_pacient']
    data = request.json['data']
    continut = request.json['continut']
    ecgS = Ecg(id_pacient,data,str(continut))
    db.session.add(ecgS)
    db.session.commit()
    return ecg_schema.jsonify(ecgS)


@app.route('/addPacientDisease',methods=['POST'])
def add_PacientDisease():
    id_pacient = request.json['id_pacient']
    id_boala = request.json['id_boala']
    asoc = PacientDiseaseTable(id_pacient,id_boala)
    db.session.add(asoc)
    db.session.commit()

    return patient_disease_single.jsonify(asoc)


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
