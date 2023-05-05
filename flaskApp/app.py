import boto3
from boto3.dynamodb.conditions import Key
import os
from flask import Flask, render_template, request, session
from flask import redirect, url_for
from boto3.dynamodb.conditions import Attr

os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAVU2WUM5AFMHPR6BK'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'WMTPdl3BKCL0TVuPCixGicS5qlPDIKoS+FRt/GZi'
os.environ['AWS_SESSION_TOKEN'] = 'FwoGZXIvYXdzEJ///////////wEaDBPcLR4NHyR3tCKlOyLNAfRbLWgY1RLGC63cqFnEDqrkxMOdE0Cuo6CUJHHh5FMf65U0ovDSu0H3/qTQXoxFiohVlLAAGIdwcwTtEh4lw5nbDtWutothcdFEraDIZdP+hZjdo9Ur4NdS6yi6Ao06it1e31wibpnhykB9HLA9jP9n6W65ixhlWdMNkGBlZlfDN8pKQsszOXKkR9I4j0d7wx575zJvUQe7OLlAT6iEkczhcPzrXVpEy7zPo4WoVIB5YxZ30GQVqPLVhJLT0fgj4wMMZfwPI8BvG1Li65go+InLoQYyLXMhAvgQ0LNE44cIvXB5/Mci1AdvHheVT9iOZw17cZ/XYltoNW7E0KqY3otKFw=='  # Optional if you are using temporary credentials

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb.Table('login')
table_music = dynamodb.Table('music')
table_sub = dynamodb.Table('subscriptions')

def s3_url(bucket_name, object_name):
    s3_client = boto3.client('s3')
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name
        }
    )
    return url

app = Flask(__name__)
app.secret_key = 'mysecretkey'

@app.route('/')
def home():
    return render_template('login.html')

def get_user(email):
    response = table.get_item(
        Key={
            'email': email
        }
    )
    return response.get('Item')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method ==  'POST':

        email = request.form['email']
        password = request.form['password']

        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
            )
    
        if response['Count'] == 0:
                # No user with this email exists
                return render_template('login.html', error='Email is invalid')

        user = response['Items'][0]
    
        if password == user['password']:
            user_id = user['user_name']
            session['user_id'] = user_id
            return redirect('/main')
        else:
            # Password is incorrect
            return render_template('login.html', error='Password is invalid')
        
    else:
        return render_template('login.html')

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Add email and password to DynamoDB table
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        if response.get('Items'):
            # email already exists in the login table
            return render_template('register.html', error='The email already exists')
        else:
            table.put_item(Item={'email': email, 'user_name': username, 'password': password})
            return render_template('login.html')
            # return 'Registration successful!'
    else:
        return render_template('register.html')
    
@app.route('/main',  methods=['GET'])
def mainpage():
    # DISPLAY USERNAMR ON MAINPAGE
    user_id = session.get('user_id')
    return render_template('main.html', username =user_id)


@app.route('/query')
def query():
    return render_template('query.html')

@app.route('/query-results', methods=['POST'])
def query_results():
    try:
        artist = request.form['artist']
        year = request.form['year']
        title = request.form['title']

        if artist and title and year:
            response = table_music.query(
            FilterExpression= Attr('year').eq(year),
            KeyConditionExpression=Key('title').eq(title) & Key('artist').eq(artist)
            )
            if response['Count'] == 0:
                return render_template('query_results.html', error="No results found, please query again")
            
        elif title and artist:
        # Search by title and artist
            response = table_music.query(
                KeyConditionExpression=Key('title').eq(title) & Key('artist').eq(artist)
            )
            if response['Count'] == 0:
                return render_template('query_results.html', error="no results is retrieved, please query again")
        elif year and artist:
            response = table_music.scan(
            FilterExpression=Attr('year').eq(year) & Attr('artist').eq(artist) & Attr('title').exists()
            )
            if response['Count'] == 0:
                return render_template('query_results.html', error="no results is retrieved, please query again")
        elif year and title:
            response = table_music.query(
                FilterExpression= Attr('year').eq(year),
                KeyConditionExpression=Key('title').eq(title) 
                )
            if response['Count'] == 0:
                return render_template('query_results.html', error="no results is retrieved, please query again")
        elif title:
        # Search by title only
            response = table_music.query(
                KeyConditionExpression=Key('title').eq(title)
            )
            if response['Count'] == 0:
                return render_template('query_results.html', error="no results is retrieved, please query again")
        elif artist:
        # Search by artist only
            response = table_music.scan(
            FilterExpression=Attr('artist').contains(artist)
            )
            if response['Count'] == 0:
                    return render_template('query_results.html', error="no results is retrieved, please query again")
        elif year:
            response = table_music.scan(
            FilterExpression=Attr('year').eq(year) & Attr('title').exists()
            )
            if response['Count'] == 0:
                return render_template('query_results.html', error="no results is retrieved, please query again")
        else:
        # No search parameters specified
            # response = table_music.scan()
            return render_template('query_results.html', error = "no results is retrieved, please query again")

    # Render the query results template
        return render_template('query_results.html', results=response['Items'])
    except Exception as e:
        print(str(e))

    
@app.route('/subscribed', methods=['GET', 'POST'])
def subscribed():
    try:
        if request.method == 'POST':
        # Retrieve the form data
            song_title = request.form.get('title')
            song_artist = request.form.get('artist')
            song_img_url = request.form.get('img_url')
            song_year = request.form.get('year')
            user_id = session.get('user_id')

        # Create a new item in the 'subscriptions' table
            table_sub.put_item(Item={
                'sub_user_name': user_id,
                'song_title': song_title,
                'song_artist': song_artist,
                'song_year': song_year,
                'song_img_url': song_img_url
            })

            response = table_sub.scan(
                FilterExpression=Attr('song_title').eq(song_title) & Attr('sub_user_name').exists()
            )

            subbed_song = response['Items'][0]

            if subbed_song['song_title'] == song_title:
            # Redirect to a success page
                return render_template('subscribed.html')
            # return redirect('/main') 
        
        
    
    # If the request method is GET, render the subscribe form
        else:
            return render_template('subscribe.html')
    except Exception as e:
        print(str(e))


@app.route('/subscribed_info', methods=['GET', 'POST'])
def subscribed_info():
    try:
        user_id = session.get('user_id')
        response = table_sub.scan(
            FilterExpression=Attr('sub_user_name').eq(user_id)
        )
        
        # ensure to let system know if theres no elements
        if response['Count'] == 0:
                return render_template('subscribed_info.html', error='NO SUBSCRIPTIONS YET!')
            
        user = response['Items'][0]  # assuming there's only one item matching the query

        if user:
    # Render the HTML page with the retrieved row

            if user['sub_user_name'] == user_id:
            # return "madd"
                return render_template('subscribed_info.html', results=response['Items'], username = user_id)

        
        return render_template('subscribed_info.html', error = "empty list")

    except Exception as e:
        print(str(e))

@app.route('/remove_subscription', methods=['POST'])
def remove_subscription():
    try:

        if request.method == 'POST':
        #retrieve from the subscription_info page to remove
            song_title = request.form.get('title')
            user_id = session['user_id']


            table_sub.delete_item(
                Key={
                    'sub_user_name': user_id,
                    'song_title': song_title
                }
                )
            response = table_sub.scan(
                    FilterExpression=Attr('song_title').eq(song_title) & Attr('sub_user_name').exists()
                )
            
            if response['Count'] == 0:
                return render_template('subscribed.html', error='Subscription not found')
            
            # if not response['Items']:
            #     return render_template('subscribe.html', error='out of elements')
            subbed_song = response['Items'][0]

            if subbed_song['song_title'] == song_title:
            # Redirect to a success page
                    return render_template('subscribed.html')
        
            return render_template('subscribed.html')
    # If the request method is GET, render the subscribe form
        
        return render_template('subscribed.html')
        
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=80)