from datetime import *
from dateutil.rrule import *

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Chores, Workers

app = Flask(__name__)

# Connect to database and create database session
engine = create_engine('sqlite:///chores.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

freqTypes = ('By Week Day', 'By Month Day', 'Monthly', 'Yearly')

def listDates(dtstart, dtend, freq, values):
    # freq 0=byweekday, 1=bymonthday, 2=MONTHLY, 3=YEARLY
    dates = []
    date = []
    dtexec = dtstart
    while dtexec <= dtend:
        if freq == 0:
            date = list(rrule(DAILY, count=2, byweekday=values, 
                dtstart=dtexec, cache=True))
        elif freq == 1:
            date = list(rrule(DAILY, count=2, bymonthday=values, 
                dtstart=dtexec, cache=True))
        elif freq == 2:
            date = list(rrule(MONTHLY, count=2, dtstart=dtexec, 
                interval=values, cache=True))
        elif freq == 3:
            date = list(rrule(YEARLY, count=2, dtstart=dtexec, 
                interval=values, cache=True))
        if len(date) > 0:
            dtexec = date[0]
            if dtexec <= dtend:
                dates.append(dtexec)
            dtexec = date[1]
        else:
            break
    return dates


@app.route('/')
def list_chores():
    returnStr = ''
    chores = session.query(Chores).all()
    for c in chores:
        returnStr += c.name + '<br>'
    return render_template('list_chores.html', chores=chores, freqTypes=freqTypes)


@app.route('/add_chore', methods=['GET', 'POST'])
def add_chore():
    if request.method == 'POST':
        if request.form['start_date'] == '':
            startDate = None
        else:
            startDate = datetime.strptime(request.form['start_date'],'%Y-%m-%d').date()
        if request.form['end_date'] == '':
            endDate = None
        else:
            endDate = datetime.strptime(request.form['end_date'],'%Y-%m-%d').date()
        if request.form['freq'] == '0':
            dayList = request.form.getlist('weekday')
            dayListInt = []
            for day in dayList:
                dayListInt.append(int(day))
            days = str(dayListInt)
            newValues = days[1:-1]
        else:
            newValues = request.form['values']
        newChore = Chores(name=request.form['name'], 
            start_date=startDate, end_date=endDate,
            freq=request.form['freq'],
            values=newValues)
        session.add(newChore)
        session.commit()
        return redirect(url_for('list_chores'))
    else:
        return render_template('add_chore.html', freqTypes=freqTypes)


@app.route('/dates')
def dates():
    returnStr = 'listing dates'
    # dateList = listDates(datetime(2015,8,15),datetime(2018,12,15), 3, 1)
    # dateList = listDates(datetime(2015,8,15),datetime(2016,12,15), 0, (1,3))
    values = '1,3,5'.split(',')
    valuesInt = []
    for v in values:
        valuesInt.append(int(v))
    dateList = listDates(datetime(2015,8,15),datetime(2016,12,15), 0, valuesInt)
    for d in dateList:
        returnStr += '<br>' + d.strftime ('%A, %B %e, %Y')
    return returnStr


if __name__ == '__main__':
    app.run(host='10.0.2.15',debug=True)
