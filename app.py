from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'api'
app.json.sort_keys = False

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def index():
    data = {
        'status' : 'OK',
        'code'  : 200,
        'message'   : 'Welcome to a simple Indonesia Territories Api'
    }
    result = data
    return jsonify(result), 200

@app.get('/provinces')
def get_all_provinces():    
    query = "SELECT * FROM provinces"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'All Provinces',
        data = json_data), 200
    
@app.get('/province/<province_id>')
def get_province_detail(province_id):    
    params = [province_id]
    query = "SELECT * FROM provinces WHERE province_id=%s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
        code  = '404',
        message   = 'Data Not Found',), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'Detail Province',
        data = json_data), 200

@app.get('/regencies')
def get_all_regencies():    
    query = "SELECT * FROM regencies"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'All Regencies',
        data = json_data), 200

@app.get('/regency/<regency_id>')
def get_regency_detail(regency_id):    
    params = [regency_id]
    query = "SELECT * FROM regencies WHERE regency_id=%s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
        code  = '404',
        message   = 'Data Not Found',), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'Detail Regency',
        data = json_data), 200
    
@app.get('/regencies/<province_id>')
def get_regencies_by_province(province_id):    
    params = [province_id]
    query = "SELECT \
            reg.province_id as province_id, prov.name as province_name, reg.regency_id AS regency_id, reg.name as regency_name \
            FROM regencies AS reg \
            JOIN provinces AS prov ON reg.province_id = prov.province_id \
            WHERE reg.province_id=%s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
        code  = '404',
        message   = 'Data Not Found',), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'Regencies By Province',
        data = json_data), 200

@app.get('/districts')
def get_all_districts():    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT \
                    dis.district_id as district_id, dis.name AS district_name, \
                    reg.regency_id as regency_id, reg.name AS regency_name,  \
                    prov.province_id AS province_id, prov.name AS province_name \
                    FROM districts AS dis \
                    JOIN regencies AS reg ON dis.regency_id = reg.regency_id \
                    JOIN provinces AS prov ON reg.province_id = prov.province_id ")
    result = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'All Districts',
        data = json_data), 200
    
@app.get('/district/<district_id>')
def get_district_detail(district_id):    
    params = [district_id]
    query = "SELECT \
            * FROM districts \
            WHERE district_id=%s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
        code  = '404',
        message   = 'Data Not Found',), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'Detail District',
        data = json_data), 200    

@app.get('/districts/<regency_id>')
def get_districts_by_regency(regency_id):
    params = [regency_id]
    query = "SELECT \
            reg.regency_id AS regency_id, reg.name AS regency_name, \
            dis.district_id AS district_id, dis.name AS rdistrict_name \
            FROM districts AS dis \
            JOIN regencies AS reg ON dis.regency_id = reg.regency_id\
            WHERE dis.regency_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
        code  = '404',
        message   = 'Data Not Found',), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'Districts By Regency',
        data = json_data), 200
    

@app.get('/villages/<district_id>')
def get_districts_by_district(district_id):
    params = [district_id]
    query = "SELECT \
            reg.province_id as province_id, prov.name as province_name, reg.district_id AS district_id, reg.name as district_name \
            FROM villages AS reg \
            JOIN provinces AS prov ON reg.province_id = prov.province_id \
            WHERE reg.province_id=%s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
        code  = '404',
        message   = 'Data Not Found',), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = 'OK',
        message   = 'Districts By District',
        data = json_data), 200

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)