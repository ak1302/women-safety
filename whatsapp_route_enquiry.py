
# Download the helper library from https://www.twilio.com/docs/python/install
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

from twilio.rest import Client
from tkinter import *
import time
from selenium import webdriver
import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from selenium.webdriver.common.keys import Keys
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


import speech_recognition as speech
import pickle
from tkinter import *
import time
from selenium import  webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from selenium.webdriver.common.keys import Keys


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""

    # body = request.values.get('Body', None)
    src = request.form.get('src')
    dest = request.form.get('des')

    # Start our response





    from selenium import webdriver
    
    # selenium webdriver path in your system...
    service = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.get('https://www.google.com/maps/dir///@27.9107022,78.0760799,15z/data=!4m2!4m1!3e0')

    driver.set_window_size(1024,600)
    driver.maximize_window()

    time.sleep(5)


    dataset1 = pd.read_csv('crime.csv')
    X = dataset1.drop('Crime value', axis=1)
    y = dataset1['Crime value']

    #from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    #from sklearn.tree import DecisionTreeRegressor
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)

    driver.find_element(By.XPATH,'//*[@id="sb_ifc50"]/input').send_keys(src)
    driver.find_element(By.XPATH, '//*[@id="sb_ifc51"]/input').send_keys(dest)
    driver.find_element(By.XPATH, '//*[@id="sb_ifc51"]/input').send_keys(Keys.RETURN)

    time.sleep(5)



    road_xpath = '//h1[@id="section-directions-trip-title-0" or @id="section-directions-trip-title-1" or@id="section-directions-trip-title-2"]/span'
    roads = driver.find_elements(By.XPATH, road_xpath)
    print(roads)

    list_of_via_roads_final1 = [None,]
    list_of_via_roads_final2 = []


    for road in roads:
        road_name = road.text
        print(road_name)
        list_of_via_roads_final2.append(road_name)
        check_for_and = "and" in road_name
        check_for_slash = "/" in road_name



        if check_for_and == True:

            road_name_final1 = road_name.split('and')[0].strip()
            road_name_final2 = road_name.split('and')[1].strip()
            list_of_via_roads_final1.append(road_name_final1)
            for items in range(len(list_of_via_roads_final1)):
                if list_of_via_roads_final1[items] == road_name_final1:
                    list_of_via_roads_final1.append(road_name_final2)

                else:
                    list_of_via_roads_final1.append(road_name_final1)


        elif check_for_slash == True:

            road_name_final1 = road_name.split('/')[0].strip()
            list_of_via_roads_final1.append(road_name_final1)

        else:
            road_name_final1 = road_name
            list_of_via_roads_final1.append(road_name_final1)

    print(road_name)
    # pickle.dump(road,open('model.pkl','wb'))



    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    # Remove duplicates from this list.
    values = list_of_via_roads_final1
    result = remove_duplicates(values)

    list_of_via_roads_final1 = result



    clean = [x for x in list_of_via_roads_final1 if x != None]
    print(clean)

    b = 0
    c = 0
    A = [None] * 5
    for i in range(len(clean)):
        # name_of_road = list_of_via_roads_final1[i]
        csv_file = csv.reader(open('roads.csv', 'r', encoding='utf-8'))
        # print(name_of_road)

        for row in csv_file:
            if clean[i] == row[0]:
    #             print(row)
                row.pop(0)
                #print(row)
                #print(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                A[i] = regressor.predict([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]]])

    #             print(A[i])
                b = b + 1

    m = A[0]
    # print(A)
    for i in range(b):
       if int(m)> int(A[i]):
           m = A[i]
           c = i


    # print(m)
    # print(c)


    time.sleep(1)
    clicking_path = f'//div[@id="section-directions-trip-{c}"]'

    driver.find_element(By.XPATH, clicking_path).click()
    try:
        driver.find_element(By.XPATH, clicking_path).click()
    except:
        pass

    print("Safest route will be via " + list_of_via_roads_final2[c])
    final_result = "Safest route will be via " + list_of_via_roads_final2[c]


    time.sleep(5)

    url_current = driver.current_url
    print(url_current)
    return jsonify({'safest route': url_current})


    label3 = Label(text = final_result,font= 50)
    label3.place(x=400,y=380)

    # your twilio auth_token and account_sid...
    account_sid = 'AC3b2160df9122f450dead692e51dff8d4'
    auth_token = 'ea79b13fb53fdc8e85565239a9003d81'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Safest route between " +source + " and " +des + " will be via " +list_of_via_roads_final2[c] + "\n" +"The url is: " + url_current,
        
        # your twilio number...
        from_='+17069205692',
        
        # user's whatsapp number...
        to='+918108231625'
    )

    # return list_of_via_roads_final2[c]


    # Add a message
    # resp.message("Ahoy! Thanks so much for your message.")
    resp.message("Ahoy")

    return str(resp)


if __name__ == "__main__":
    app.run(debug='true')
