#################################################
# Libraries
#################################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, distinct, inspect

from datetime import timedelta, datetime

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """All routes available:"""
    return (
        f"<br>All routes availabe:</br>"
        f"<br><a href=api/precipitation>/api/precipitation</a></br>"
        f"<br><a href=api/stations>/api/stations</a></br>"
        f"<br><a href=api/temperature>/api/temperature</a></br>"
        f"<br>/api/</br>"
        

    )


@app.route("/api/precipitation")
def precipitation():
    """Return a list of precipitation data"""
    # Create our session (link) from Python to the DB
    session = Session(engine)
   # Dates
    # find the last recording date
    max_date = session.query(func.max(Measurement.date)).all()
    end_date = max_date[0][0] # last recording date
    # find 1 year prior to the last recording date
    year = timedelta(days=365)
    # convert last recording date to date format
    end_date_ = datetime.strptime(end_date, '%Y-%m-%d')
    # calculate begin date
    begin_date_ = end_date_ - year
    # Query 
    sel_p = [ Measurement.date, 
            Measurement.prcp]
    precipitation_query =   session.query(*sel_p).\
                            filter(Measurement.date >= begin_date_, Measurement.date <= end_date_).all()

    # Convert list of tuples into normal list
    precipitation_dict = dict(precipitation_query)
    session.close()

    return jsonify(precipitation_dict)


@app.route("/api/stations")
def stations():
    """Return a list of station data"""
   # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query 
    sel_s = [Measurement.station]
    stations_query =    session.query(*sel_s).\
                        group_by(Measurement.station).\
                        order_by(Measurement.station).all()
    session.close()

    return jsonify(stations_query)

@app.route("/api/temperature")
def temperature():
    """Return a list of temperature data"""
   # Create our session (link) from Python to the DB
    session = Session(engine)
    # Dates
    # find the last recording date
    max_date = session.query(func.max(Measurement.date)).all()
    end_date = max_date[0][0] # last recording date
    # find 1 year prior to the last recording date
    year = timedelta(days=365)
    # convert last recording date to date format
    end_date_ = datetime.strptime(end_date, '%Y-%m-%d')
    # calculate begin date
    begin_date_ = end_date_ - year
    # Query 
    sel_p = [ Measurement.tobs]
    temperature_query =   session.query(*sel_p).\
                            filter(Measurement.date >= begin_date_, Measurement.date <= end_date_).all()
    session.close()
    
    return jsonify(temperature_query)

@app.route("/api/<start>")
def calc_temps(start):
    """the minimum temperature, the average temperature, and the max temperature for a given date range."""
   # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)]
    calc_temp_query = session.query(*sel).filter(Measurement.date >= start).all()

    return jsonify(calc_temp_query)

@app.route("/api/<start>/<end>")
def calc_temps_range(start, end):
    """the minimum temperature, the average temperature, and the max temperature for a given date range."""
   # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)]
    calc_temp_range_query = session.query(*sel).filter(Measurement.date >= start, Measurement.date <= end).all()
        
    return jsonify(calc_temp_range_query)


if __name__ == '__main__':
    app.run(debug=True)
