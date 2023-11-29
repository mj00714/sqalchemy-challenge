import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

##################################
# Database Setup
##################################
engine = create_engine ('sqlite:///../Resources/hawaii.sqlite')

# reflect an existing db into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

##################################
# Flask Setup
##################################

app = Flask(__name__)

##################################
# Flask Routes
##################################

@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f'<h2>Available routes for historical Hawaii weather data</h2><br/>'
        f'Percipitation Data Route: /api/v1.0/percipitation<br/>'
        f'Available Weather Stations Route: /api/v1.0/stations<br/>'
        f'Tempature Data Route (for station USC00519281): /api/v1.0/tobs<br/>'
        f'Start Date Only Route: /api/v1.0/<start_date><br/>'
        f'Start <em>and</em> End Date Route: /api/v1.0/<start_date>/<end_date><br/><br>'
        f'<b>*** Note that the last two routes allow you to enter dates between 2016-08-23 and 2017-08-23. Dates must be entered in YYYY-MM-DD format and the start and end date must be separated by the "/". If one date is entered, it will be a start date that defaults to an end date of 2017-08-23.</b>'
    )

@app.route('/api/v1.0/percipitation')
def percipitation():
    # create the session link from python to the db
    session = Session(engine)

    """Return a list of daily percipitation from 8/23/16 to 8/23/17"""
    # query the daily percipitation from all stations during the stated time period

    start_date = '2016-08-23'
    sel = [measurement.date,
           func.sum(measurement.prcp)]
    percipitation = session.query(*sel).\
        filter(measurement.date >= start_date).\
        group_by(measurement.date).\
        order_by(measurement.date).all()
    
    session.close()

    # return the dictionary with the date as the key and the percipitation as the value
    percipitation_dates = []
    percipitation_totals = []

    # run a for loop to populate the lists

    for date, dailytotal in percipitation:
        percipitation_dates.append(date)
        percipitation_totals.append(dailytotal)

    percipitation_dictionary = dict(zip(percipitation_dates, percipitation_totals))

    return jsonify(percipitation_dictionary)

# repeat for stations

@app.route('/api/v1.0/stations')
def stations():
    # create the session link from python to the db
    session = Session(engine)

    """Return a list of the active weather stations in HI"""
    # return the list of weather stations
    sel = [station.station]
    local_stations = session.query(station.station).all()
    session.close()

    # return the dictionary with the stations
    station_list = list(np.ravel(local_stations))

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    #create the session link from python to the db
    session = Session(engine)

    """Return the historical temperatures between the given dates"""
    # query the data between 8/23/16 and 8/23/17 for the recorded temperatures for the most active station
    start_date = '2016-08-23'
    sel = [measurement.date,
           measurement.tobs]
    temps = session.query(*sel).\
        filter(measurement.date >= start_date, measurement.station == 'USC00519281').\
        group_by(measurement.date).\
        order_by(measurement.date).all()
    
    session.close()

    # return the dictionary with the date as the key and temp as the value

    record_dates = []
    record_temps = []

    for date, record in temps:
        record_dates.append(date)
        record_temps.append(record)

    station_tobs_dictionary = dict(zip(record_dates, record_temps))

    return jsonify(station_tobs_dictionary)

@app.route('/api/v1.0/<start_date>')
def sample_trip_1(start_date=None, end_date='2017-08-23'):
    # this query route will default to the latest possible end date. min, average and max temps for the range

    session = Session(engine)
    query = session.query(func.min(measurement.tobs), 
        func.avg(measurement.tobs), 
        func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    trip_detail = []
    for min, avg, max in query:
        trip_dictionary = {}
        trip_dictionary['Min'] = min
        trip_dictionary['Avg'] = avg
        trip_dictionary['Max'] = max
        trip_detail.append(trip_dictionary)

    # error check for null results
    if trip_dictionary['Min']:
        return jsonify(trip_detail)
    else:
        return jsonify({"Error: you must enter a YYYY-MM-DD formatted start date for your query"})
    
@app.route('/api/v1.0/<start_date>/<end_date>')
def sample_trip_2(start_date, end_date):
    # this query route will require a start and end date. min, average and max temps for the range

    session = Session(engine)
    query = session.query(func.min(measurement.tobs), 
        func.avg(measurement.tobs), 
        func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    trip_detail = []
    for min, avg, max in query:
        trip_dictionary = {}
        trip_dictionary['Min'] = min
        trip_dictionary['Avg'] = avg
        trip_dictionary['Max'] = max
        trip_detail.append(trip_dictionary)

    # error check for null results
    if trip_dictionary['Min'] and trip_dictionary['Max']:
        return jsonify(trip_detail)
    else:
        return jsonify({"Error: you must enter a YYYY-MM-DD formatted start and end dates for your query"})
    

if __name__ == '__main__':
    app.run(debug=True)