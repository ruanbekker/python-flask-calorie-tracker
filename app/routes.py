from flask import render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Food, Meal
from datetime import datetime
from sqlalchemy import func
from flask import current_app as app

@app.route('/')
def index():
    today = datetime.utcnow().date()
    meals = Meal.query.filter_by(date=today).all()
    total_calories = sum(m.food.calories * m.quantity for m in meals)
    return render_template('index.html', meals=meals, total_calories=total_calories)

@app.route('/add-food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        food = Food(
            name=request.form['name'],
            protein=float(request.form['protein']),
            carbs=float(request.form['carbs']),
            fat=float(request.form['fat']),
            calories=float(request.form['calories'])
        )
        db.session.add(food)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_food.html')

@app.route('/log-meal', methods=['GET', 'POST'])
def log_meal():
    foods = Food.query.all()
    if request.method == 'POST':
        meal = Meal(
            category=request.form['category'],
            food_id=int(request.form['food_id']),
            quantity=float(request.form['quantity']),
            date=datetime.utcnow().date()
        )
        db.session.add(meal)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('log_meal.html', foods=foods)

@app.route('/report')
def report():
    daily_totals = (
        db.session.query(Meal.date, func.sum(Meal.quantity * Food.calories))
        .join(Food)
        .group_by(Meal.date)
        .order_by(Meal.date)
        .all()
    )
    labels = [d[0].strftime('%Y-%m-%d') for d in daily_totals]
    values = [round(d[1], 2) for d in daily_totals]

    return render_template('report.html', labels=labels, values=values, data=daily_totals)

