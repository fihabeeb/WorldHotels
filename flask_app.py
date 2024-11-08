# - 22066955 Fadil Idris
import mysql.connector, dbconnect
from flask import Flask, session, render_template, request, url_for, redirect, flash
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta, date
from functools import wraps


app = Flask(__name__) #instantiating flask app

app.secret_key = 'Spider-Man'  #secret key for the sessions
DB_NAME = 'World_Hotels'

@app.route('/')
@app.route('/index')
@app.route('/home')
def main_Page():
	connect = dbconnect.getConnection()
	if connect != None and connect.is_connected():
		print('Yay')
		cursor = connect.cursor()
		SQL = 'SELECT City FROM HotelInformation;'
		cursor.execute(SQL)
		print("Done")
		output = cursor.fetchall()
		cursor.close()
		connect.close()
		print("Opening Main page")
		return render_template("main_Page.html", resultset = output, usertype = 'none')
	else:
		print('Cant connect to database')
		return 'DB Connection Error'




@app.route('/login' , methods = ['POST','GET'])
def login_Page():

	errrrr = None
	print("Opening Login Page")
	if request.method == 'POST':
		try:
			print("Opening Registration Page")
			emailname = request.form['user_Email']
			psswrd = request.form['user_Password']
			print("trying")
			database = dbconnect.getConnection()
			if database.is_connected():
				cursor_obj = database.cursor()
				primarysql = "SELECT Email FROM UserInformation"
				cursor_obj.execute(primarysql)
				print(cursor_obj)
				rows = cursor_obj.fetchall()
				for x in rows:
					print(x[0])
					print(emailname)
					if x[0] == emailname:
						print("Email Found")
						sql2 = "SELECT User_Password, Privilages, Name, userinfoid, email FROM UserInformation;"
						args = emailname
						found_right_pass = False
						cursor_obj.execute(sql2)
						print(cursor_obj)
						valz = cursor_obj.fetchall()
						print(valz)
						print(psswrd)
						for x in range (len(valz)):
							output = sha256_crypt.verify(psswrd, valz[x][0])
							if output and valz[x][4] == emailname:
								found_right_pass = True
								Privilage = valz[x][1]
								usersname = valz[x][2]
								userid = valz[x][3]
								print("Privilages: " + Privilage)
								print("Usersname: " + usersname)
								print(found_right_pass)
								break
						print("checked")
						if found_right_pass:
							print("Login Successful")

							session['logged_in'] = True     #set session variables
							session['email'] = request.form['user_Email']
							session['usertype'] = str(Privilage)
							session['username'] = usersname
							session['userid'] = userid

							#i dont know how to fix this: flash('Login Successful')
							#insert login code here
							return redirect(url_for('main_Page_Login', username = session['username'], usertype = session['usertype']))
							return render_template("main_Page.html",\
							 usertype=usersname)
						else:
							print("wong pass wod")
							errrrr = 'Invalid Username or Password'
							#return redirect(url_for('login_Page'))
					#else:
					 #   print('wrongemai')
					  #  errrrr = 'Invalid Username or Password'
					   # cursor_obj.close()
		except:
			print('Error')
			#database.rollback()
			#msg += " insertion error"
			#print(msg)
		finally:
			print("done")
	else:
		print("Not Post")
		#return "Not Post"
	return render_template("login_Page.html", error = errrrr)

@app.route('/register' , methods = ['POST','GET'])
def register_Page():
	errrrr = None
	if request.method == 'POST':
		try:
			print("Opening Registration Page")
			emailname = request.form['user_Email']
			frstname = request.form['user_First_Name']
			lstname = request.form['user_Last_Name']
			psswrd = request.form['user_Password']
			hash_value = sha256_crypt.hash(str(psswrd))
			#consider checking if the user already exists right here
			print("trtying")
			msg = emailname + " " + frstname + " " + lstname + " " + hash_value
			print(msg)
			database = dbconnect.getConnection()
			if database.is_connected():
				cursor_obj = database.cursor()
				primarysql = "INSERT INTO UserInformation (Name, Surname, Email, User_Password) \
				VALUES (%s, %s, %s, %s)"
				#secondarysql = "SELECT customerinfoid FROM CustomerInfo ORDER BY customerinfoid DESC LIMIT 1;"
				#use sql to get the most recent customer info id and place it down there
				#try to let it fly first tho
				#sql = "INSERT INTO customerlogin(Email, User_Password, CustomerInfoId)"
				print(cursor_obj)
				input = (frstname, lstname, emailname, hash_value) #Protected against sql injection
				cursor_obj.execute(primarysql, input)
				database.commit()
				#cursor_obj.execute(secondarysql)
				#rows = cursor_obj.fetchall()
				#for x in rows:
				#    print(x)
				cursor_obj.close()
				msg += " Added"
				#session variables
				session['logged_in'] = True
				session['username'] = frstname
				session['email'] = emailname
				session['usertype'] = 'standard'   #default all users are standard
				errrrr = 'Registration Successful'
				return redirect(url_for('login_Page'))
			print(msg)
		except Exception as error:
			print('Error')
			errrrr = 'Registration Error'
			database.rollback()
			msg += " insertion error"
			#print(msg)
			#return f'Error occurred: {error}'
		finally:
			print("done")
	else:
		print("Not Post")
		#return "Not Post"
	return render_template("register_Page.html", error = errrrr)

@app.route('/aboutus')
def about_Us():
	print("Opening about us page")
	return render_template("about_Us.html", usertype = session['usertype'], username = session['username'])

@app.route('/contactus')
def contact_Us():
	print("opening contact us page")
	return render_template("contact_Us.html", usertype = session['usertype'], username = session['username'])



#Start of Wrappers-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			print("You need to login first")
			#return redirect(url_for('login', error='You need to login first'))
			return render_template('login_Page.html', error='You need to login first')
	return wrap


def admin_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if ('logged_in' in session) and (session['usertype'] == 'admin'):
			return f(*args, **kwargs)
		else:
			print("You need to login first as admin user")
			return render_template('login_Page.html', error='You need to login first as admin user', usertype = session['usertype'], username = session['username'])
	return wrap

@app.route("/logout/")
@login_required
def logout():
	session.clear()    #clears session variables
	print("You have been logged out!")
	return redirect(url_for('main_Page', error='You have been logged out'))




@app.route('/index/<usertype>/<username>')
@app.route('/home/<usertype>/<username>')
@login_required
def main_Page_Login(usertype, username):
	connect = dbconnect.getConnection()
	if connect != None and connect.is_connected():
		print('Yay')
		cursor = connect.cursor()
		SQL = 'SELECT City FROM HotelInformation;'
		cursor.execute(SQL)
		print("Done")
		output = cursor.fetchall()
		cursor.close()
		connect.close()
		print("Opening Main page")
		return render_template("main_Page.html", resultset = output, username = session['username'], usertype = session['usertype'])
	else:
		print('Cant connect to database')
		return 'DB Connection Error'







@app.route('/admin_Tools/<checker>', methods = ['POST','GET'])
@login_required
@admin_required
def admin_Tools(checker):
	todo = None
	total_earnings = 0
	connect = dbconnect.getConnection()
	cursor = connect.cursor()
	if (checker == "True"):
		todo = request.form['bookingchange']
	if (checker == "TrueA"):

		user_to_update_for = request.form['pass_update_user_id']
		password_to_update_to = request.form['user_pass_update_new_password']
		password_to_update_to = sha256_crypt.hash(password_to_update_to)
		cursor.execute('UPDATE UserInformation SET User_Password = %s WHERE UserInfoId = %s;',\
				  (password_to_update_to, user_to_update_for))
		connect.commit()
		print("User password is updates successfully")
		flash("User password is updates successfully")
	if (checker == "TrueB"):
		newcity = request.form['new_city']
		stdcap = request.form['new_std_room_capacity']
		doubcap = request.form['new_double_room_capacity']
		famcap = request.form['new_family_room_capacity']
		peakseason = request.form['new_peak_season_pricing']
		offseason = request.form['new_off_season_pricing']
		cursor.execute('INSERT INTO HotelInformation (City, Standared_Room_Capacity, Double_Room_Capacity, Family_Room_Capacity, PeakSeasonPrice, OffSeasonPrice) VALUES (%s, %s, %s, %s, %s, %s);', \
				 (newcity, stdcap, doubcap, famcap, peakseason, offseason))
		connect.commit()
		print("New Hotel Successfully added")
		flash("New Hotel Successfully added")

	if (checker == "TrueC"):
		citodel = request.form['city_to_delete']
		cursor.execute('DELETE FROM HotelInformation WHERE City = %s;', (citodel,))
		connect.commit()
		print("Hotel successfully deleted")
		flash("Hotel successfully deleted")

	if (checker == "TrueD"):
		newcity = request.form['new_city']
		stdcap = request.form['new_std_room_capacity']
		doubcap = request.form['new_double_room_capacity']
		famcap = request.form['new_family_room_capacity']
		peakseason = request.form['new_peak_season_pricing']
		offseason = request.form['new_off_season_pricing']
		cursor.execute('UPDATE HotelInformation SET City = %s, Standared_Room_Capacity = %s, Double_Room_Capacity = %s, Family_Room_Capacity = %s, PeakSeasonPrice = %s, OffSeasonPrice = %s WHERE City = %s;', \
				  (newcity, stdcap, doubcap, famcap, peakseason, offseason, newcity))
		connect.commit()
		print("Hotel data suuccessfully updated")
		flash("Hotel data suuccessfully updated")

	if (todo == "report"):
		#to generate a sales report, add all the total charges up
		SQL = 'Select TotalCharges, PaymentStatus, BookingID FROM Billings'
		cursor.execute(SQL)
		print("Done")
		moneyoutput = cursor.fetchall()
		for x in moneyoutput:
			if x[1] == "Payed" or x[1] == "Extra Payement":
				total_earnings += float(x[0])
			else:
				total_earnings -= float(x[0])

		#to get it for each hotel, do the think with; the booking table

		pass
	SQL = 'SELECT UserInfoId, Name FROM UserInformation;'
	cursor.execute(SQL)
	print("Done")
	output = cursor.fetchall()

	SQL2 = 'SELECT City FROM HotelInformation;'
	cursor.execute(SQL2)
	print("Done")
	output2 = cursor.fetchall()
	cursor.close()
	connect.close()
	return render_template('admin_Tools.html', username = session['username'], usertype = session['usertype'], \
						todo = todo, resultset = output, cityset = output2, total_earnings = total_earnings)



@app.route('/generateuserrecord/')
@login_required
def generate_user_record():
	print('User records')
	#here you can generate required data as per business logic
	return """
		<h1> this is User record for user {} </h1>
		<a href='/userfeatures')> Go to User Features page </a>
	""".format(session['username'])



@app.route('/generateadminreport/')
@login_required
@admin_required
def generate_admin_report():
	print('admin reports')
	#here you can generate required data as per business logic
	return """
		<h1> this is admin report for {} </h1>
		<a href='/adminfeatures')> Go to Admin Features page </a>
	""".format(session['username'])

@app.route('/booking_start/', methods = ['POST', 'GET'])
@login_required
def booking_start():
	print(request.method)
	discount = 0
	if request.method == 'POST':
		offseasondays = 0
		peakseasondays = 0
		peakmonths = [4, 5, 6, 7, 8, 11, 12]
		checkindate = request.form['user_Check_In_Date']
		accCity = request.form['city_list']
		checkoutdate = request.form['user_Check_Out_Date']
		nooofguests = request.form['num_Adults']
		noofchilds = request.form['num_Children']
		room_type = request.form['rooms']
		noofnights = datetime.strptime(checkoutdate, '%Y-%m-%d') - datetime.strptime(checkindate, '%Y-%m-%d')
		today = datetime.today()
		daystocheckin = (datetime.strptime(checkindate, '%Y-%m-%d') - today).days
		print(f'bruh{daystocheckin}')
		if daystocheckin >= 80:
			discount = 30
		elif daystocheckin >= 60 and daystocheckin <= 79:
			discount = 20
		elif daystocheckin >= 45 and daystocheckin <= 59:
			discount = 10
		print("WOO0")
		print(noofnights)
		print(datetime.strptime(checkoutdate, '%Y-%m-%d').month)
		print(datetime.strptime(checkindate, '%Y-%m-%d').month)
		for j in range (noofnights.days):
			j = datetime.strptime(checkindate, '%Y-%m-%d') + timedelta(days=j)
			print(j.month)
			if j.month in peakmonths:
				peakseasondays += 1
			else:
				offseasondays += 1
		print("peakseason: " + str(peakseasondays))
		print("offseason: " + str(offseasondays))
		lookupdata = [accCity, checkindate, checkoutdate, offseasondays, peakseasondays, nooofguests, noofchilds, noofnights.days, discount, int(-discount) / 100]
		conn = dbconnect.getConnection()
		if conn != None:
			print('MYSQL Connection is likeee')
			dbcursor = conn.cursor()
			if room_type != "room_Size_Any":
				room_type_insert =  0
				if room_type == "room_Size_Single":
					room_type_insert = "single"
				elif room_type == "room_Size_Double":
					room_type_insert = "double"
				elif room_type == "room_Size_Family":
					room_type_insert = "family"
				dbcursor.execute('SELECT RoomNumber FROM Room WHERE HotelId = %s and RoomType = %s;', (accCity, room_type_insert, ))
				rowsA = dbcursor.fetchall()
				print (rowsA)
				print("LEN ROWSA")
				print(len(rowsA))
				#After getting stuff from HotelInformation, subtract the friggin total length by this to get actual rooms remaining
				number_of_single_rooms = len(rowsA)
				number_of_double_rooms = len(rowsA)
				number_of_family_rooms = len(rowsA)
				print("TYTPE")
				print(type(number_of_single_rooms))
			elif room_type == "room_Size_Any":
				dbcursor.execute('SELECT RoomNumber FROM Room WHERE HotelId = %s and RoomType = %s;', (accCity, "single", ))
				rowsA = dbcursor.fetchall()
				print (rowsA)
				#print(rowsA[0])
				print(len(room_type))
				print("Remaining rooms: ")
				print(len(room_type))
				number_of_single_rooms = len(rowsA)
				dbcursor.execute('SELECT RoomNumber FROM Room WHERE HotelId = %s and RoomType = %s;', (accCity, "double", ))
				rowsA = dbcursor.fetchall()
				print (rowsA)
				#print(rowsA[0])
				print(len(room_type))
				print("Remaining rooms: ")
				print(len(room_type))
				number_of_double_rooms = len(rowsA)
				dbcursor.execute('SELECT RoomNumber FROM Room WHERE HotelId = %s and RoomType = %s;', (accCity, "family", ))
				rowsA = dbcursor.fetchall()
				print (rowsA)
				#print(rowsA[0])
				print(len(room_type))
				print("Remaining rooms: ")
				print(len(room_type))
				number_of_family_rooms = len(rowsA)


			dbcursor.execute('SELECT * FROM HotelInformation WHERE City = %s;', (accCity,))
			rows = dbcursor.fetchall()
			print (rows)
			datarows = []
			for row in rows:
				data = list(row)
				fare = (int(row[6])) * int(offseasondays)
				fare += (int(row[5])) * int(peakseasondays)
				print(fare)
				data.append(fare)
				datarows.append(data)
			dbcursor.close()
			conn.close()
			print(datarows)
			number_of_single_rooms = float(datarows[0][2]) - number_of_single_rooms
			number_of_double_rooms = float(datarows[0][3]) - number_of_double_rooms
			number_of_family_rooms = float(datarows[0][4]) - number_of_family_rooms
			return render_template('booking_start.html', resultset=datarows, lookupdata=lookupdata, room_type = room_type, usertype = session['usertype'], username = session['username'],\
						  number_of_single_rooms = number_of_single_rooms, number_of_double_rooms = number_of_double_rooms, number_of_family_rooms = number_of_family_rooms)
		else:
			print('DB connection Error')
			return redirect(url_for('index'))
	else:
		return "CRY EMOJI"






@app.route ('/booking_confirm/', methods = ['POST', 'GET'])
@login_required
def booking_confirm():
	bookingdata = []
	cardnumber = 0
	if request.method == 'POST':
		#print('booking confirm initiated')
		acccity = request.form['acccity']
		checkindate = request.form['checkindate']
		checkoutdate = request.form['checkoutdate']
		noofguests = request.form['noofguests']

		estimatedfare = request.form['bookingchoice']
		room_type = request.form['roomtype']

		offseasondays = request.form['offseasondays']
		peakseasondays = request.form['peakseasondays']
		payement_status = "Payed"
		#totalfare = request.form['totalfare']
		#print('Testing total fare: ', totalfare)
		#address = request.form['accaddress']
		#smoking = request.form['smoking']
		#features = request.form['features']
		totalfare = ''
		address = ''
		smoking = ''
		features = ''
		noofnights = datetime.strptime(checkoutdate, '%Y-%m-%d') - datetime.strptime(checkindate, '%Y-%m-%d')
		#temp_number = 2
		conn = dbconnect.getConnection()
		#value_from_radio = str(value_from_radio).strip("[")
		#value_from_radio = str(value_from_radio).strip("]")
		#estimatedfare = ""
		#room_type = ""
		#gear = 1
		#print(estimatedfare)
		#for i in value_from_radio:
		#	if i != ",":
		#		if gear == 1:
		#			estimatedfare = estimatedfare + i
		#		elif gear == 2:
		#			room_type = room_type + i
		#	else:
		#		gear = 2
		print(estimatedfare)
		#room_type = str(room_type).strip(" ")
		print(room_type)



		cardnumber = request.form['cardnumber']

		#you can also get customer details entered in the form

		bookingdata = [estimatedfare, acccity, checkindate, checkoutdate, noofguests, estimatedfare, address, smoking, features, noofnights.days]

		#room_number_string = acccity[0] + acccity[1] + acccity[2] + room_type[0] + room_type[1] + room_type[2] + "1"

		#Now we need to save booking data in DB
		conn = dbconnect.getConnection()
		if conn != None:    #Checking if connection is None
			print('MySQL Connection is established')
			dbcursor = conn.cursor()    #Creating cursor object
			room_number_int_value = 1





			dbcursor.execute('SELECT HotelInformationID FROM HotelInformation WHERE City = %s;', (acccity,))
			rows = dbcursor.fetchall()
			print (rows)
			print (rows[0][0])
			hotel_info_id = rows[0][0]


			dbcursor.execute('SELECT RoomNumber FROM Room WHERE HotelID = %s AND Roomtype = %s;', (hotel_info_id,room_type, ))
			rows = dbcursor.fetchall()
			print("Rows:")
			print(rows)
			for j in rows:
				print(f"J {j[0]}")
				print("J-1:")
				print(j[0][-1])
				print(room_number_int_value)
				if room_number_int_value != int(j[0][-1]):
					break
				else:
					room_number_int_value += 1

			room_number_string = acccity[0] + acccity[1] + acccity[2] + room_type[0] + room_type[1] + room_type[2] + str(room_number_int_value)


			conn.commit()

			dbcursor.execute('INSERT INTO Room (HotelID, RoomNumber, RoomType) VALUES \
				(%s, %s, %s);', (hotel_info_id, room_number_string, room_type))
			print('Booking statement executed successfully.')
			conn.commit()

			dbcursor.execute('SELECT RoomTableID FROM Room ORDER BY RoomTableID DESC LIMIT 1;')
			rows = dbcursor.fetchall()
			print (rows)
			print (rows[0][0])
			room_id = rows[0][0]


			user_information_id = session['userid']
			dbcursor.execute('INSERT INTO BookingTable (RoomTableID, CheckInDate, CheckOutDate, HotelInformationID, UserInformationID) VALUES \
				(%s, %s, %s, %s, %s);', (room_id, checkindate, checkoutdate, hotel_info_id, user_information_id))


			dbcursor.execute('SELECT BookingId FROM BookingTable ORDER BY BookingId DESC LIMIT 1;')
			rows = dbcursor.fetchall()
			print (rows)
			print (rows[0][0])
			booking_latest_id = rows[0][0]


			dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', (str(float(estimatedfare) / (float(offseasondays) + float(peakseasondays))), estimatedfare, payement_status, booking_latest_id))

			print('Booking statement executed successfully.')
			conn.commit()

			#As bookingid is autogenerated so we can get it by running following SELECT
			dbcursor.execute('SELECT LAST_INSERT_ID();')
			rows = dbcursor.fetchone()
			bookingid = rows[0]
			bookingdata.append(bookingid)

			#Slicing card number as displaying full card number is a security risk
			cardnumber = cardnumber[-4:-1]
			print(cardnumber)
			dbcursor.execute
			dbcursor.close()
			conn.close() #Connection must be closed

		else:
			print('DB connection Error')
			return redirect(url_for('index'))
	return render_template('booking_confirm.html', resultset=bookingdata, cardnumber=cardnumber, usertype = session['usertype'], username = session['username'])

@app.route('/booking_tools_1/', methods = ['POST', 'GET'])
@login_required
def booking_tools_1():
	tool_action = request.form['bookingchange']
	tool_table_id = request.form['id']
	delete_confirm = request.form['deleteconfirmation']
	checkindateval = request.form['checindatethang']
	checkoutdateval = request.form['checkoutdatethang']
	hotel_name = request.form['hotel_name']
	user_id = None
	print(tool_table_id)
	return render_template('booking_tools_1.html', username = session['username'], \
						 usertype = session['usertype'], form_action = tool_action, tool_table_id = tool_table_id, \
							checkindateval = checkindateval, checkoutdateval = checkoutdateval, user_id=user_id, hotel_name = hotel_name)




@app.route('/booking_tools/<forms>', methods = ['POST', 'GET'])
@login_required
def booking_tools(forms):
		tool_action = 0
		tool_table_id = 0
		delete_confirm = 0
		checkindateval = 0
		checkoutdateval = 0
		hotel_name = 0
		if forms == True:
			tool_action = request.form['bookingchange']
			tool_table_id = request.form['id']
			delete_confirm = request.form['deleteconfirmation']
			checkindateval = request.form['checindatethang']
			checkoutdateval = request.form['checkoutdatethang']
			hotel_name = request.form['hotel_name']
		user_id = None
		#Now we need to save booking data in DB
		conn = dbconnect.getConnection()
		print('MySQL Connection is established')
		dbcursor = conn.cursor()
		print('create / amend records / delete records / generate reports')
		#records from database can be derived, updated, added, deleted
		#user login can be checked..
		print ('Welcome ', session['username'], ' as ', session['usertype'])

		dbcursor.execute('SELECT UserInfoId FROM UserInformation WHERE Name = %s;', (session['username'],))
		rows = dbcursor.fetchall()
		print (rows[0])
		user_id = rows[0][0]
		dbcursor.execute('SELECT * FROM BookingTable WHERE UserInformationID = %s and Status <> %s;', (user_id, "Cancelled"))
		rows2 = dbcursor.fetchall()
		datarows = []
		for row in rows2:
			data = list(row)
			datarows.append(data)
		dbcursor.close()
		conn.close()
		print(datarows)

		return render_template('booking_tools.html', resultset=datarows, username = session['username'], \
						 usertype = session['usertype'], form_action = tool_action, tool_table_id = tool_table_id, \
							checkindateval = checkindateval, checkoutdateval = checkoutdateval, user_id=user_id, hotel_name = hotel_name)




@app.route('/update_step/<forms>/<type>', methods = ['POST', 'GET'])
@login_required
def update_step(forms, type):
		cardnumber = 954994941
		refund_activate = 0
		extra_pay = ""
		fare_vale = 0
		checkindate = 0
		checkoutdate = 0
		tool_table_id = 0
		hotel_name = 0
		pay_us = 0
		fare = 0
		old_price = 0
		total_new_fare = 0
		conn = dbconnect.getConnection()
		dbcursor = conn.cursor()
		print('MySQL Connection is established')
		if forms == "True":
			tool_table_id_2 = request.form['tool_table_id_2']
			cardnumber = request.form['cardnumber']
			if type == "refund":
				refund_activate = request.form['refund_activate']
			elif type == "extra":
				extra_pay = request.form['extra_pay']
			fare_vale = request.form['fare_value']
		bookingdata = []
		if forms == "False":
			checkindate = request.form['user_Check_In_Date']
			tool_table_id = request.form['tool_table_id']
			checkoutdate = request.form['user_Check_Out_Date']
			hotel_name = request.form['hotel_name']
			dbcursor.execute('SELECT TotalCharges FROM Billings WHERE BookingID = %s;', (tool_table_id,))
			rows2 = dbcursor.fetchall()

			for x in rows2:
				old_price +=float(x[0])


			peakseasondays = 0
			offseasondays = 0
			peakmonths = [4, 5, 6, 7, 8, 11, 12]
			noofnights = datetime.strptime(checkoutdate, '%Y-%m-%d') - datetime.strptime(checkindate, '%Y-%m-%d')
			print("WOO0")
			print(noofnights)
			print(datetime.strptime(checkoutdate, '%Y-%m-%d').month)
			print(datetime.strptime(checkindate, '%Y-%m-%d').month)
			for j in range (noofnights.days):
				j = datetime.strptime(checkindate, '%Y-%m-%d') + timedelta(days=j)
				print(j.month)
				if j.month in peakmonths:
					peakseasondays += 1
				else:
					offseasondays += 1
			print("peakseason: " + str(peakseasondays))
			print("offseason: " + str(offseasondays))
			dbcursor.execute('SELECT * FROM HotelInformation WHERE HotelInformationID = %s;', (hotel_name,))
			rows = dbcursor.fetchall()

			print (rows)
			print (hotel_name)
			fare = (int(rows[0][6])) * int(offseasondays)
			fare += (int(rows[0][5])) * int(peakseasondays)

			total_new_fare = old_price - fare
			pay_us = 0
			if total_new_fare > 0:
				pay_us = 2
			elif total_new_fare < 0:
				pay_us = 1
				total_new_fare = total_new_fare * - 1
		print("rwgswr")
		if refund_activate == 969:
			dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', ("N/A", fare_vale, "Refund", str(tool_table_id_2)))
			refund_activate == 0
			return redirect(url_for('booking_confirm', resultset=bookingdata, cardnumber=cardnumber, usertype = session['usertype'], username = session['username'], acccity = hotel_name))
		print(extra_pay)
		if extra_pay == "969":
			dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', ("N/A", fare_vale, "Extra Payement", str(tool_table_id_2)))
			extra_pay == "0"
			return redirect(url_for('booking_confirm', usertype = session['usertype'], username = session['username']),resultset=bookingdata, cardnumber=cardnumber)

		dbcursor.close()
		conn.close()

		return render_template('update_step.html', username = session['username'], tool_table_id = tool_table_id,\
						 usertype = session['usertype'], payus = pay_us, fare = fare, old_price = old_price, total_new_fare = total_new_fare,\
							checkoutdate = checkoutdate, checkindate = checkindate)




@app.route('/update_step_2/', methods = ['POST', 'GET'])
@login_required
def update_step_2():
	conn = dbconnect.getConnection()
	dbcursor = conn.cursor()
	extra_pay = request.form['extra_pay']
	fare_vale = request.form['fare_value']
	tool_table_id_2 = request.form['tool_table_id_2']
	new_check_in = request.form['newcheckin']
	new_check_out = request.form['newcheckout']
	cardnumber = request.form['cardnumber']
	bookingdata = []
	dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', ("N/A", fare_vale, "Extra Payement", str(tool_table_id_2)))
	dbcursor.execute('UPDATE BookingTable SET CheckInDate = %s, CheckOutDate = %s WHERE BookingId = %s;', (new_check_in, new_check_out, str(tool_table_id_2)))
	conn.commit()
	dbcursor.close()
	conn.close()
	extra_pay == "0"

	#return redirect(url_for('main_Page_Login', usertype= session['usertype'], username = session['username']))
	return redirect(url_for('booking_confirm', cardnumber = cardnumber, bookingdata=bookingdata, usertype = session['usertype'], username = session['username']))


@app.route('/update_step_3/', methods = ['POST', 'GET'])
@login_required
def update_step_3():
	conn = dbconnect.getConnection()
	dbcursor = conn.cursor()
	fare_vale = request.form['fare_value']
	tool_table_id_2 = request.form['tool_table_id_2']
	new_check_in = request.form['newcheckin']
	new_check_out = request.form['newcheckout']
	bookingdata = []
	dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', ("N/A", fare_vale, "SR Refund", str(tool_table_id_2)))
	dbcursor.execute('UPDATE BookingTable SET CheckInDate = %s, CheckOutDate = %s WHERE BookingId = %s;', (new_check_in, new_check_out, str(tool_table_id_2)))
	conn.commit()
	dbcursor.close()
	conn.close()

	return redirect(url_for('main_Page_Login', usertype= session['usertype'], username = session['username']))
	#return redirect(url_for('booking_confirm', cardnumber = cardnumber, bookingdata=bookingdata, usertype = session['usertype'], username = session['username']))


@app.route('/update_step_4/', methods = ['POST', 'GET'])
@login_required
def update_step_4():
	conn = dbconnect.getConnection()
	dbcursor = conn.cursor()
	refund_math = 0
	tool_table_id_2 = request.form['tool_table_id']
	dbcursor.execute('SELECT TotalCharges FROM Billings WHERE BookingId = %s;', (tool_table_id_2,))
	rows = dbcursor.fetchall()
	for x in rows[0]:
		refund_math += float(x)

	dbcursor.execute('SELECT * FROM BookingTable WHERE BookingId = %s;', (tool_table_id_2,))
	rows = dbcursor.fetchall()
	checkin = rows[0][2]
	today = date.today()
	daystocheckin = (checkin - today).days
	if daystocheckin > 60:
		payus = 10
		refund_amount = refund_math
	elif daystocheckin > 30:
		payus = 11
		refund_amount = refund_math / 2
	elif daystocheckin < 30:
		payus = 12
		refund_amount = 0
	#dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
	#			(%s, %s, %s, %s);', ("N/A", fare_vale, "SR Refund", str(tool_table_id_2)))
	#dbcursor.execute('UPDATE BookingTable SET CheckInDate = %s, CheckOutDate = %s WHERE BookingId = %s;', (new_check_in, new_check_out, str(tool_table_id_2)))
	conn.commit()
	dbcursor.close()
	conn.close()

	return render_template('update_step.html', username = session['username'],payus = payus, refund_amount = refund_amount,\
						 dayscheckin = daystocheckin, usertype = session['usertype'], tool_table_id = tool_table_id_2)
	#return redirect(url_for('booking_confirm', cardnumber = cardnumber, bookingdata=bookingdata, usertype = session['usertype'], username = session['username']))


@app.route('/update_step_5/', methods = ['POST', 'GET'])
@login_required
def update_step_5():
	conn = dbconnect.getConnection()
	dbcursor = conn.cursor()
	tool_table_id_2 = request.form['tool_table_id']
	action = request.form['action']
	refund_amount = request.form['refund_amount']
	dbcursor.execute('SELECT RoomTableID FROM BookingTable WHERE BookingId = %s;', (tool_table_id_2,))
	rows = dbcursor.fetchall()
	print(rows[0][0])
	roomtabledeleteid = rows[0][0]
	print(action)
	print(type(action))
	if action == "all":
		dbcursor.execute('DELETE FROM ROOM WHERE RoomTableId = %s;', (roomtabledeleteid,))
		dbcursor.execute('UPDATE BookingTable SET Status = %s WHERE BookingId = %s;', ("Cancelled", str(tool_table_id_2)))
		dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', ("N/A", refund_amount, "FCR Refund", str(tool_table_id_2)))

	elif action == "half":
		dbcursor.execute('DELETE FROM ROOM WHERE RoomTableId = %s;', (roomtabledeleteid,))
		dbcursor.execute('UPDATE BookingTable SET Status = %s WHERE BookingId = %s;', ("Cancelled", str(tool_table_id_2)))
		dbcursor.execute('INSERT INTO Billings (ChargeRate, TotalCharges, PaymentStatus, BookingID) VALUES \
				(%s, %s, %s, %s);', ("N/A", refund_amount, "HCR Refund", str(tool_table_id_2)))
	elif action == "none":
		dbcursor.execute('DELETE FROM ROOM WHERE RoomTableId = %s;', (roomtabledeleteid,))
		dbcursor.execute('UPDATE BookingTable SET Status = %s WHERE BookingId = %s;', ("Cancelled", str(tool_table_id_2)))

	conn.commit()
	dbcursor.close()
	conn.close()
	return redirect(url_for('main_Page_Login', usertype= session['usertype'], username = session['username']))
	#return render_template('update_step.html', username = session['username'],payus = payus, refund_amount = refund_amount,\
	#					 dayscheckin = daystocheckin, usertype = session['usertype'])
	#return redirect(url_for('booking_confirm', cardnumber = cardnumber, bookingdata=bookingdata, usertype = session['usertype'], username = session['username']))

#End of Wrappers-=-=-=-=-=-=-==-=-=-==-=-=-=-=-=-=-=-=-==--==-=-=-=-=-=-==-=-=-=-==-=-=-=-
if __name__ == '__main__':    #you can skip this if running app on terminal window
	for i in range(13000, 18000):
		try:
			app.run(debug = True, port = i)
			break
		except OSError as e:
			print("Port {i} not available".format(i))