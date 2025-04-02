from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required
from .forms import EmployeeForm
from .models import Employee
from app.modules.auth.models import User
from app.extensions import db

employee_bp = Blueprint('employee', __name__, 
                      template_folder='templates',
                      url_prefix='/employees')

@employee_bp.route('/')
@login_required
def list_employees():
    employees = Employee.query.order_by(Employee.full_name).all()
    return render_template('employee/list.html', employees=employees)

@employee_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_employee():
    form = EmployeeForm()
    
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.flush()

            employee = Employee(
                user_id=user.id,
                full_name=f"{form.first_name.data} {form.last_name.data}",
                position=form.position.data,
                salary=float(form.salary.data),
                department=form.department.data,
                metadata={
                    'phone': form.phone.data,
                    'address': form.address.data,
                    'hire_date': form.hire_date.data
                }
            )
            db.session.add(employee)
            db.session.commit()
            
            flash('Funcionário criado com sucesso!', 'success')
            return redirect(url_for('employee.list_employees'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('Falha na criação de funcionário', exc_info=True)
            flash(f'Erro: {str(e)}', 'danger')
    
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erro no campo {getattr(form, field).label.text}: {error}", 'warning')
        flash('Corrija os erros no formulário', 'warning')

    return render_template('employee/create.html', form=form)

@employee_bp.route('/<uuid:employee_id>')
@login_required
def employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee/detail.html', employee=employee)


@employee_bp.route('/vulnerable', methods=['GET', 'POST'])
@login_required
def vulnerable_employee_detail():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id', '').split(' ')[0]
        
        try:
            raw_query = f"SELECT * FROM hr.employees WHERE id::text LIKE '%{employee_id}'"
            
            conn = db.engine.raw_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute(raw_query)
                
                try:
                    result = cursor.fetchall()
                    employees = [dict(zip([col[0] for col in cursor.description], row)) for row in result]
                except:
                    employees = []
                    conn.commit()
                    
            finally:
                cursor.close()
                conn.close()
            
            return render_template('employee/detail.html',
                                employees=employees,
                                vulnerable=True)
        except Exception as e:
            current_app.logger.error(f"SQL Injection attempt: {str(e)}")
            flash(f'Erro na consulta: {str(e)}', 'danger')
            
        return redirect(url_for('employee.vulnerable_employee_detail'))
    
    return render_template('employee/vulnerable_form.html')


@employee_bp.route('/edit/<uuid:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)
    
    if form.validate_on_submit():
        try:
            employee.full_name = f"{form.first_name.data} {form.last_name.data}"
            employee.position = form.position.data
            employee.salary = form.salary.data
            employee.department = form.department.data
            employee.metadata = {
                'phone': form.phone.data,
                'address': form.address.data
            }
            
            employee.user.email = form.email.data
            if form.password.data:
                employee.user.set_password(form.password.data)
            
            db.session.commit()
            flash('Dados atualizados!', 'success')
            return redirect(url_for('employee.employee_detail', employee_id=employee.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')
    
    names = employee.full_name.split(' ', 1)
    form.first_name.data = names[0]
    form.last_name.data = names[1] if len(names) > 1 else ''
    form.email.data = employee.user.email
    
    return render_template('employee/edit.html', form=form, employee=employee)

@employee_bp.route('/delete/<uuid:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    user = employee.user
    
    try:
        db.session.delete(employee)
        db.session.delete(user)
        db.session.commit()
        flash('Funcionário removido!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')
    
    return redirect(url_for('employee.list_employees'))