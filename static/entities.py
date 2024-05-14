from static import db
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash


#Associative entity between enrollment and Candidate m2m
enrollment_candidate_association=db.Table(
    'certificate',
    db.Column('id',db.Integer,primary_key=True,nullable=False),
    db.Column('EnrollmentId',db.Integer,db.ForeignKey('enrollment.id'),nullable=True),
    db.Column('CandidateId',db.Integer,db.ForeignKey('candidate.id'),nullable=True)
)

#Associative entity between candidate and qualification m2m

candidate_qualification_association=db.Table(
    'credentials',
    db.Column('id',db.Integer,primary_key=True,nullable=False),
    db.Column('CandidateId',db.Integer,db.ForeignKey('candidate.id'),nullable=False),
    db.Column('QualificationId',db.Integer,db.ForeignKey('qualification.id'),nullable=True)
)

class Application(db.Model):
    __tablename__ = 'application'
    
    id = db.Column(db.Integer, primary_key=True)
    CandidateId = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    OpeningId = db.Column(db.Integer, db.ForeignKey('opening.id'), nullable=False)
    ApplicationDate = db.Column(db.DateTime, default=datetime.utcnow)
    CoverLetter = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Application {self.id}>'


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key = True,nullable=False)
    JobDescription=db.Column(db.String(100), nullable=False)
    
class Company(db.Model):
    __tablename__ = 'company'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    CompanyName=db.Column(db.String(100), nullable=False)
    CompanyAddress=db.Column(db.String(100), nullable=False)
    CompanyPhoneNo=db.Column(db.String(20),nullable=False)
    CompanyEmail=db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'{self.id}'
    
    def getCompanyName(CompanyId):
        companyName = Company.query.filter_by(id=CompanyId).first()
        return f'{companyName.CompanyName}'
    
class SpecificQualification(db.Model):
    __tablename__='specificqualification'
    id=db.Column(db.String(50), primary_key=True,nullable=False)
    Description=db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'{self.id}'
    
    def getSpecificQualificationName(SpecificQualificationId):
        specificQualificationName = SpecificQualification.query.filter_by(id=SpecificQualificationId).first()
        return f'{specificQualificationName.Description}'
    
class Qualification(db.Model):
    __tablename__='qualification'
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    QualificationName=db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f'{self.id}'
    
    def getQualificationName(QualificationId):
        qualificationName = Qualification.query.filter_by(id=QualificationId).first()
        return f'{qualificationName.QualificationName}'
    
    #credents = db.relationship('Candidate', secondary=candidate_qualification_association, backref=db.backref('candidate_qualification', lazy='dynamic'),overlaps="credents,candidates")
    
class Course(db.Model):
    __tablename__='course'
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    CourseName=db.Column(db.String(100),nullable=False)
    TrainingDescription=db.Column(db.String(255),nullable=False)
    TrainingStartDate=db.Column(db.DateTime(timezone=True), nullable=False)
    TrainingEndDate=db.Column(db.DateTime(timezone=True), nullable=False)
    PaymentType=db.Column(db.String(50), nullable=False)
    PaymentDate=db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    
class JobHistory(db.Model):
    __tablename__='jobhistory'
    id=db.Column(db.Integer, primary_key=True,nullable=False)
    JobId=db.Column(db.Integer, db.ForeignKey('job.id'),nullable=False)
    JobStartDate=db.Column(db.DateTime(timezone=True), nullable=False)
    JobEndDate=db.Column(db.DateTime(timezone=True),nullable=False)
    
class Candidate(db.Model):
    __tablename__='candidate'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    CandidateName=db.Column(db.String(50),nullable=False)
    Birthdate=db.Column(db.DateTime(timezone=True),nullable=False)
    Age=db.Column(db.Integer,nullable=False)
    Gender=db.Column(db.String(50),nullable=False)
    ContactNo=db.Column(db.String(15), nullable=False)
    Email=db.Column(db.String(50), nullable=True)
    JobHistoryid = db.Column(db.Integer, db.ForeignKey('jobhistory.id'),nullable=False)
    
    #candidates = db.relationship('Qualification', secondary=candidate_qualification_association, backref=db.backref('qualification_possessed', lazy='dynamic'),overlaps="credents,candidates")

class Opening(db.Model):
    __tablename__='opening'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    CompanyId=db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    QualificationId=db.Column(db.Integer,db.ForeignKey('qualification.id'),nullable=False)
    Code=db.Column(db.String(50),db.ForeignKey('specificqualification.id'),nullable=True)
    JobName=db.Column(db.String,nullable=False)
    JobDescription=db.Column(db.String,nullable=False)
    Startdate=db.Column(db.DateTime(timezone=True),nullable=False)
    Enddate=db.Column(db.DateTime(timezone=True),nullable=False)
    JobShift=db.Column(db.String(50),nullable=False)
    JobType=db.Column(db.String(25),nullable=False)
    HourlyPay=db.Column(db.Integer,nullable=False)
    Address=db.Column(db.String(100), nullable=False)
        
class Prerequisite(db.Model):
    __tablename__='prerequisite'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    PrerequisiteQualification=db.Column(db.Integer,db.ForeignKey('qualification.id'),nullable=False)
    
class Enrollment(db.Model):
    __tablename__='enrollment'
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    CoursePrerequisiteId=db.Column(db.Integer,db.ForeignKey('prerequisite.id'),nullable=True)
    CourseId=db.Column(db.Integer,db.ForeignKey('course.id'),nullable=True)
    DateStart=db.Column(db.DateTime(timezone=True),nullable=False)
    DateEnd=db.Column(db.DateTime(timezone=True),nullable=False)    
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
