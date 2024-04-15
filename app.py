from flask import Flask, request, jsonify, url_for, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'api'
app.json.sort_keys = False

mysql = MySQL(app)


@app.route('/', methods=['GET','POST'])
def index():
    url = 'http://127.0.0.1:5000'

    return render_template('welcome_page.html',
                           url=url)

@app.get('/query')
def query():
    params = []
    query = "SELECT \
            prov.province_id AS province_id, prov.name AS province_name, prov.capital_city AS capital_city, \
            reg.regency_id AS regency_id, reg.name AS regency_name, \
            dis.district_id AS district_id, dis.name AS district_name, \
            vil.village_id AS village_id, vil.name AS village_name \
            FROM provinces AS prov\
            JOIN regencies AS reg ON prov.province_id = reg.province_id \
            JOIN districts AS dis ON reg.regency_id = dis.regency_id \
            JOIN villages AS vil ON dis.district_id = vil.district_id "
    province = request.args.get('province')

    # Check if request name exists
    if province:
        query +="WHERE prov.name LIKE %s "
        params.append("%{}%".format(province))
    
    
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
                code  = '404',
                message   = "Data Not Found",), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))

    return jsonify(
        code  = '200',
        status    = True,
        message   = 'Query Result',
        data = json_data), 200

@app.get('/provinces')
def get_all_provinces():
    params = []
    query = "SELECT * FROM provinces "
    name = request.args.get('name')
    
    # Check if request name exists
    if name:
        query +="WHERE name LIKE %s "
        params.append("%{}%".format(name))
        
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
                code  = '404',
                message   = "Data Not Found",), 404
        
    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))

    return jsonify(
        code  = '200',
        status    = True,
        message   = 'All Provinces' if not name else 'Provinces with Param {}'.format(name),
        data = json_data), 200
    
@app.get('/provinces/<province_id>')
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
        status    = True,
        message   = 'Detail Province {}'.format(json_data[0]['name']),
        data = json_data), 200

@app.get('/regencies')
def get_all_regencies():    
    params = []
    query = "SELECT * FROM regencies"
    name = request.args.get('name')

    if name:
        query += " WHERE name LIKE %s"
        params.append('%{}%'.format(name))

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
        status    = True,
        message   = 'All Regencies' if not name else 'Regencies with Param {}'.format(name),
        data = json_data), 200

@app.get('/regencies/<regency_id>')
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
        status    = True,
        message   = 'Detail Regency {}'.format(json_data[0]['name']),
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
        status    = True,
        message   = 'Regencies By Province',
        data = json_data), 200

@app.get('/districts')
def get_all_districts():
    params = []
    query = "SELECT \
            dis.district_id as district_id, dis.name AS district_name, \
            reg.regency_id as regency_id, reg.name AS regency_name,  \
            prov.province_id AS province_id, prov.name AS province_name \
            FROM districts AS dis \
            JOIN regencies AS reg ON dis.regency_id = reg.regency_id \
            JOIN provinces AS prov ON reg.province_id = prov.province_id "
    name = request.args.get('name')

    if name:
        query += "WHERE dis.name LIKE %s"
        params.append("%{}%".format(name))

    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    if not result:
        return jsonify(
            code = '404',
            message = 'Data Not Found',), 404

    row_headers=[x[0] for x in cursor.description]
    json_data = []
    for res in result:
            json_data.append(dict(zip(row_headers,res)))
            
    return jsonify(
        code  = '200',
        status    = True,
        message   = 'All Districts',
        data = json_data), 200
    
@app.get('/districts/<district_id>')
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
        status    = True,
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
        status    = True,
        message   = 'Districts By Regency',
        data = json_data), 200
    

@app.get('/villages')
def get_all_villages():
    params = []
    name = request.args.get('name')
    query = ("SELECT \
             vil.village_id AS village_id, vil.name AS village_name, \
             dis.name AS district_name, reg.name AS regency_name, prov.name AS province_name \
             FROM villages AS vil \
             JOIN districts AS dis ON vil.district_id = dis.district_id \
             JOIN regencies AS reg ON dis.regency_id = reg.regency_id \
             JOIN provinces AS prov ON reg.province_id = prov.province_id ")

    if name:
        query +=" WHERE vil.name LIKE %s "
        params.append("%{}%".format(name))

    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    if not result:
        return jsonify(
            code    = '404',
            message = 'Data Not Found',), 404

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    for res in result:
        json_data.append(dict(zip(row_headers, res)))

    return jsonify(
        code    = '200',
        status  = True,
        message = 'All Villages' if not name else 'Villages With Params {}'.format(name),
        data = json_data),200
@app.get('/villages/<district_id>')
def get_villages_by_district(district_id):
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
        status    = True,
        message   = 'Districts By District',
        data = json_data), 200
    
    
@app.get('/villages/<village_id>')    
def get_village_detail(village_id):
    params = [village_id]
    query = "SELECT \
            * \
            FROM villages \
            WHERE village_id = %s"
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    if not result:
        return jsonify(
            code    = '404',
            message = 'Data Not Found'),404
        
    return jsonify(
        code = 200,
        message = "Detail Village",
        data = result 
        ),200

if __name__=='__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)