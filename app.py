from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
import string
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qrcodes.db'
app.config['UPLOAD_FOLDER'] = 'static/qrcodes'
db = SQLAlchemy(app)

def generate_display_code():
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not QRCode.query.filter_by(display_code=code).first():
            return code

def is_valid_path_identifier(identifier):
    # 检查标识符是否只包含字母、数字、下划线和连字符
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', identifier))

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    max_members = db.Column(db.Integer)
    current_members = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.Column(db.Integer, default=0)
    display_code = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, **kwargs):
        path_identifier = kwargs.pop('path_identifier', None)
        super(QRCode, self).__init__(**kwargs)
        
        if path_identifier and is_valid_path_identifier(path_identifier):
            # 检查自定义标识符是否已被使用
            existing = QRCode.query.filter_by(display_code=path_identifier).first()
            if not existing:
                self.display_code = path_identifier
            else:
                self.display_code = generate_display_code()
        else:
            self.display_code = generate_display_code()

with app.app_context():
    if not os.path.exists('static/qrcodes'):
        os.makedirs('static/qrcodes')
    db.create_all()
    
    # 检查现有记录是否有display_code
    qrcodes = QRCode.query.filter_by(display_code=None).all()
    for qrcode in qrcodes:
        qrcode.display_code = generate_display_code()
    db.session.commit()

@app.route('/')
def index():
    qrcodes = QRCode.query.order_by(QRCode.order).all()
    return render_template('index.html', qrcodes=qrcodes)

@app.route('/display')
def display():
    active_qrcode = QRCode.query.filter_by(is_active=True).order_by(QRCode.order).first()
    return render_template('display.html', qrcode=active_qrcode)

@app.route('/group/<display_code>')
def display_single(display_code):
    qrcode = QRCode.query.filter_by(display_code=display_code).first_or_404()
    return render_template('display.html', qrcode=qrcode, single_mode=True)

@app.route('/update_qrcode/<int:id>', methods=['POST'])
def update_qrcode(id):
    qrcode = QRCode.query.get_or_404(id)
    
    if 'qrcode' in request.files:
        file = request.files['qrcode']
        if file.filename != '':
            # 删除旧文件
            old_file_path = os.path.join('static', qrcode.image_path.lstrip('/'))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            
            # 保存新文件
            filename = f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            qrcode.image_path = f"/static/qrcodes/{filename}"
    
    if 'name' in request.form:
        qrcode.name = request.form['name']
    if 'max_members' in request.form:
        qrcode.max_members = int(request.form['max_members'])
    if 'order' in request.form:
        qrcode.order = int(request.form['order'])
    
    # 处理路径标识符的更新
    if 'path_identifier' in request.form and request.form['path_identifier'].strip():
        path_identifier = request.form['path_identifier'].strip()
        if is_valid_path_identifier(path_identifier):
            existing = QRCode.query.filter(QRCode.id != id, QRCode.display_code == path_identifier).first()
            if not existing:
                qrcode.display_code = path_identifier
            else:
                flash('路径标识已被使用，请选择其他标识')
                return redirect(url_for('index'))
        else:
            flash('路径标识只能包含字母、数字、下划线和连字符')
            return redirect(url_for('index'))
    
    db.session.commit()
    flash('二维码更新成功')
    return redirect(url_for('index'))

@app.route('/add_qrcode', methods=['POST'])
def add_qrcode():
    if 'qrcode' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('index'))
    
    file = request.files['qrcode']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    # 验证路径标识符
    path_identifier = request.form.get('path_identifier', '').strip()
    if path_identifier:
        if not is_valid_path_identifier(path_identifier):
            flash('路径标识只能包含字母、数字、下划线和连字符')
            return redirect(url_for('index'))
        if QRCode.query.filter_by(display_code=path_identifier).first():
            flash('路径标识已被使用，请选择其他标识')
            return redirect(url_for('index'))

    if file:
        filename = f"qrcode_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        new_qrcode = QRCode(
            name=request.form.get('name'),
            image_path=f"/static/qrcodes/{filename}",
            max_members=int(request.form.get('max_members', 500)),
            order=int(request.form.get('order', 0)),
            path_identifier=path_identifier
        )
        db.session.add(new_qrcode)
        db.session.commit()
        
        flash('QR Code added successfully')
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    qrcode = QRCode.query.get_or_404(id)
    action = request.form.get('action')
    
    if action == 'increment':
        qrcode.current_members = min(qrcode.current_members + 1, qrcode.max_members)
    elif action == 'decrement':
        qrcode.current_members = max(qrcode.current_members - 1, 0)
    
    if qrcode.current_members >= qrcode.max_members:
        qrcode.is_active = False
        next_qrcode = QRCode.query.filter(QRCode.order > qrcode.order, QRCode.current_members < QRCode.max_members).order_by(QRCode.order).first()
        if next_qrcode:
            next_qrcode.is_active = True
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_qrcode/<int:id>', methods=['POST'])
def delete_qrcode(id):
    qrcode = QRCode.query.get_or_404(id)
    if os.path.exists(os.path.join('static', qrcode.image_path.lstrip('/'))):
        os.remove(os.path.join('static', qrcode.image_path.lstrip('/')))
    db.session.delete(qrcode)
    db.session.commit()
    flash('QR Code deleted successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 