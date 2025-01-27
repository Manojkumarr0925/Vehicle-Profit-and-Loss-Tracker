from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app import app

vehicles = []
entries = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vehicle_options', methods=['GET', 'POST'])
def vehicle_options():
    session_vehicles = session.get('vehicles', vehicles)
    if request.method == 'POST':
        selected_vehicle = request.form.get('vehicle')
        if selected_vehicle:
            return redirect(url_for('manage_vehicle', vehicle_name=selected_vehicle))
    return render_template('vehicle_options.html', vehicles=session_vehicles)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    vehicle_name = request.form.get('vehicle_name')
    session_vehicles = session.get('vehicles', vehicles)
    if vehicle_name in session_vehicles:
        flash(f"Vehicle {vehicle_name} has already been added.", 'error')
        return redirect(url_for('vehicle_options'))
    if vehicle_name:
        return render_template('add_vehicle_confirmation.html', vehicle_name=vehicle_name)
    flash("Please enter a vehicle name.", 'error')
    return redirect(url_for('vehicle_options'))

@app.route('/confirm_add_vehicle', methods=['POST'])
def confirm_add_vehicle():
    vehicle_name = request.form.get('vehicle_name')
    confirmation = request.form.get('confirmation')
    session_vehicles = session.get('vehicles', vehicles)
    if confirmation == 'Yes':
        if vehicle_name not in session_vehicles:
            session_vehicles.append(vehicle_name)
            entries[vehicle_name] = []
            session['vehicles'] = session_vehicles
            flash(f"Vehicle {vehicle_name} added successfully!", 'success')
        else:
            flash(f"Vehicle {vehicle_name} has already been added.", 'error')
            return redirect(url_for('vehicle_options'))
    return redirect(url_for('vehicle_options'))

@app.route('/edit_vehicle', methods=['POST'])
def edit_vehicle():
    old_vehicle = request.form.get('old_vehicle')
    new_vehicle = request.form.get('new_vehicle')
    session_vehicles = session.get('vehicles', vehicles)
    if old_vehicle == new_vehicle:
        flash("Same vehicle number cannot be edited.", 'error')
    elif new_vehicle in session_vehicles:
        flash(f"Vehicle {new_vehicle} already exists.", 'error')
    elif old_vehicle in session_vehicles:
        flash(f"Do you want to edit {old_vehicle} to {new_vehicle}?", 'confirm')
    return redirect(url_for('vehicle_options'))

@app.route('/confirm_edit_vehicle', methods=['POST'])
def confirm_edit_vehicle():
    old_vehicle = request.form.get('old_vehicle')
    new_vehicle = request.form.get('new_vehicle')
    confirmation = request.form.get('confirmation')
    session_vehicles = session.get('vehicles', vehicles)
    if confirmation == 'Yes' and old_vehicle in session_vehicles:
        index = session_vehicles.index(old_vehicle)
        session_vehicles[index] = new_vehicle
        entries[new_vehicle] = entries.pop(old_vehicle)
        session['vehicles'] = session_vehicles
        flash(f"Vehicle {old_vehicle} successfully edited to {new_vehicle}!", 'success')
    return redirect(url_for('vehicle_options'))

@app.route('/delete_vehicle', methods=['POST'])
def delete_vehicle():
    vehicle = request.form.get('vehicle')
    return render_template('delete_confirmation.html', message=f"Do you want to delete this vehicle {vehicle}?", vehicle=vehicle)

@app.route('/confirm_delete_vehicle', methods=['POST'])
def confirm_delete_vehicle():
    vehicle = request.form.get('vehicle')
    confirmation = request.form.get('confirmation')
    session_vehicles = session.get('vehicles', vehicles)
    if confirmation == 'Yes' and vehicle in session_vehicles:
        session_vehicles.remove(vehicle)
        entries.pop(vehicle, None)
        session['vehicles'] = session_vehicles
        flash(f"Vehicle {vehicle} has been successfully deleted!", 'success')
    return redirect(url_for('vehicle_options'))

@app.route('/manage_vehicle/<vehicle_name>')
def manage_vehicle(vehicle_name):
    return render_template('manage_vehicle.html', vehicle_name=vehicle_name)

@app.route('/add_entry/<vehicle_name>', methods=['GET', 'POST'])
def add_entry(vehicle_name):
    if request.method == 'POST':
        date = request.form.get('date')
        entry_type = request.form.get('entry_type')
        amount = float(request.form.get('amount'))  # Convert amount to float
        description = request.form.get('description')
        entries[vehicle_name].append({'date': date, 'entry_type': entry_type, 'amount': amount, 'description': description})
        flash("Entry added successfully!", 'success')
        return redirect(url_for('manage_vehicle', vehicle_name=vehicle_name))
    return render_template('add_entry.html', vehicle_name=vehicle_name)

@app.route('/edit_entry/<vehicle_name>', methods=['GET', 'POST'])
def edit_entry(vehicle_name):
    if request.method == 'POST':
        selected_entry = request.form.get('selected_entry')
        date = request.form.get('date')
        entry_type = request.form.get('entry_type')
        amount = request.form.get('amount')
        description = request.form.get('description')
        if selected_entry and date and entry_type and amount and description:
            selected_entry = int(selected_entry)
            return render_template('entry_confirmation.html', message=f"Do you want to edit this entry in {vehicle_name}?", vehicle_name=vehicle_name, entry_index=selected_entry, date=date, entry_type=entry_type, amount=amount, description=description)
        else:
            flash("All fields are required.", 'error')
            return redirect(url_for('edit_entry', vehicle_name=vehicle_name, selected_entry=selected_entry))
    selected_entry = request.args.get('selected_entry')
    if selected_entry is not None:
        selected_entry = int(selected_entry)
        return render_template('edit_entry.html', vehicle_name=vehicle_name, entries=entries[vehicle_name], selected_entry=selected_entry)
    else:
        flash("No entry selected for editing.", 'error')
        return redirect(url_for('transactions', vehicle_name=vehicle_name))

@app.route('/confirm_edit_entry', methods=['POST'])
def confirm_edit_entry():
    vehicle_name = request.form.get('vehicle_name')
    entry_index = int(request.form.get('entry_index'))
    date = request.form.get('date')
    entry_type = request.form.get('entry_type')
    amount = request.form.get('amount')
    description = request.form.get('description')
    confirmation = request.form.get('confirmation')
    if confirmation == 'Yes':
        try:
            amount = float(amount) if amount else 0.0  # Ensure amount is converted to float
            entries[vehicle_name][entry_index] = {'date': date, 'entry_type': entry_type, 'amount': amount, 'description': description}
            flash("Entry edited successfully!", 'success')
        except ValueError:
            flash("Invalid amount value.", 'error')
    return redirect(url_for('manage_vehicle', vehicle_name=vehicle_name))

@app.route('/delete_entry/<vehicle_name>', methods=['GET', 'POST'])
def delete_entry(vehicle_name):
    if request.method == 'POST':
        selected_entry = int(request.form.get('selected_entry'))
        return render_template('delete_entry_confirmation.html', message=f"Do you want to delete this entry from {vehicle_name}?", vehicle_name=vehicle_name, entry_index=selected_entry)
    return render_template('delete_entry.html', vehicle_name=vehicle_name, entries=entries[vehicle_name])

@app.route('/confirm_delete_entry', methods=['POST'])
def confirm_delete_entry():
    vehicle_name = request.form.get('vehicle_name')
    entry_index = int(request.form.get('entry_index'))
    confirmation = request.form.get('confirmation')
    if confirmation == 'Yes':
        entries[vehicle_name].pop(entry_index)
        flash("Entry deleted successfully!", 'success')
    return redirect(url_for('manage_vehicle', vehicle_name=vehicle_name))

@app.route('/summary/<vehicle_name>', methods=['GET', 'POST'])
def summary(vehicle_name):
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        compare_vehicles = request.form.getlist('compare_vehicles')
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        total_income = sum(entry['amount'] for entry in entries[vehicle_name] if entry['entry_type'] == 'Income' and start_date_obj <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date_obj)
        total_expense = sum(entry['amount'] for entry in entries[vehicle_name] if entry['entry_type'] == 'Expense' and start_date_obj <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date_obj)
        net_profit_loss = total_income - total_expense

        summary = {
            'income': total_income,
            'expense': total_expense,
            'net': net_profit_loss
        }

        compare_summaries = []
        for compare_vehicle in compare_vehicles:
            compare_income = sum(entry['amount'] for entry in entries[compare_vehicle] if entry['entry_type'] == 'Income' and start_date_obj <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date_obj)
            compare_expense = sum(entry['amount'] for entry in entries[compare_vehicle] if entry['entry_type'] == 'Expense' and start_date_obj <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date_obj)
            compare_net = compare_income - compare_expense

            compare_summaries.append({
                'vehicle_name': compare_vehicle,
                'income': compare_income,
                'expense': compare_expense,
                'net': compare_net
            })

        return render_template('summary.html', vehicle_name=vehicle_name, summary=summary, start_date=start_date, end_date=end_date, compare_summaries=compare_summaries, vehicles=vehicles)

    return render_template('summary.html', vehicle_name=vehicle_name, vehicles=vehicles)

@app.route('/transactions/<vehicle_name>')
def transactions(vehicle_name):
    if vehicle_name not in entries:
        flash(f"Vehicle {vehicle_name} not found.", 'error')
        return redirect(url_for('vehicle_options'))
    
    # Sort entries by date in ascending order
    sorted_entries = sorted(entries[vehicle_name], key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
    return render_template('transactions.html', vehicle_name=vehicle_name, entries=sorted_entries)


if __name__ == "__main__":
    app.run(debug=True)
