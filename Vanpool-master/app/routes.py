from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app import app, db, login_manager
from app.forms import LoginForm, RegistrationForm, RegisterVehicleForm, AddDriverForm, AssignDriverForm, DestinationForm
from app.models import User, Vehicle, ACCESS
from mapclass import map


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    form = DestinationForm()
    b=map("b")
    universityLocation=b.getlocationdes("the University of Iowa")
    startMap = b.getMapUrl(universityLocation[0],universityLocation[1])
    temp = ''

    if form.is_submitted():
         a = map("a")
         userLocation = a.getlocationmyself()


         # origin location
         # des location
         destination = form.destination.data
         dest = str(destination)
         destinationLocation=a.getlocationdes(dest)
         temp = a.des(userLocation[0], userLocation[1],destinationLocation[0], destinationLocation[1])
         start=a.getlocationmyself()
         startLocation=('%s , %s')%(start[0] ,start[1])
         info=a.mapinfo(startLocation,dest)
         distance = info['rows'][0].get('elements')[0].get('distance').get('text')
         time = info['rows'][0].get('elements')[0].get('duration').get('text')
         flash("Your destination is:%s" % dest)
         flash("estimate distance:%s" % distance)
         flash("estimate time:%s" % time)
         d=a.mapinfo("University of Iowa",startLocation)
         driverDistance=d['rows'][0].get('elements')[0].get('distance').get('text')
         driverTime=d['rows'][0].get('elements')[0].get('duration').get('text')
         flash("Distance of driver and you:%s" % driverDistance)
         flash("driver will arrive around:%s" % driverTime)
         # destination = form.destination.data
         # start = form.start.data
         # dest = str(destination)
         # strt = str(start)
         # a.getlocationmyself()
         # flash("Your are from:%s" % strt)
         # flash("to:%s" % dest)
         # j = a.mapinfo(strt,dest)
         # distance=j['rows'][0].get('elements')[0].get('distance').get('text')
         # time=j['rows'][0].get('elements')[0].get('duration').get('text')
         # flash("estimate distance:%s" % distance)
         # flash("estimate time:%s" % time)
         # d=a.mapinfo("University of Iowa",strt)
         # driverDistance=d['rows'][0].get('elements')[0].get('distance').get('text')
         # driverTime=d['rows'][0].get('elements')[0].get('duration').get('text')
         # flash("Distance of driver and you:%s" % driverDistance)
         # flash("driver will arrive around:%s" % driverTime)
         return render_template('index.html', form = form, value = temp,data = "a223jsd")


    #return render_template('index.html', title='Home', form=form)
    return render_template('index.html', title='Home', form=form, value = startMap)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data, access=ACCESS[request.form['role']])
        user.set_password(form.password.data)
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/driver_management', methods=['GET', 'POST'])
def driver_management():
    users = User.query.all()
    return render_template('driver_management.html', title='Driver Management', users=User.query.all())


@app.route('/add_drivers', methods=['GET', 'POST'])
def add_drivers():
    form = AddDriverForm()
    if form.is_submitted():
        db.session.query(User).filter(User.id == request.form.get('drivers')).update({User.access: User.access + 1})
        db.session.commit()
        flash("Successfully added " + str(User.query.get(request.form.get('drivers')).username) + " as a driver!")
        return redirect(url_for('index'))
    return render_template('add_drivers.html', title='Add Drivers', form=form, users=User.query.all())


@app.route('/fleet_management', methods=['GET', 'POST'])
def fleet_management():
    return render_template('fleet_management.html', title='Fleet Management', users=User.query.all(),
                           vehicles=Vehicle.query.all())


@app.route('/assign_drivers', methods=['GET', 'POST'])
def assign_drivers():
    form = AssignDriverForm()
    if form.is_submitted():
        """
        vehic = Vehicle.query.all()
        for v in vehic:
            if v.driver.username == User.query.get(request.form.get('drivers')).username:
                db.session.delete(v)
        db.session.commit()
        """
        vehic = Vehicle.query.all()
        for v in vehic:
            if v.driver == User.query.get(request.form.get('drivers')):
                v.driver = None
        vehicle = Vehicle.query.get(request.form.get('vehicles'))
        vehicle.driver = User.query.get(request.form.get('drivers'))
        """
        vehicle = Vehicle(model=Vehicle.query.get(request.form.get('vehicles')).model,
                          make=Vehicle.query.get(request.form.get('vehicles')).make,
                          color=Vehicle.query.get(request.form.get('vehicles')).color,
                          driver_id=request.form.get('drivers'),
                          driver=User.query.get(request.form.get('drivers')))
                          """
        db.session.commit()
        flash("You have successfully registered a vehicle!")
        return redirect(url_for('index'))
    return render_template('assign_drivers.html', title='Assign Drivers', form=form, users=User.query.all(),
                           vehicles=Vehicle.query.all())


@app.route('/register_vehicle', methods=['GET', 'POST'])
def register_vehicle():
    """Admin Role"""
    form = RegisterVehicleForm()
    if form.is_submitted():
        vehicle = Vehicle(model=form.model.data,
                          make=form.make.data,
                          color=form.color.data,
                          license_plate=form.license_plate.data
                          )
        """
        vehicle = Vehicle(model=form.model.data, make=form.make.data, color=form.color.data,
                          driver_id=request.form.get('drivers'),
                          driver=User.query.get(request.form.get('drivers')))
                          """

        db.session.add(vehicle)
        db.session.commit()
        flash("You have successfully registered a vehicle!")
        return redirect(url_for('index'))
    return render_template('register_vehicle.html', title='Register Vehicle', form=form,
                           users=User.query.all(), vehicles=Vehicle.query.all())


@app.route('/show_users', methods=['GET', 'POST'])
def show_users():
    return render_template('show_users.html', title="Show Users", users=User.query.all(), v=Vehicle.query.all())


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


# @app.route('/mapUrl', methods=['GET', 'POST'])
# def mapUrl():
#     a = map("a")
#     return a.getMapUrl(a.lat, a.lng)


def clearVehicle(u):
    v = u.vehicle.all()
    db.session.delete(v)
    db.session.commit()
