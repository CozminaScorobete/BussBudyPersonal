# save this as app.py
from flask import Flask, request, url_for, render_template, flash, session, render_template_string, Response
from markupsafe import escape
import mysql.connector
from verifyEmail import sendEmail
import logging
import random
import time
import folium
import os

import math
from flask import Flask, render_template, jsonify, request
import random
from math import sqrt, sin, cos, atan2


from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key="cheie_secreta_nu_imi_place_web-ul"

############################################################
###VARIABLE

timetable1=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69]
timetable2=[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76]
timetable3=[14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83]
timetable4=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87]
timetable5=[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76]
bus_stops = [
    {"name": "Bus Stop 1", "lat": 37.7749, "lon": -122.4194, "popup": "Welcome to Bus Stop 1!"},
    {"name": "Bus Stop 2", "lat": 37.7833, "lon": -122.4167, "popup": "This is Bus Stop 2!"},
    {"name": "Bus Stop 3", "lat": 37.7917, "lon": -122.4083, "popup": "Greetings from Bus Stop 3!"},
    {"name": "Continental", "lat": 45.755768, "lon": 21.231871, "popup": "Hotel Continental🗿"},
    {"name": "Piața Libertății", "lat": 45.755988, "lon": 21.226887, "popup": "Piața Libertății"},
    {"name": "Piața 700", "lat": 45.756243, "lon": 21.222984, "popup": "Piața Timișoara 700"},
    {"name": "Spitalul de Copii", "lat": 45.755380, "lon": 21.221161, "popup": "Spitalul de Copii"},
    {"name": "Catedrala", "lat": 45.751396, "lon": 21.223763, "popup": "Catedrala mitropolitană"},
    {"name": "Piața Sfânta Maria", "lat": 45.748828, "lon": 21.219151, "popup": "Piața Maria"},
    {"name": "Parcul Doina", "lat": 45.744454, "lon": 21.222314, "popup": "Parcul Doina (C. Sylva)"},
    {"name": "Piața Bălcescu", "lat": 45.741780, "lon": 21.225083, "popup": "Piața Nicolae Bălcescu"},
    {"name": "Piața Crucii", "lat": 45.741846, "lon": 21.232408, "popup": "Piața Crucii"},
    {"name": "Cluj", "lat": 45.743685, "lon": 21.236982, "popup": "Strada Clujului"},
    {"name": "Sala Olimpia", "lat": 45.745209, "lon": 21.241371, "popup": "Aleea F.C. Ripensia"},
    {"name": "Deliblata", "lat": 45.747001, "lon": 21.246541, "popup": "Strada Deliblata"},
    {"name": "Banatim", "lat": 45.748888, "lon": 21.252997, "popup": "Banatim"},
    {"name": "Fabrica de bere", "lat": 45.753006, "lon": 21.250202, "popup": "Fabrica de bere Timișoreana"},
    {"name": "Piața Traian", "lat": 45.757517, "lon": 21.249233, "popup": "Piața Traian"},
    {"name": "3 August", "lat": 45.756763, "lon": 21.244976, "popup": "3 August"},
    {"name": "Prefectura", "lat": 45.755687, "lon": 21.238521, "popup": "Prefectura Județului Timiș"},
    {"name": "CONTINENTAL", "lat": 45.732699, "lon": 21.258512, "popup": "CONTINENTAL AG"},
    {"name": "P-ţa Domăşnean", "lat": 45.733605, "lon": 21.260136, "popup": "P-ţa Domăşnean"},
    {"name": "Giratie Sudului", "lat": 45.731340, "lon": 21.246986, "popup": "Giratie Sudului"},
    {"name": "Parc Sudului", "lat": 45.734127, "lon": 21.248695, "popup": "Parc Sudului"},
    {"name": "Blv. Sudului", "lat": 45.737120, "lon": 21.250538, "popup": "Blv Sudului"},
    {"name": "Spit. Județean", "lat": 45.738637, "lon": 21.238210, "popup": "Spit. Județean"},
    {"name": "Casa Tineretului", "lat": 45.741484, "lon": 21.238767, "popup": "Casa tineretului are un profi foarte cool"},
    {"name": "Sala Olimpia", "lat": 45.746092, "lon": 21.240558, "popup": "Sala Olimpia"},
    {"name": "Complex Studențesc", "lat": 45.748990, "lon": 21.236044, "popup": "Aici au șhaorma bună uneori"},
    {"name": "Parcul Copiilor", "lat": 45.751833, "lon": 21.233474, "popup": "Greetings from Bus Stop 3!"},
    {"name": "Hector", "lat": 45.756908, "lon": 21.233848, "popup": "Sincer nu știu cine e Hector 🤷"},
    {"name": "Piața Mărăști", "lat": 45.759448, "lon": 21.228620, "popup": "Oituz"},
    {"name": "Pţa. Cons. Europei", "lat": 45.764518, "lon": 21.225200, "popup": "Iulius Mall"},
    {"name": "Div 9 Cavalerie", "lat": 45.769426, "lon":  21.230383, "popup": "Div 9 Cavalerie"},
    {"name": "Euro-Dedeman", "lat": 45.768067, "lon": 21.236721, "popup": "DE-DE-MAN!👷"},
    {"name": "Gara de Est", "lat": 45.767846, "lon": 21.244951, "popup": "Aici vin trenuri uneori"},
    {"name": "Stuparilor", "lat": 45.772976, "lon": 21.245742, "popup": "Stuparilor"},
    {"name": "Petru și Pavel", "lat": 45.776811, "lon": 21.233472, "popup": "Petru și Pavel"},
    {"name": "Pomiculturii", "lat": 45.773157, "lon": 21.231734, "popup": "Aici sunt pomi uneori"}
]
linia6=[(stop["lat"], stop["lon"]) for stop in bus_stops[3:20]]
linia6.append((bus_stops[3]["lat"], bus_stops[3]["lon"]))
liniaE2=[(stop["lat"], stop["lon"]) for stop in bus_stops[20:39]]
liniaE2.extend((stop["lat"], stop["lon"]) for stop in bus_stops[33:23:-1])
liniaE2.append((bus_stops[20]["lat"], bus_stops[20]["lon"]))
bus_routes = [
    {
        "route": [
            [37.7749, -122.4194],
            [37.7782, -122.4208],  # A curved point
            [37.7817, -122.4199],  # Another curved point
            [37.7833, -122.4167]
        ],
        "popup": "Curved Route from Bus Stop 1 to Bus Stop 2"
    },
    {
        "route": [
            [37.7833, -122.4167],
            [37.7871, -122.4144],  # A curved point
            [37.7917, -122.4083]
        ],
        "popup": "Curved Route from Bus Stop 2 to Bus Stop 3"
    },
    {
        "route": linia6,
        "popup": "Traseu Tramvai 6"
    },
    {
        "route": liniaE2,
        "popup": "Traseu Linia Express 2"
    }
]

dynamic_pins = [
    {"id": 1, "lat": 45.755768, "lon": 21.231871, "title": "Tramvai 6a [1]", "popup": "Status: Estimare", "timetable": timetable1, "route": linia6, "time_difference": 0, "expiration_time": None},
    {"id": 2, "lat": 45.756243, "lon": 21.222984, "title": "Tramvai 6a [2]", "popup": "Status: Estimare", "timetable": timetable2, "route": linia6, "time_difference": 0, "expiration_time": None},
    {"id": 3, "lat": 45.755988, "lon": 21.226887, "title": "Tramvai 6b [1]", "popup": "Status: Estimare", "timetable": timetable3, "route": linia6[::-1], "time_difference": 0, "expiration_time": None},
    {"id": 4, "lat": 45.755988, "lon": 21.226887, "title": "Tramvai 6b [2]", "popup": "Status: Estimare", "timetable": timetable4, "route": linia6[::-1], "time_difference": 0, "expiration_time": None},
    {"id": 5, "lat": 45.755988, "lon": 21.226887, "title": "Autobuz E2", "popup": "Status: Estimare", "timetable": timetable5, "route": liniaE2, "time_difference": 0, "expiration_time": None}
]

##################################################################################################
#####DATABASE CONNECTION
connection=mysql.connector.connect(host="localhost", user="root", password="", database="busbuddy")

if connection.is_connected():
    print("Connected Successfully")
else:
    print("Fail to connect")

connection.close()

connection=mysql.connector.connect(host="localhost", user="root", password="", database="busbuddy")
cursor= connection.cursor()

#####################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_buttons_data', methods=['GET'])
def get_buttons_data():
    # Replace this with your actual data retrieval logic
    button_data = []

    for pis in dynamic_pins:
         if pis["popup"]=="Status: Întârziat":
              button_data.append({"title": pis["title"], "description": pis["popup"]})
         
    return jsonify(button_data)

@app.route('/map', methods=['POST', 'GET']) 
def map():
    return render_template('map.html', bus_stops=bus_stops, bus_routes=bus_routes, dynamic_pins=dynamic_pins)

def calculate_dynamic_pins_positions():
    new_dynamic_pins = []  # Create a new list to hold the updated positions

    current_time = datetime.now()
    current_minute = (current_time.minute + current_time.second / 60) % 60  # Calculate time elapsed in minutes

    for pin in dynamic_pins:
        timetable = pin["timetable"]
        route = pin["route"]
        time_difference = pin.get("time_difference", 0)  # Get the stored time difference

        # Check if the "Live" status has expired
        expiration_time = pin.get("expiration_time")
        if expiration_time and current_time > expiration_time:
            # Reset the status to "Estimare" or any desired status
            pin["popup"] = "Status: Estimare"

        # Calculate the current and next stops based on the adjusted timetable
        current_stop_index = next_stop_index = 0
        for i, minute in enumerate(timetable):
            adjusted_minute = (minute + time_difference) % 60

            if adjusted_minute <= current_minute:
                current_stop_index = i
            else:
                next_stop_index = i
                break

        if (timetable[0]+ time_difference) % 60>=current_minute:
            for i, minute in enumerate(timetable):
                adjusted_minute = (minute + time_difference) % 60 - 60

                if adjusted_minute <= current_minute:
                    current_stop_index = i
                else:
                    next_stop_index = i
                    break

        # Calculate alpha based on the adjusted time difference
        if current_stop_index == next_stop_index:
            # If the bus is currently at a stop, alpha should be 0
            alpha = 0
        else:
            be = (timetable[next_stop_index % len(timetable)] - timetable[current_stop_index % len(timetable)]) % 60
            alpha = ((current_minute - timetable[current_stop_index]) + be) % be / be

        # Ensure alpha is between 0 and 1
        alpha = alpha % 1  # Adjust alpha to be within [0, 1)

        print(current_stop_index,alpha,next_stop_index,time_difference)
        # Interpolate between the current and next stops based on the alpha factor
        lat_a, lon_a = route[current_stop_index % (len(route)-1)]
        lat_b, lon_b = route[next_stop_index % (len(route)-1)]
        lat = lat_a + alpha * (lat_b - lat_a)
        lon = lon_a + alpha * (lon_b - lon_a)

        # Create a new pin with updated position
        new_pin = {
            "id": pin["id"],
            "lat": lat,
            "lon": lon,
            "title": pin["title"],
            "popup": pin["popup"],
            "timetable": pin["timetable"],
            "route": pin["route"],
            "time_difference": time_difference  # Use the stored time difference
        }

        new_dynamic_pins.append(new_pin)

    return new_dynamic_pins


@app.route('/button1_action', methods=['POST'])
def button1_action():
    global dynamic_pins
    pin_id = request.json['pin_id']
    # funny button logic
    if dynamic_pins[pin_id - 1]["popup"] != "Status: Live":
        dynamic_pins[pin_id - 1]["popup"] = "Status: Întârziat"
        return jsonify({"result": "Întârziare raportată cu succes"})
    else:
        return jsonify({"result": "Bă neobrăzatule"})

def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the distance between two points using the Haversine formula
    R = 6371  # Earth radius in kilometers

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (sin(dlat / 2) ** 2) + cos(lat1) * cos(lat2) * (sin(dlon / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
@app.route('/button2_action', methods=['POST'])
def button2_action():
    global dynamic_pins
    data = request.json
    pin_id = data.get('pin_id')
    user_lat = data.get('user_lat')
    user_lon = data.get('user_lon')

    print(f"Button 2 clicked for Dynamic Pin {pin_id}, User Location: {user_lat}, {user_lon}")

    closest_point = None
    min_distance = float('inf')
    closest_alpha = None
    closest_interval = None

    # Get the pin's route
    pin_route = dynamic_pins[pin_id - 1]["route"]

    # Iterate through each interval on the route
    for i in range(len(pin_route) - 1):
        lat1, lon1 = pin_route[i]
        lat2, lon2 = pin_route[i + 1]

        # Calculate the distance to the closest point on the edge
        edge_distance = calculate_distance(user_lat, user_lon, lat1, lon1)

        # Calculate the projection of the user's location onto the edge
        edge_length_squared = (lat2 - lat1)**2 + (lon2 - lon1)**2
        t = max(0, min(1, ((user_lat - lat1) * (lat2 - lat1) + (user_lon - lon1) * (lon2 - lon1)) / edge_length_squared))

        # Calculate the coordinates of the closest point on the edge
        closest_lat = lat1 + t * (lat2 - lat1)
        closest_lon = lon1 + t * (lon2 - lon1)

        # Calculate the distance between the user and the closest point on the edge
        distance_to_closest_point = calculate_distance(user_lat, user_lon, closest_lat, closest_lon)

        # Update the closest point if the new distance is smaller
        if distance_to_closest_point < min_distance:
            min_distance = distance_to_closest_point
            closest_point = (closest_lat, closest_lon)
            closest_alpha = t
            closest_interval = i

    # Calculate the time difference between the current time and the timetable for the closest interval
    current_time = datetime.now()
    current_minute = (current_time.minute + current_time.second / 60) % 60
    time_difference = math.floor((-dynamic_pins[pin_id - 1]["timetable"][closest_interval] + current_minute) % 60)

    # Update the time difference for the specific pin
    dynamic_pins[pin_id - 1]["time_difference"] = time_difference

    # Update the status to "Live"
    dynamic_pins[pin_id - 1]["popup"] = "Status: Live"

    expiration_time = datetime.now() + timedelta(minutes=2)
    dynamic_pins[pin_id - 1]["expiration_time"] = expiration_time

    return jsonify({"result": "Poziție mijloc de transport corectată"})

# website uses this endpoind for pins
@app.route('/get_dynamic_pins')
def get_dynamic_pins():
    updated_dynamic_pins = calculate_dynamic_pins_positions()

    return jsonify(updated_dynamic_pins)

@app.route('/home', methods=['POST','GET'])
def home():
      return render_template('index.html')

@app.route('/profil', methods=['POST','GET'])
def profil():
      return render_template('profilepage.html')

@app.route('/lini', methods=['POST','GET'])
def lini():
      return render_template('linii.html')

@app.route('/intarzieri', methods=['POST','GET'])
def intarzieri():
      return render_template('intarzierii.html')

@app.route('/register', methods=['POST','GET'])
def register():
      return render_template('registerpage.html')

@app.route('/inregistrare', methods=['POST','GET'])
def inregistrare():
      nume=str(request.form['nume'])
      email=str(request.form['email'])
      parola=str(request.form['parola'])
      nr_gen = random.randrange(1000, 10000)
      session['nr_gen'] = nr_gen
      session['nume'] = nume
      session['email'] = email
      session['parola'] = parola
      query = "SELECT COUNT(*) FROM useri WHERE email = %s"
      cursor.execute(query, (email,))
      result = cursor.fetchone()
      email_exists = result[0] > 0
      if(email_exists==0):
            sendEmail(email,nr_gen)
            return render_template('registerpage1.html', nr_gen=nr_gen, nume=nume,email=email,parola=parola)
      else:
            flash("Emailul exista deja. Incercati un email nou")
            return render_template('registerpage.html') 

@app.route('/verif', methods=['POST','GET'])
def verificare():
      nr=0
      nr_gen = session.get('nr_gen')
      nr=int(request.form['nr'])
      if(nr==nr_gen):
         insert_query = "INSERT INTO useri (nume, email, parola) VALUES (%s, %s, %s)"
         data_to_insert = (session.get('nume'), session.get('email'), session.get('parola'))
         cursor.execute(insert_query, data_to_insert)
         connection.commit()
         cursor.close()
         connection.close()
         return render_template('mappage.html')
      else:
        
        flash("Cod Gresit. Introdu din Nou")
        return render_template('registerpage1.html')   

@app.route('/log', methods=['POST','GET'])
def logi():
      return render_template('loginpagepage.html')

@app.route('/logare', methods=['POST','GET'])
def logare():
      email='asdfguioipiuytrdfghjklkkjhg'
      email=str(request.form['email'])
      parola=str(request.form['parola'])
      query = "SELECT COUNT(*) FROM useri WHERE email = %s AND parola = %s"
      cursor.execute(query, (email, parola,))
      result = cursor.fetchone()
      email_exists = result[0] > 0
      if(email_exists==1):
           
            return render_template('mappage.html')
      else:
            flash("Contul nu exista.")
            return render_template('loginpagepage.html') 


if __name__=="__main__":
    app.run(debug=True, port=8080)