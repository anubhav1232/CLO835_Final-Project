from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Database connection details from environment variables
DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPWD = os.environ.get("DBPWD")
DATABASE = os.environ.get("DATABASE")
DBPORT = int(os.environ.get("DBPORT"))

# Owner's name from environment variable (simulate ConfigMap)
APP_OWNER = os.environ.get('APP_OWNER', 'Your Name Here')

# S3 Bucket Details
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'clo835-privatebucket')
S3_OBJECT_KEY = os.environ.get('S3_OBJECT_KEY', 'COD.jpg')

# Create an S3 client using boto3
s3_client = boto3.client('s3')

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """Generate a pre-signed URL to share an S3 object.

    :param bucket_name: string
    :param object_key: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                   Params={'Bucket': bucket_name,
                                                           'Key': object_key},
                                                   ExpiresIn=expiration)
    except NoCredentialsError:
        print("Credentials not available")
        return None

    # The response contains the presigned URL
    return response

# Define the supported color codes
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}

# Default color selection
COLOR = os.environ.get('APP_COLOR', 'lime')
if COLOR not in color_codes:
    print(f"Color '{COLOR}' not supported. Falling back to 'lime'.")
    COLOR = 'lime'

@app.route("/", methods=['GET', 'POST'])
def home():
    # Generate pre-signed URL for the background image
    presigned_url = generate_presigned_url(S3_BUCKET_NAME, S3_OBJECT_KEY)
    
    if not presigned_url:
        presigned_url = 'https://via.placeholder.com/500'  # Fallback image if pre-signed URL fails

    return render_template('addemp.html', color=color_codes[COLOR], background_image_url=presigned_url, owner=APP_OWNER)

@app.route("/about", methods=['GET', 'POST'])
def about():
    # Generate pre-signed URL for the background image
    presigned_url = generate_presigned_url(S3_BUCKET_NAME, S3_OBJECT_KEY)
    
    if not presigned_url:
        presigned_url = 'https://via.placeholder.com/500'  # Fallback image if pre-signed URL fails

    return render_template('about.html', color=color_codes[COLOR], background_image_url=presigned_url, owner=APP_OWNER)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    except Exception as e:
        print(f"Error inserting employee: {e}")
        emp_name = "Error"
    finally:
        cursor.close()

    # Generate pre-signed URL for the background image
    presigned_url = generate_presigned_url(S3_BUCKET_NAME, S3_OBJECT_KEY)
    
    if not presigned_url:
        presigned_url = 'https://via.placeholder.com/500'  # Fallback image if pre-signed URL fails

    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR], background_image_url=presigned_url, owner=APP_OWNER)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    # Generate pre-signed URL for the background image
    presigned_url = generate_presigned_url(S3_BUCKET_NAME, S3_OBJECT_KEY)
    
    if not presigned_url:
        presigned_url = 'https://via.placeholder.com/500'  # Fallback image if pre-signed URL fails

    return render_template("getemp.html", color=color_codes[COLOR], background_image_url=presigned_url, owner=APP_OWNER)

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    emp_id = request.form['emp_id']
    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output = {
                "emp_id": result[0],
                "first_name": result[1],
                "last_name": result[2],
                "primary_skills": result[3],
                "location": result[4],
            }
        else:
            output = {"emp_id": "Not Found", "first_name": "", "last_name": "", "primary_skills": "", "location": ""}
    except Exception as e:
        print(f"Error fetching employee: {e}")
    finally:
        cursor.close()

    # Generate pre-signed URL for the background image
    presigned_url = generate_presigned_url(S3_BUCKET_NAME, S3_OBJECT_KEY)
    
    if not presigned_url:
        presigned_url = 'https://via.placeholder.com/500'  # Fallback image if pre-signed URL fails

    return render_template(
        "getempoutput.html",
        id=output["emp_id"],
        fname=output["first_name"],
        lname=output["last_name"],
        interest=output["primary_skills"],
        location=output["location"],
        color=color_codes[COLOR],
        background_image_url=presigned_url,
        owner=APP_OWNER
    )

if __name__ == '__main__':
    # Command-line argument for color (optional)
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        if args.color in color_codes:
            COLOR = args.color
        else:
            print(f"Command-line color '{args.color}' not supported. Falling back to 'lime'.")
            COLOR = 'lime'

    print(f"Application will run with background color: {COLOR}")
    app.run(host='0.0.0.0', port=81, debug=True)
