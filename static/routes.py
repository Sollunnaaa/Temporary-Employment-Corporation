from static import app,db
from flask import render_template, request, redirect,url_for,jsonify,flash
import locale,os
from static.entities import *
from static.forms import *
from flask import session


#Login/Signup
@app.route('/')
def index():
    return render_template('loginsignup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        # Here you might set a session variable to track if the user is logged in
        return redirect(url_for('dashboard'))
    else:
        return "Invalid username or password"

@app.route('/dashboard')
def dashboard():
    # Here you might check if the user is logged in using session variables
    return redirect(url_for('main'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another one."
        
        new_user = User(full_name=full_name, username=username, email=email)
        new_user.set_password(password)  # Set password using the set_password method
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('create_account.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

#Home Page----------------------------------------------------------------
@app.route('/home')
def main():
    query=request.args.get('query','')
    return redirect('search')

#-----------------------------------------------------------------------------
#About Us page
@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')
#---------------------------------------------------------------------------------------------
#Search Page
@app.route('/search',methods=['GET','POST'])
def search():   
    query = request.args.get('query','')
    if query:
        results = Opening.query.filter(Opening.JobName.ilike(f"%{query}%") | Opening.CompanyId.ilike(f"%{query}%")).order_by(Opening.JobName).all()
        for result in results:
            companyNames = Company.getCompanyName(result.CompanyId)
            result.CompanyId = companyNames
    else:
        results=Opening.query.group_by(Opening.JobName).order_by(Opening.JobName).all() 
        for result in results:
            companyNames = Company.getCompanyName(result.CompanyId)
            result.CompanyId = companyNames
            
    return render_template('HomePage.html',query=query,results=results)
#-------------------------------------------------------------------------------------------------------
#dynamically update side panel
def get_openings():
    # Query Opening entity class to retrieve openings from the database
    openings = Opening.query.all() 
    return openings

def get_opening_details(opening_id):
    # Query Opening entity class to retrieve details of a specific opening by ID
    opening = Opening.query.get(opening_id) 
    return opening

@app.route('/details/<int:opening_id>')
def get_opening(opening_id):
    
    opening = get_opening_details(opening_id)
    if opening:
        opening_dict = {
            'id': opening.id,
            'JobName': opening.JobName,
            'CompanyId': Company.getCompanyName(opening.CompanyId),
            'Startdate': opening.Startdate.strftime('%B %d %Y'),  # Convert to string in desired format
            'Enddate': opening.Enddate.strftime('%B %d %Y'),  # Convert to string in desired format
            'HourlyPay': opening.HourlyPay,
            'JobShift':opening.JobShift,
            'JobType' :opening.JobType,
            'Address':opening.Address,
            'JobDetails': opening.JobDescription,
            'SpecificQualification': SpecificQualification.getSpecificQualificationName(opening.Code),
            'Qualification':Qualification.getQualificationName(opening.QualificationId)
        }
        return jsonify(opening_dict)    
    else:
        return jsonify({'error': 'Opening not found'}), 404
#-----------------------------------------------------------------------------------------------------------------------
#Job Page
archived_jobs = []

@app.route('/postpage', methods=['GET'])
def employ():
    query = request.args.get('query','')
    jobs = Opening.query.all()
    sort_order = request.args.get('sort', None)
    if sort_order == 'newest':
        sorted_jobs = sorted(jobs, key=lambda x: x['id'], reverse=True)
    elif sort_order == 'oldest':
        sorted_jobs = sorted(jobs, key=lambda x: x['id'])
    else:
        sorted_jobs = jobs # No sorting applied if sort_order is None
    return render_template('postpage.html',query=query,jobs=sorted_jobs,archived_jobs=archived_jobs)


@app.route('/submit_job', methods=['GET','POST'])
def submit_job():
    form = OpeningForm()
    if form.validate_on_submit():
        JobName=form.JobName.data
        pay = form.pay.data
        description = form.description.data
        Startdate = form.Startdate.data
        Enddate = form.Enddate.data
        jobshift=form.jobshift.data
        jobtype=form.jobtype.data
        address=form.address.data
        job_to_add = Opening(JobName=JobName,HourlyPay=pay,JobDescription=description,Startdate=Startdate,Enddate=Enddate,JobShift=jobshift,JobType=jobtype,Address=address,) 
        similarJobs = Opening.query.filter(Opening.name.like(f'%{job_to_add.name}')).all()
        if similarJobs:
             flash(f'Job: {job_to_add.name} is already in the database!',category='warning')
        else:
            db.session.add(job_to_add)
            db.session.commit()
            flash(f'Success! Item {job_to_add.name} has been created!', category='success')
            query = request.args.get('query','')
            results = Opening.query.filter(Opening.name.ilike(f"%{query}%")).all()
            
            results = [results[-1]] + results[:-1]
            return render_template('postpage.html', job=results,query=query,form=form)
        CheckFormError(form)
        return redirect(url_for('employ'))
    
    

@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    query=request.args.get('query','')
    jobs = Opening.query.filter(Opening.id.ilike(f"%{query}%")).all()
    archived_jobs
    # Find the job by ID and remove it from the jobs list, then add it to archived jobs
    job_to_delete = next((job for job in jobs if job['id'] == job_id), None)
    if job_to_delete:
        jobs.remove(job_to_delete)
        archived_jobs.append(job_to_delete)
        flash('Job successfully archived!', 'info')
    return redirect(url_for('employ'))

@app.route('/restore_job/<int:job_id>', methods=['POST'])
def restore_job(job_id):
    global jobs, archived_jobs
    # Find the job by ID and remove it from the archived jobs list, then add it to the jobs list
    job_to_restore = next((job for job in archived_jobs if job['id'] == job_id), None)
    if job_to_restore:
        archived_jobs.remove(job_to_restore)
        jobs.append(job_to_restore)
        flash('Job successfully restored!', 'success')
    return redirect(url_for('employ'))

@app.route('/search_jobs', methods=['GET'])
def search_jobs(): 
    query = request.args.get('query','')
    if query:
        results = Opening.query.filter(Opening.JobName.ilike(f"%{query}%") | Opening.CompanyId.ilike(f"%{query}%")).order_by(Opening.JobName).all()
        for result in results:
            companyNames = Company.getCompanyName(result.CompanyId)
            result.CompanyId = companyNames
    else:
        results=Opening.query.group_by(Opening.JobName).order_by(Opening.JobName).all() 
        for result in results:
            companyNames = Company.getCompanyName(result.CompanyId)
            result.CompanyId = companyNames
            
    return render_template('postpage.html',query=query,jobs=results)
#---------------------------------------------------------------------------------------------------------------------------------
#apply

@app.route('/apply/<int:opening_id>', methods=['GET', 'POST'])
def apply(opening_id):
    if request.method == 'GET':
        opening = Opening.query.get(opening_id)
        if not opening:
            flash('The job opening does not exist.', 'error')
            return redirect(url_for('main'))
        
        # Display the application form
        return render_template('apply.html', opening=opening)
    
    elif request.method == 'POST':
        # Process the application
        candidate_id = request.form['candidate_id'] 
        cover_letter = request.form['cover_letter']
        
        application = Application(
            CandidateId=candidate_id,
            OpeningId=opening_id,
            CoverLetter=cover_letter,
            ApplicationDate=datetime.utcnow()
        )
        db.session.add(application)
        db.session.commit()
        
        flash('Your application has been submitted.', 'success')
        return redirect(url_for('main'))

#---------------------------------------------------------------------------------------------------------------------------
#Below are functions and methods used by the whole system
def datetimeformat(value, format='%B %d, %Y' ):
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat

#Tried to change company id foreign key (not working)
def formatItems(items):
    query = request.args.get('query','')
    for item in items:
        query_company = Company.query.filter(Company.CompanyName)
        item.Id = query_company
    
    return items

def CheckFormError(form):
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')
    