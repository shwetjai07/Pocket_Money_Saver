from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import User, Transaction
from . import db
from datetime import datetime, timedelta, timezone

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def index():
    txns = Transaction.query.filter_by(user_id=current_user.id).all()

    today = datetime.now(timezone.utc).date()

    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    #Daily
    income_today = sum(t.amount for t in txns if t.type == 'income' and t.date.date() == today)
    expense_today = sum(t.amount for t in txns if t.type == 'expense' and t.date.date() == today)

    #Weekly
    income_week = sum(t.amount for t in txns if t.type == 'income' and start_of_week <= t.date.date() <= today)
    expense_week = sum(t.amount for t in txns if t.type == 'expense' and start_of_week <= t.date.date() <= today)

    #Monthly
    income_month = sum(t.amount for t in txns if t.type == 'income' and start_of_month <= t.date.date() <= today)
    expense_month = sum(t.amount for t in txns if t.type == 'expense' and start_of_month <= t.date.date() <= today)

    #Calculation
    income = sum(t.amount for t in txns if t.type == 'income')
    expense = sum(t.amount for t in txns if t.type == 'expense')

    balance = income - expense

    txnList = [[txn.type, txn.tags, txn.reason, txn.date.date(), txn.amount] for txn in txns]
    txnList.reverse()
    
    return render_template('index.html',
                           user=current_user,
                           balance=balance,
                           income_today=income_today,
                           expense_today=expense_today,
                           income_week=income_week,
                           expense_week=expense_week,
                           income_month=income_month,
                           expense_month=expense_month,
                           txnList=txnList)


@routes.route('/add-transaction', methods=['POST'])
def add_transaction():
    amount = float(request.form.get('amount'))
    tag = request.form.get('tag')
    reason = request.form.get('reason')
    ttype = request.form.get('type')
    print(request.form.get('type'))

    new_txn = Transaction(
        amount=amount,
        reason=reason,
        tags=tag,
        type=ttype,
        user_id=current_user.id
    )

    db.session.add(new_txn)
    db.session.commit()

    flash('Transaction added successfully.', category='success')

    return redirect(url_for('routes.index'))

@routes.route('/tags', methods=['GET'])
def tags():
    return redirect(url_for('routes.index'))


@routes.route('/analysis', methods=['GET'])
def analysis():
    return redirect(url_for('routes.index'))