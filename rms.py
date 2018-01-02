from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, validators, SelectField, DateTimeField, DateField
from passlib.hash import sha256_crypt
from database import users, register, lastrohinga, lastrohingaFamily , schoolinfo, healthevent, pendingevents, housingg, foods, itemRecords, needfoods
from flask_mysqldb import MySQL
from wtforms.validators import InputRequired, Length
from functools import wraps


app = Flask(__name__)

app.config['SECRET_KEY'] = "thisissecrect"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'demo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

ulist = []
check = 0
data = {}


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message='An Email Is Required')])
    password = PasswordField('Password', validators=[InputRequired('Password is Required'), Length(min=5, max=10, message='Password must be 5 to 10 charecters')])
    role = SelectField(
        'role',
        choices=[('admin', 'Admin'), ('doctor', 'Doctor')]
    )


class addrohingaForm(FlaskForm):
    rohinga_name = StringField('Name', validators=[InputRequired(message='A name Is Required')])
    age = StringField('Age')
    sex = SelectField(
        'Sex',
        choices=[('M', 'male'), ('F', 'Female'), ('O', 'Other')]
    )
    new_family_id = SelectField(
        'NEED NEW FAMILY ID ?',
        choices=[('0', 'NO'), ('1', 'YES')]
    )
    family_id = StringField('Existing FAMILY ID ( IF THERE IS ANY )')
    camp_no = StringField('Camp No', validators=[InputRequired(message='A camp_no Is Required')])
   


class addschoolForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='A School name Is Required')])
    camp_no = StringField('Camp No', validators=[InputRequired(message='A camp_no Is Required')])
    teacher_count = StringField('Total Teacher', validators=[InputRequired(message='A teacher count Is Required')])
    student_count = StringField('Total Student', validators=[InputRequired(message='A student_count Is Required')])
    student_capacity = StringField('Student Capacity',validators=[InputRequired(message='A student_capacity Is Required')])
    contact = StringField('Contact', validators=[InputRequired(message='A contact Is Required')])
   


class campss(FlaskForm):
    camp_name = StringField('Camp Name', validators=[InputRequired(message='A camp_name Is Required')])
    camp_no = StringField('Camp No', validators=[InputRequired(message='A camp_no Is Required')])
    address = StringField('Address', validators=[InputRequired(message='A address Is Required')])
    sanitation = StringField('Sanitation', validators=[InputRequired(message='A sanitation Is Required')])
    tubewell = StringField('Tubewell',validators=[InputRequired(message='A tubewell Is Required')])

class event(FlaskForm):
    event_name = StringField('Event Name', validators=[InputRequired(message='A name Is Required')])
    sector = SelectField(
        'Sector',
        choices=[('Health', 'Health'), ('Education', 'Education')]
    )
    Description = StringField('Description', validators=[InputRequired(message='A contact Is Required')])
    contact = StringField('Contact', validators=[InputRequired(message='A contact Is Required')])
    startdate = DateTimeField('Start Date And Time( yyyy-mm-dd hh:mm:ss )', validators=[InputRequired(message='A Date And Time Is Required')])
    enddate = DateTimeField('End Date And Time ( yyyy-mm-dd hh:mm:ss )', validators=[InputRequired(message='A Date And Time Is Required')])
    

class appevent(FlaskForm):
    administrator = StringField('Administrator', validators=[InputRequired(message='A contact Is Required')])
    volunteer = StringField('Volunteer', validators=[InputRequired(message='A contact Is Required')])
    checked = SelectField(
        'Checked',
        choices=[('1', 'Yes'), ('0', 'No')]
    )

class volunteer(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='A name Is Required')])
    department = SelectField(
        'Department',
        choices=[('Doctor', 'Doctor'), ('Teacher', 'Teacher'), ('volunteer', 'volunteer')]
    )
    contact = StringField('Contact', validators=[InputRequired(message='A contact Is Required')])
    check_in = DateTimeField('Check In ( yyyy-mm-dd hh:mm:ss )', validators=[InputRequired(message='A Date And Time Is Required')])
    check_out = DateTimeField('Check Out ( yyyy-mm-dd hh:mm:ss )', validators=[InputRequired(message='A Date And Time Is Required')])


class Doctor(FlaskForm):
    doctor_name  = StringField('Doctor Name ', validators=[InputRequired(message='A name Is Required')])
    department = StringField('Department', validators=[InputRequired(message='A department Is Required')])
    contact = StringField('Contact', validators=[InputRequired(message='A contact Is Required')])
    camp_no = StringField('Camp No', validators=[InputRequired(message='A camp_no Is Required')])


class Patientt(FlaskForm):
    patient_id  = StringField('Rohinga ID ', validators=[InputRequired(message='A name Is Required')])
    doctor_id  = StringField('Doctor Id ', validators=[InputRequired(message='A name Is Required')])
    department = StringField('Department', validators=[InputRequired(message='A department Is Required')])
    disease = StringField('Disease', validators=[InputRequired(message='A disease Is Required')])
    start_date = DateField('Start Date', validators=[InputRequired(message='A start_date Is Required')])
    end_date = StringField('End Date')


class aidd(FlaskForm):
    family_id  = StringField('Family ID ', validators=[InputRequired(message='A name Is Required')])
    typee   = SelectField(
        'Type',
        choices=[('Blanket', 'Blanket'), ('Rice', 'Rice'),  ('Dal', 'Dal')]
    )
    amount  = StringField('Amount ', validators=[InputRequired(message='A department Is Required')])
    expire  = DateTimeField('Expire Date ( yyyy-mm-dd hh:mm:ss )', validators=[InputRequired(message='A department Is Required')])

class aidcategoryy(FlaskForm):
    typee  = StringField('Type ', validators=[InputRequired(message='A name Is Required')])
    amount  = StringField('Amount(Per Person)', validators=[InputRequired(message='Amount Is Required')])
    


@app.route('/')
def rootdr():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/food')
def food():
    ulist = []
    a = foods("Rice")
    b = foods("Dal")
    cur = mysql.connection.cursor()
    cur.execute('''SELECT amount FROM items where type="Rice"''')
    rv = cur.fetchall()
    for i in rv:
        amount=i['amount']
    print(amount)
    c = needfoods(amount)
    print(c)
    cur.execute('''SELECT amount FROM items where type="Dal"''')
    rv = cur.fetchall()
    for i in rv:
        amount=i['amount']
    print(amount)
    d = needfoods(amount)
    print(d)
    return render_template('food.html', a=a,b=b,c=c,d=d)


@app.route('/housing')
def housing():
    ulist = []
    a = housingg()
    for i in a:
        ulist.append(i)

    print(ulist)
    return render_template('housing.html', ulist=ulist)


@app.route('/housing/<string:id>/', methods=['GET', 'POST'])
def housingdetails(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT SUM(member_count) as Total_population FROM family where camp_no=%s''',id)
    rv = cur.fetchall()
    for i in rv:
        T_Population=i['Total_population']
    print(T_Population)


    cur.execute('''SELECT SUM(member_count) as Total_population FROM family''')
    rv = cur.fetchall()
    for i in rv:
        Total_P=i['Total_population']


    cur.execute('''SELECT COUNT(rohinga_id) as Total_male FROM rohinga where camp_no=%s and sex="M"''',id)
    rv = cur.fetchall()
    for i in rv:
        T_Male=i['Total_male']
    print(T_Male)


    cur.execute('''SELECT COUNT(rohinga_id) as Total_Female FROM rohinga where camp_no=%s and sex="F"''',id)
    rv = cur.fetchall()
    for i in rv:
        T_Female=i['Total_Female']
    print(T_Female)


    cur.execute('''SELECT SUM(children) as Total_children FROM family where camp_no=%s''',id)
    rv = cur.fetchall()
    for i in rv:
        T_children=i['Total_children']
    print(T_children)


    cur.execute('''SELECT COUNT(family_id) as Total_Family FROM family where camp_no=%s''',id)
    rv = cur.fetchall()
    for i in rv:
        T_Family=i['Total_Family']
    print(T_Family)

    cur.execute('''SELECT COUNT(family_id) as Total_Family FROM family''')
    rv = cur.fetchall()
    for i in rv:
        Total_F=i['Total_Family']
    print(T_Family)

    Total_FF=round(((T_Family/Total_F)*100),2)
    Total_PP=round(((T_Population/Total_P)*100),2)
    p_M= round(((T_Male/Total_P)*100),2)
    p_F= round(((T_Female/Total_P)*100),2)
    p_C= round(((T_children/Total_P)*100),2)

    return render_template('campinfo.html',T_Population=T_Population,T_Male=T_Male,T_Female=T_Female,T_children=T_children,T_Family=T_Family,Total_PP=Total_PP,Total_FF=Total_FF,p_M=p_M,p_F=p_F,p_C=p_C)



@app.route('/health')
def health():
    ulist = []
    a = healthevent()
    for i in a:
        ulist.append(i)

    print(ulist)
    return render_template('health.html', ulist=ulist)


@app.route('/deshboard')
@is_logged_in
def deshboard():
    return render_template('admin-deshboard.html')


@app.route('/addrohinga', methods=['GET', 'POST'])
@is_logged_in
def addrohinga():
    form = addrohingaForm()
    data = {}
    data2 = {}
    if form.validate_on_submit():
        rohinga_name = form.rohinga_name.data
        age = form.age.data
        sex = form.sex.data
        new_family_id = (form.new_family_id.data)
        family_id = (form.family_id.data)
        camp_no = (form.camp_no.data)
        print(camp_no)
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM camps WHERE camp_no=%s", [camp_no])
        familydata = cur.fetchone()
        camp_name = familydata['camp_name']
        print(camp_name)
        black_listed = 0
        cur = mysql.connection.cursor()
        if new_family_id == '0':
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM family WHERE family_id = %s", [family_id])
            familydata = cur.fetchone()
            if int(age) >= 18:
                updateElder=int(familydata['elder'])+1
                updateChildren=int(familydata['children'])
                updateMember=int(familydata['member_count'])+1
                cur.execute("""UPDATE family SET member_count=%s, children=%s, elder=%s WHERE family_id=%s""",(updateMember,updateChildren,updateElder,family_id))
                mysql.connection.commit()
            else:
                updateElder=int(familydata['elder'])
                updateChildren=int(familydata['children'])+1
                updateMember=int(familydata['member_count'])+1
                cur.execute("""UPDATE family SET member_count=%s, children=%s, elder=%s WHERE family_id=%s""",(updateMember,updateChildren,updateElder,family_id))
                mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO rohinga(rohinga_name,age,sex,family_id,camp_no,black_listed) VALUES(%s,%s,%s,%s,%s,%s)''',(rohinga_name, age, sex, family_id, camp_no, black_listed))
            mysql.connection.commit()
            flash('A New Rohingya Entry is Added', 'success')
            familydata = int(family_id)
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM family WHERE family_id = %s", [familydata])
            familydata = cur.fetchone()
            rohingadata = lastrohinga()
            cur = mysql.connection.cursor()
            result1 = cur.execute("SELECT * FROM rohinga WHERE rohinga_id = %s", [rohingadata['rohinga_id']])
            rohingadata = cur.fetchone()
            return render_template('rohingainfo.html', rohingadata=rohingadata, familydata=familydata)
        else:
            if int(age) >= 18:
                cur.execute('''INSERT INTO family(camp_no,member_count,children,elder) VALUES(%s,%s,%s,%s)''',(camp_no, 1, 0, 1))
                mysql.connection.commit()
            else:
                cur.execute('''INSERT INTO family(camp_no,member_count,children,elder) VALUES(%s,%s,%s,%s)''',(camp_no, 1, 1, 0))
                mysql.connection.commit()
            result = cur.execute("SELECT family_id FROM family ORDER BY family_id DESC LIMIT 1")
            data = cur.fetchone()
            family_id = data['family_id']
            cur.execute('''INSERT INTO rohinga(rohinga_name,age,sex,family_id,camp_no,black_listed) VALUES(%s,%s,%s,%s,%s,%s)''',(rohinga_name, age, sex, family_id, camp_no, black_listed))
            mysql.connection.commit()
            flash('A New Rohingya Entry is Added', 'success')
            return redirect(url_for('rohingainfo'))
        

    return render_template('addrohinga.html', form=form)


@app.route('/adminregister', methods=['GET', 'POST'])
@is_logged_in
def adminregister():
    form = RegisterForm()
    if form.validate_on_submit():
        email = (form.email.data)
        password = sha256_crypt.encrypt(str(form.password.data))
        role = (form.role.data)
        print(email)
        print(password)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO login(email,password,role) VALUES(%s,%s,%s)''', (email, password, role))
        mysql.connection.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    else:
        return render_template('adminregister.html', form=form)





@app.route('/admin-adminlist')
@is_logged_in
def adminlist():
    ulist = []
    a = users()
    for i in a:
        ulist.append(i)

    print(ulist)
    return render_template('admin-adminlist.html', ulist=ulist)


@app.route('/rohingainfo')
@is_logged_in
def rohingainfo():
    familydata = lastrohingaFamily()
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM family WHERE family_id = %s", [familydata['family_id']])
    familydata = cur.fetchone()
    rohingadata = lastrohinga()
    cur = mysql.connection.cursor()
    result1 = cur.execute("SELECT * FROM rohinga WHERE rohinga_id = %s", [rohingadata['rohinga_id']])
    rohingadata = cur.fetchone()
    return render_template('rohingainfo.html', rohingadata=rohingadata, familydata=familydata)



@app.route('/education')
def education():
    ulist = []
    a = schoolinfo()
    for i in a:
        ulist.append(i)

    print(ulist)
    return render_template('education.html', ulist=ulist)



@app.route('/itemrecord')
def itemrecord():
    ulist = []
    a = itemRecords()
    for i in a:
        ulist.append(i)

    print(ulist)
    return render_template('itemrecord.html', ulist=ulist)


@app.route('/edititem/<string:idd>/', methods=['GET', 'POST'])
@is_logged_in
def edititem(idd):
    print(idd)
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM items where type=%s''',[idd])
    mysql.connection.commit()
    return redirect(url_for('aidcategory'))



@app.route('/camps', methods=['GET', 'POST'])
@is_logged_in
def camps():
    form = campss()
    if form.validate_on_submit():
        camp_name = (form.camp_name.data)
        camp_no = (form.camp_no.data)
        sanitation = int(form.sanitation.data)
        tubewell = int(form.tubewell.data)
        address = (form.address.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO camps(camp_name,camp_no,address,sanitation,tubewell) VALUES(%s,%s,%s,%s,%s)''',(camp_name, camp_no,address, sanitation, tubewell))
        mysql.connection.commit()
        flash('You have successfully registerd a new CAMP', 'success')
        return redirect(url_for('deshboard'))
    else:
        return render_template('camp.html', form=form)



@app.route('/addschool', methods=['GET', 'POST'])
@is_logged_in
def addschool():
    form = addschoolForm()
    if form.validate_on_submit():
        name = (form.name.data)
        camp_no = (form.camp_no.data)
        teacher_count = (form.teacher_count.data)
        student_count = (form.student_count.data)
        student_capacity = (form.student_capacity.data)
        contact = (form.contact.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO school(name,camp_no,teacher_cont,student_count,student_capacity,contact) VALUES(%s,%s,%s,%s,%s,%s)''',(name, camp_no, teacher_count, student_count, student_capacity, contact))
        mysql.connection.commit()

        flash('You have successfully registerd a new school', 'success')
        return redirect(url_for('deshboard'))
    else:
        return render_template('addschool.html', form=form)


@app.route('/doctor', methods=['GET', 'POST'])
@is_logged_in
def doctor():
    form = Doctor()
    if form.validate_on_submit():
        doctor_name = (form.doctor_name.data)
        department = (form.department.data)
        camp_no = (form.camp_no.data)
        contact = (form.contact.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO doctor(doctor_name,department,camp_no,contact) VALUES(%s,%s,%s,%s)''',(doctor_name, department, camp_no, contact))
        mysql.connection.commit()

        flash('You have successfully registerd a new Doctor', 'success')
        return redirect(url_for('deshboard'))
    else:
        return render_template('doctor.html', form=form)

@app.route('/patient', methods=['GET', 'POST'])
@is_logged_in
def patient():
    form = Patientt()
    if form.validate_on_submit():
        patient_id = (form.patient_id.data)
        doctor_id = (form.doctor_id.data)
        department = (form.department.data)
        disease = (form.disease.data)
        start_date = (form.start_date.data)
        end_date = (form.end_date.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO patient(patient_id,disease,department,start_date,end_date,doctor_id) VALUES(%s,%s,%s,%s,%s,%s)''',(patient_id,disease, department, start_date, end_date,doctor_id))
        mysql.connection.commit()

        flash('You have successfully registerd a new Patient', 'success')
        return redirect(url_for('deshboard'))
    else:
        return render_template('patient.html', form=form)


@app.route('/aid', methods=['GET', 'POST'])
@is_logged_in
def aid():
    form = aidd()
    if form.validate_on_submit():
        family_id = (form.family_id.data)
        typee = (form.typee.data)
        amount = (form.amount.data)
        expire = (form.expire.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO aid(family_id,type,amount,expire) VALUES(%s,%s,%s,%s)''',(family_id,typee,amount,expire))
        mysql.connection.commit()

        flash('You have successfully registerd', 'success')
        return redirect(url_for('deshboard'))
    else:
        return render_template('aid.html', form=form)


@app.route('/aidcategory', methods=['GET', 'POST'])
@is_logged_in
def aidcategory():
    form = aidcategoryy()
    if form.validate_on_submit():
        typee = (form.typee.data)
        amount = (form.amount.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO items(type,amount) VALUES(%s,%s)''',(typee,amount))
        mysql.connection.commit()
        flash('You have successfully added a new record', 'success')
        return redirect(url_for('deshboard'))
    else:
        return render_template('aidcat.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candid = (request.form['password'])

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM login WHERE email = %s", ([email]))
        print(result)
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            if sha256_crypt.verify(password_candid, password):
                session['logged_in'] = True
                session['username'] = email
                session['role'] = data['role']
                return render_template('admin-deshboard.html')
            else:
                error = 'PASSWORD NOT MATCHED'
                return render_template('login.html', error=error)
        else:
            error = 'NO USER'
            return render_template('login.html', error=error)
        cur.closs()
    else:
        return render_template('login.html')


@app.route('/searchrohinga', methods=['GET', 'POST'])
@is_logged_in
def searchrohinga():
    if request.method == 'POST':
        Rid = int(request.form['id'])
        cur = mysql.connection.cursor()
        result1 = cur.execute("SELECT * FROM rohinga WHERE rohinga_id = %s", ([Rid]))
        
        rohingadata = cur.fetchone()
        Fid = int(rohingadata['family_id'])
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM family WHERE family_id = %s", ([Fid]))
        familydata = cur.fetchone()
        return render_template('rohingainfo.html', rohingadata=rohingadata, familydata=familydata)

    return render_template('searchrohinga.html')

@app.route('/events', methods=['GET', 'POST'])
def events():
    form = event()
    if form.validate_on_submit():
        event_name = (form.event_name.data)
        sector = (form.sector.data)
        contact = (form.contact.data)
        startdate = (form.startdate.data)
        enddate = (form.enddate.data)
        contact = (form.contact.data)
        Description = (form.Description.data)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO events(event_name,sector,contact,start_date,end_date,checked,Description) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(event_name, sector, contact, startdate, enddate, 0,Description))
        mysql.connection.commit()
        flash('You have successfully registerd a new Event', 'success')
        return redirect(url_for('home'))

    else:
        return render_template('events.html', form=form)


@app.route('/pendingevents')
@is_logged_in
def pendingeventss():
    ulist = []
    a = pendingevents()
    for i in a:
        ulist.append(i)
    print(ulist)
    return render_template('pendingevents.html', ulist=ulist)


@app.route('/approveevents/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def approveevents(id):
    form = appevent()
    url=''
    print(url)
    if form.validate_on_submit():
        administrator = (form.administrator.data)
        volunteer = (form.volunteer.data)
        checked = (form.checked.data)
        event_id = str(id)
        print(id)
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE events SET administrator=%s, volunteer=%s, checked=%s WHERE event_id=%s""",(administrator,volunteer,checked,event_id))
        mysql.connection.commit()
        flash('You have successfully registerd in a new Event', 'success')
        return redirect(url_for('home'))

    else:
        return render_template('approveevent.html', form=form, url=url)


@app.route('/events/<string:id>/', methods=['GET', 'POST'])
def singleevent(id):
    form = volunteer()
    url=''
    print(url)
    if form.validate_on_submit():
        event_name = (form.name.data)
        department = (form.department.data)
        contact = (form.contact.data)
        check_in = (form.check_in.data)
        check_out = (form.check_out.data)
        event_id = str(id)
        print(id)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO volunteer(event_id,name,department,contact,check_in,check_out,availability) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(event_id,event_name, department, contact, check_in, check_out, 0))
        mysql.connection.commit()
        result = cur.execute("SELECT volunteer_id FROM volunteer ORDER BY volunteer_id DESC LIMIT 1")
        data = cur.fetchone()
        volunteer_id = data['volunteer_id']
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO serves(event_id,volunteer_id) VALUES(%s,%s)''',(event_id,volunteer_id))
        mysql.connection.commit()
        if department=="Doctor" or department=="Teacher":
            cur = mysql.connection.cursor()
            cur.execute("""UPDATE events SET administrator=administrator-1 WHERE event_id=%s""",(event_id))
            mysql.connection.commit()
        else:
            cur = mysql.connection.cursor()
            cur.execute("""UPDATE events SET volunteer=volunteer-1 WHERE event_id=%s""",(event_id))
            mysql.connection.commit()
        flash('You have successfully registerd in a new Event', 'success')
        return redirect(url_for('home'))

    else:
        return render_template('volunteer.html', form=form, url=url)


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
