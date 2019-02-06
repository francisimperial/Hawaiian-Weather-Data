import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy.pool import SingletonThreadPool

engine = create_engine("sqlite:///Resources/hawaii.sqlite", poolclass=SingletonThreadPool)
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
    """List of all available routes"""
    return(
        f"Available routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"~ Query dates and temperatures from the last year (8/23/2016)<br/>"
        f"/api/v1.0/stations<br/>"
        f"~ List of active stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"~ List of Temperature Observations from the last year (8/23/2016)<br/>"
        f"/api/v1.0/start<br/>"
        f"~ Returns Minimum, Maximum, and Average Temperatures for a given date<br/>"
        f"/api/v1.0/start_end<br/>"
        f"~ Returns Minimum, Maximum, and Average Temperatures for a given period<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query dates and temperatures from last year"""
    
    # Query from the year before the last date 
    precip_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > "2016-08-23").all()

    # Create dictionary with date as the key with the temps
    precip_all = []
    for precip in precip_query:
        precip_dict = {}
        precip_dict['Date'] = precip[0]
        precip_dict['TOBS'] = precip[1]
        precip_all.append(precip_dict)
    
    return jsonify(precip_all)

@app.route("/api/v1.0/stations")
def stations():
    """Lists all active stations"""

    # Query stations
    station_query = session.query(Station.name, Station.station).all()

    # Create dictionary with name and station as keys
    station_all = []
    for station in station_query:
        station_dict = {}
        station_dict['Name'] = station[0]
        station_dict['Station'] = station[1]
        station_all.append(station_dict)
    
    return jsonify(station_all)

@app.route("/api/v1.0/tobs")
def tobs():
    """Lists all Temperature Observations from the last year"""

    # Query tobs from the last year
    tobs_query = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date > "2016-08-23").all()
    
    # Create dictionary with name, date, and tobs as keys
    tobs_all = []
    for tob in tobs_query:
        tobs_dict = {}
        tobs_dict['Name'] = tob[0]
        tobs_dict['Date'] = tob[1]
        tobs_dict['Tobs'] = tob[2]
        tobs_all.append(tobs_dict)
    
    return jsonify(tobs_all)

@app.route("/api/v1.0/start")
def given_date(date):
    """Return Minimum, Maximum, and Average Temperatures of a given date"""

    # Query for given date
    date_query = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date == date).all()
    
    # Create dictionary with Date and temps as keys
    date_info = []
    for date in date_query:
        date_dict = {}
        date_dict['Date'] = date[0]
        date_dict['Min Temp'] = date[1]
        date_dict['Max Temp'] = date[2]
        date_dict['Avg Temp'] = date[3]
        date_info.append(date_dict)
    
    return jsonify(date_info)

@app.route("/api/v1.0/start_end")
def given_period(start, end):
    """Return Minimum, Maximum, and Average Temperatures of a given period"""

    # Query for given period 
    period_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start,end)).all()
    
    # Create dictionary for temp information on given period
    period_info = []
    for period in period_query:
        period_dict = {}
        period_dict["Start Date"] = start
        period_dict["End Date"] = end
        period_dict["Min Temp"] = period[0]
        period_dict["Max Temp"] = period[1]
        period_dict["Avg Temp"] = period[2]
        period_info.append(period_dict)

    return jsonify(period_info)

if __name__ == '__main__':
    app.run(debug=True)