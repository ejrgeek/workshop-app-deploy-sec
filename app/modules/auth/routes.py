from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegistrationForm, ResetPasswordForm
from .models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__,
                   template_folder='templates/auth',
                   url_prefix='/auth')

@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('employee.list_employees'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next') or url_for('employee.list_employees')
            return redirect(next_page)
        
        flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('employee.list_employees'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                is_active=True
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar conta. Tente outro usuário/email.', 'danger')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            if not current_user.check_password(form.current_password.data):
                flash('Senha atual incorreta', 'danger')
                return render_template('auth/reset_password.html', form=form)
            
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Senha atualizada com sucesso!', 'success')
            return redirect(url_for('employee.list_employees'))
        
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar senha.', 'danger')
            current_user.logger.error(f"Erro ao atualizar senha: {str(e)}")
    
    return render_template('auth/reset_password.html', form=form)
