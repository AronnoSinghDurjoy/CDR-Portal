from flask import Flask, render_template, request, jsonify, session, redirect, url_for, make_response
import oracledb
import paramiko
import time
import random
import csv
import io
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configuration


# Oracle DB Configs
db_configs = {

}

# Allowed numbers
ALLOWED_NUMBERS = {

}

# SMS Gateway Info


# OTP Store
otp_store = {}

def normalize_phone(phone):
    digits = ''.join(filter(str.isdigit, phone))
    if digits.startswith('01'):
        digits = '88' + digits
    elif digits.startswith('880'):
        pass
    return digits

def log_login(phone):
    with open('login_logs.txt', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {phone} logged in\n")

def send_sms_via_ssh(to, text):
    cmd = (

    )
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SSH_SMS_HOST, port=SSH_SMS_PORT, username=SSH_SMS_USER, password=SSH_SMS_PASS, timeout=10)
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
        out = stdout.read().decode()
        err = stderr.read().decode()
        code = stdout.channel.recv_exit_status()
        ssh.close()
        print("SMS STDOUT:", out)
        print("SMS STDERR:", err)
        return code == 0
    except Exception as e:
        print("SSH SMS Error:", e)
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session or not session['authenticated']:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def fetch_14_column_cdr_data(msisdn, start, end, radio_filter):
    try:
        user =
        password =
        dsn =

        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        def return_strings_as_bytes(cursor, metadata):
            if metadata.type_code is oracledb.DB_TYPE_VARCHAR:
                return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)

        cursor.outputtypehandler = return_strings_as_bytes

        string = ''
        if radio_filter == 'all':
            string = ''
        elif radio_filter == 'moc&mtc':
            string = " AND (M.M01_CALLTYPE = 'MOC' OR M.M01_CALLTYPE = 'MTC')"
        elif radio_filter == 'moc':
            string = " AND M.M01_CALLTYPE = 'MOC'"
        elif radio_filter == 'mtc':
            string = " AND M.M01_CALLTYPE = 'MTC'"
        elif radio_filter == 'smsmo&smsmt':
            string = " AND (M.M01_CALLTYPE = 'SMSMO' OR M.M01_CALLTYPE = 'SMSMT')"
        elif radio_filter == 'smsmo':
            string = " AND M.M01_CALLTYPE = 'SMSMO'"
        elif radio_filter == 'smsmt':
            string = " AND M.M01_CALLTYPE = 'SMSMT'"

        query = f'''
        
        '''

        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

def fetch_msisdn_to_imei(msisdn_input, start, end, is_file=False):
    try:


        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        query = f'''
            
        '''

        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]
        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

def fetch_imei_to_msisdn(imei, start, end):
    try:


        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        def return_strings_as_bytes(cursor, metadata):
            if metadata.type_code is oracledb.DB_TYPE_VARCHAR:
                return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)

        cursor.outputtypehandler = return_strings_as_bytes

        query = f'''
           
        '''

        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

def fetch_lac_cell_cdr(lac, cell, date):
    try:


        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        def return_strings_as_bytes(cursor, metadata):
            if metadata.type_code is oracledb.DB_TYPE_VARCHAR:
                return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)

        cursor.outputtypehandler = return_strings_as_bytes

        dt = datetime.strptime(date, '%Y-%m-%d')
        pre_date = dt - timedelta(days=3)
        post_date = dt + timedelta(days=3)
        start_date = pre_date.strftime('%Y-%m-%d')
        end_date = post_date.strftime('%Y-%m-%d')

        query = f'''
        
        '''

        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

def fetch_foreign_number_cdr_data(msisdn, start, end):
    try:


        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        def return_strings_as_bytes(cursor, metadata):
            if metadata.type_code is oracledb.DB_TYPE_VARCHAR:
                return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)

        cursor.outputtypehandler = return_strings_as_bytes

        query = f'''
        
        '''

        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

def fetch_cgi_msisdn_cdr_data(cgi, start, end, radio_filter):
    try:


        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        def return_strings_as_bytes(cursor, metadata):
            if metadata.type_code is oracledb.DB_TYPE_VARCHAR:
                return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)

        cursor.outputtypehandler = return_strings_as_bytes

        string = ''
        if radio_filter == 'all':
            string = ''
        elif radio_filter == 'moc&mtc':
            string = " AND (M.M01_CALLTYPE = 'MOC' OR M.M01_CALLTYPE = 'MTC')"
        elif radio_filter == 'moc':
            string = " AND M.M01_CALLTYPE = 'MOC'"
        elif radio_filter == 'mtc':
            string = " AND M.M01_CALLTYPE = 'MTC'"
        elif radio_filter == 'smsmo&smsmt':
            string = " AND (M.M01_CALLTYPE = 'SMSMO' OR M.M01_CALLTYPE = 'SMSMT')"
        elif radio_filter == 'smsmo':
            string = " AND M.M01_CALLTYPE = 'SMSMO'"
        elif radio_filter == 'smsmt':
            string = " AND M.M01_CALLTYPE = 'SMSMT'"

        query = f'''
        
        '''

        cursor.execute(query)

        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

def fetch_retailer_location_card_data(msisdn, start, end):
    try:


        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        cursor = connection.cursor()

        def return_strings_as_bytes(cursor, metadata):
            if metadata.type_code is oracledb.DB_TYPE_VARCHAR:
                return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)

        cursor.outputtypehandler = return_strings_as_bytes

        query = f'''
        
        '''

        cursor.execute(query)
        column_names = [col[0] for col in cursor.description]
        results = [
            [r.decode('latin-1') if isinstance(r, bytes) else r for r in row]
            for row in cursor.fetchall()
        ]

        cursor.close()
        connection.close()

        return column_names, results
    except oracledb.DatabaseError as e:
        return str(e), []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    phone = normalize_phone(data.get('phone', ''))

    if phone not in ALLOWED_NUMBERS:
        return jsonify({'success': False, 'message': 'Phone number not authorized. Please contact with BI team.'})

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    otp_store[phone] = {
        'otp': otp,
        'timestamp': time.time()
    }

    # Send SMS
    sms_text = f"Your Teletalk CDR Portal OTP is: {otp}. Valid for 5 minutes."
    sms_sent = send_sms_via_ssh(phone, sms_text)

    if sms_sent:
        return jsonify({'success': True, 'message': 'OTP sent successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send OTP'})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    phone = normalize_phone(data.get('phone', ''))
    otp = data.get('otp', '')

    if phone not in otp_store:
        return jsonify({'success': False, 'message': 'No OTP found for this number'})

    stored_otp = otp_store[phone]

    # Check if OTP is expired (5 minutes)
    if time.time() - stored_otp['timestamp'] > 300:
        del otp_store[phone]
        return jsonify({'success': False, 'message': 'OTP expired'})

    if stored_otp['otp'] == otp:
        # OTP verified
        session['authenticated'] = True
        session['phone'] = phone
        del otp_store[phone]
        log_login(phone)
        return jsonify({'success': True, 'message': 'OTP verified successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid OTP'})

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', phone=session['phone'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/service/<service_name>')
@login_required
def service(service_name):
    return render_template('service.html', service_name=service_name)

@app.route('/api/14_column_cdr', methods=['POST'])
@login_required
def api_14_column_cdr():
    data = request.get_json()
    msisdn = data.get('msisdn')
    start = data.get('start_date')
    end = data.get('end_date')
    radio_filter = data.get('radio_filter', 'all')

    column_names, results = fetch_14_column_cdr_data(msisdn, start, end, radio_filter)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/api/msisdn_to_imei', methods=['POST'])
@login_required
def api_msisdn_to_imei():
    data = request.get_json()
    msisdn = data.get('msisdn')
    start = data.get('start_date')
    end = data.get('end_date')

    column_names, results = fetch_msisdn_to_imei(msisdn, start, end)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/api/imei_to_msisdn', methods=['POST'])
@login_required
def api_imei_to_msisdn():
    data = request.get_json()
    imei = data.get('imei')
    start = data.get('start_date')
    end = data.get('end_date')

    column_names, results = fetch_imei_to_msisdn(imei, start, end)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/api/lac_cell_cdr', methods=['POST'])
@login_required
def api_lac_cell_cdr():
    data = request.get_json()
    lac = data.get('lac')
    cell = data.get('cell')
    date = data.get('date')

    column_names, results = fetch_lac_cell_cdr(lac, cell, date)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/api/foreign_number_cdr', methods=['POST'])
@login_required
def api_foreign_number_cdr():
    data = request.get_json()
    msisdn = data.get('msisdn')
    start = data.get('start_date')
    end = data.get('end_date')

    column_names, results = fetch_foreign_number_cdr_data(msisdn, start, end)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/api/cgi_msisdn_cdr', methods=['POST'])
@login_required
def api_cgi_msisdn_cdr():
    data = request.get_json()
    cgi = data.get('cgi')
    start = data.get('start_date')
    end = data.get('end_date')
    radio_filter = data.get('radio_filter', 'all')

    column_names, results = fetch_cgi_msisdn_cdr_data(cgi, start, end, radio_filter)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/api/retailer_location', methods=['POST'])
@login_required
def api_retailer_location():
    data = request.get_json()
    msisdn = data.get('msisdn')
    start = data.get('start_date')
    end = data.get('end_date')

    column_names, results = fetch_retailer_location_card_data(msisdn, start, end)

    return jsonify({
        'success': True,
        'columns': column_names,
        'data': results
    })

@app.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    data = request.get_json()
    csv_data = data.get('csv_data', [])
    columns = data.get('columns', [])
    filename = data.get('filename', 'cdr_data.csv')
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(columns)
    
    # Write data
    for row in csv_data:
        writer.writerow(row)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-type'] = 'text/csv'
    
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)