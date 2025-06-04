from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta'

# ---------------------------
# Datos de inventario: Lista de herramientas predefinidas
# Todas las instancias se marcan como "disponible"
# ---------------------------
tools = [
    # 🧪 A – Instrumentos de Medición
    {"id": 1, "name": "Multímetro Digital", "brand": "Fluke", "model": "117", "SKU": "A1", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 2, "name": "Tester de continuidad", "brand": "Extech", "model": "CT20", "SKU": "A2", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 3, "name": "Osciloscopio portátil 2 canales", "brand": "Hantek", "model": "2D42", "SKU": "A3", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 4, "name": "Calibrador Vernier Digital", "brand": "Mitutoyo", "model": "500-196-30", "SKU": "A4", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 5, "name": "Termómetro infrarrojo", "brand": "Fluke", "model": "62 MAX", "SKU": "A5", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 6, "name": "Luxómetro", "brand": "Extech", "model": "LT300", "SKU": "A6", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 7, "name": "Tacómetro digital", "brand": "REED Instruments", "model": "R7050", "SKU": "A7", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 8, "name": "Manómetro digital", "brand": "WIKA", "model": "CPG1500", "SKU": "A8", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 9, "name": "Medidor de aislamiento", "brand": "Megger", "model": "MIT420/2", "SKU": "A9", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 10, "name": "Medidor de flujo de aire", "brand": "Testo", "model": "405i", "SKU": "A10", "instances": [{"instance_id": 1, "status": "disponible"}]},
    
    # 🔧 B – Herramientas Manuales
    {"id": 11, "name": "Juego destornilladores precisión", "brand": "Wiha", "model": "26199 (20 pzs)", "SKU": "B1", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 12, "name": "Destornillador aislado eléctrico", "brand": "Klein Tools", "model": "85076", "SKU": "B2", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 13, "name": "Juego de llaves Allen (mm)", "brand": "Bondhus", "model": "12137", "SKU": "B3", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 14, "name": "Juego de llaves Allen (pulg)", "brand": "Bondhus", "model": "12232", "SKU": "B4", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 15, "name": "Llave ajustable 6\"", "brand": "Bahco", "model": "8070", "SKU": "B5", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 16, "name": "Llave ajustable 10\"", "brand": "Bahco", "model": "8072", "SKU": "B6", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 17, "name": "Juego de llaves combinadas", "brand": "Stanley", "model": "89-010 (12 pzs)", "SKU": "B7", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 18, "name": "Pinzas punta fina 6\"", "brand": "Klein Tools", "model": "D203-6", "SKU": "B8", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 19, "name": "Pinzas punta fina 8\"", "brand": "Klein Tools", "model": "D203-8", "SKU": "B9", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 20, "name": "Pinzas de corte", "brand": "Knipex", "model": "70 06 160", "SKU": "B10", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 21, "name": "Pinzas de presión (tipo Vise-Grip)", "brand": "Irwin", "model": "10CR", "SKU": "B11", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 22, "name": "Martillo ", "brand": "Truper", "model": "MA-16F", "SKU": "B12", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 23, "name": "Sierra para metales", "brand": "Bahco", "model": "319", "SKU": "B14", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 24, "name": "Cúter retráctil", "brand": "Olfa", "model": "L-1", "SKU": "B15", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 25, "name": "Cepillo de alambre manual", "brand": "3M", "model": "048011", "SKU": "B16", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},

    # ⚡ C – Electricidad y Electrónica
    {"id": 26, "name": "Cautín tipo lápiz", "brand": "Hakko", "model": "FX-888D", "SKU": "C1", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 27, "name": "Estación de soldadura digital", "brand": "Weller", "model": "WE1010NA", "SKU": "C2", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 28, "name": "Lupa con pinzas 'tercera mano'", "brand": "Carson", "model": "CP-50", "SKU": "C3", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 29, "name": "Estuche de soldadura básica", "brand": "Weller", "model": "WLC100", "SKU": "C4", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 30, "name": "Cortafrío/Desforrador cable", "brand": "Ideal", "model": "45-121", "SKU": "C5", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 31, "name": "Pelacables automático", "brand": "Irwin", "model": "2078300", "SKU": "C6", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 32, "name": "Juego de pinzas miniatura (5 piezas)", "brand": "Stanley", "model": "84-114", "SKU": "C7", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 33, "name": "Bobina de estaño sin plomo", "brand": "Kester", "model": "24-9574-1402", "SKU": "C8", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 34, "name": "Bomba desoldadora", "brand": "Engineer", "model": "SS-02", "SKU": "C9", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 35, "name": "Fuente DC regulable 0–30V", "brand": "Korad", "model": "KA3005D", "SKU": "C10", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 36, "name": "Cables de prueba con caimanes", "brand": "Pomona", "model": "3781", "SKU": "C11", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(4)]},
    {"id": 37, "name": "Juego de mini clips para medición", "brand": "Fluke", "model": "AC283", "SKU": "C12", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},

    # 🧼 D – Herramientas Auxiliares y de Seguridad
    {"id": 38, "name": "Lupa con luz LED", "brand": "Aven", "model": "26501-LED", "SKU": "D1", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 39, "name": "Cepillos antiestáticos", "brand": "Velleman", "model": "ESD-BRUSH-SET", "SKU": "D2", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 40, "name": "Tapete antiestático con conexión", "brand": "ULINE", "model": "S-14117", "SKU": "D3", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 41, "name": "Pulsera antiestática", "brand": "ULINE", "model": "H-935", "SKU": "D4", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(5)]},
    {"id": 42, "name": "Dispensador de alcohol isopropílico", "brand": "Menda", "model": "35794", "SKU": "D5", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 43, "name": "Frascos de limpieza con punta fina", "brand": "Dynarex", "model": "4252", "SKU": "D6", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(3)]},
    {"id": 44, "name": "Lentes de seguridad", "brand": "3M", "model": "Virtua CCS", "SKU": "D7", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(5)]},
    {"id": 45, "name": "Guantes antiestáticos", "brand": "Ansell", "model": "11-800", "SKU": "D8", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(10)]},
    {"id": 46, "name": "Cubrebocas KN95", "brand": "3M", "model": "9502+", "SKU": "D9", "instances": [{"instance_id": 1, "status": "disponible"}]},
    
    # 🛠️ E – Herramientas Eléctricas
    {"id": 47, "name": "Taladro inalámbrico 12V", "brand": "Bosch", "model": "GSR 12V-30", "SKU": "E1", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 48, "name": "Minitaladro tipo Dremel", "brand": "Dremel", "model": "3000-1/25", "SKU": "E2", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 49, "name": "Juego brocas HSS (1–10 mm)", "brand": "Makita", "model": "D-46202", "SKU": "E3", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 50, "name": "Juego brocas concreto SDS (4 piezas)", "brand": "DeWalt", "model": "DW5207", "SKU": "E4", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]},
    {"id": 51, "name": "Mini amoladora angular", "brand": "Bosch", "model": "GWS 600", "SKU": "E5", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 52, "name": "Pistola de calor", "brand": "Wagner", "model": "HT1000", "SKU": "E6", "instances": [{"instance_id": 1, "status": "disponible"}]},
    {"id": 53, "name": "Atornillador eléctrico de precisión", "brand": "Wowstick", "model": "1F+", "SKU": "E7", "instances": [{"instance_id": i+1, "status": "disponible"} for i in range(2)]}
]

def sanitize_text(text):
    """
    Esta función reemplaza las comillas dobles por comillas simples
    para asegurarse de que el texto no rompa la sintaxis del JSON.
    """
    if not isinstance(text, str):
        return text
    return text.replace('"', "'")

# Recorre cada herramienta de la lista y limpia los valores de interés
for tool in tools:
    if 'name' in tool:
        tool['name'] = sanitize_text(tool['name'])
    if 'brand' in tool:
        tool['brand'] = sanitize_text(tool['brand'])
    if 'model' in tool:
        tool['model'] = sanitize_text(tool['model'])
    if 'SKU' in tool:
        tool['SKU'] = sanitize_text(tool['SKU'])
    # Si tus objetos incluyen otros campos de tipo string que puedan causar problemas,
    # puedes aplicar la función sanitize_text a esos campos también.
    
# ---------------------------
# Usuarios y roles: admin y usuario normal
# ---------------------------
usuarios = {
    'administrador': {'password': 'adminpass', 'role': 'admin'},
    'usuario': {'password': 'userpass', 'role': 'user'}
}

# ---------------------------
# Solicitudes de compra (en memoria)
# ---------------------------
purchase_requests = []

# ---------------------------
# Solicitudes de baja (removal requests) en memoria
# ---------------------------
removal_requests = []

# ---------------------------
# RUTAS DE AUTENTICACIÓN
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = usuarios.get(username)
        if user_data and user_data['password'] == password:
            session['user'] = username
            session['role'] = user_data['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------------------
# DASHBOARD (adaptado según el rol)
# ---------------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    query = request.args.get('query', '')
    if query:
        filtered_tools = [tool for tool in tools if query.lower() in tool['name'].lower()]
    else:
        filtered_tools = tools

    pr_count = len(purchase_requests) if session.get('role') == 'admin' else None
    removal_count = len(removal_requests) if session.get('role') == 'admin' else None

    return render_template('dashboard.html', tools=filtered_tools, query=query, pr_count=pr_count, removal_count=removal_count)

# ---------------------------
# RUTA PARA ENVIAR SOLICITUD DE COMPRA
# ---------------------------
@app.route('/send_request', methods=['GET', 'POST'])
def send_request():
    if 'user' not in session or session.get('role') != 'user':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    
    tool_id = request.args.get('tool_id')
    tool = None
    if tool_id:
        try:
            tool = next((t for t in tools if t['id'] == int(tool_id)), None)
        except:
            tool = None
    if request.method == 'POST':
        name = request.form.get('name')
        brand = request.form.get('brand')
        model = request.form.get('model')
        quantity = int(request.form.get('quantity', 1))
        justification = request.form.get('justification')
        request_id = len(purchase_requests) + 1
        purchase_requests.append({
            'id': request_id,
            'requested_by': session['user'],
            'name': name,
            'brand': brand,
            'model': model,
            'quantity': quantity,
            'justification': justification,
            'status': 'pendiente'
        })
        flash('Solicitud de compra enviada exitosamente.')
        return redirect(url_for('dashboard'))
    return render_template('send_request.html', tool=tool)

# ---------------------------
# RUTA PARA VER SOLICITUDES DE COMPRA (solo admin)
# ---------------------------
@app.route('/purchase_requests')
def view_purchase_requests():
    if 'user' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    return render_template('purchase_requests.html', requests=purchase_requests)

# ---------------------------
# RUTA PARA RECHAZAR SOLICITUD DE COMPRA (admin)
# ---------------------------
@app.route('/purchase_requests/reject/<int:request_id>')
def reject_request(request_id):
    if 'user' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    req = next((r for r in purchase_requests if r['id'] == request_id), None)
    if req:
        purchase_requests.remove(req)
        flash(f"Solicitud {request_id} rechazada.")
    else:
        flash("Solicitud no encontrada.")
    return redirect(url_for('view_purchase_requests'))

# ---------------------------
# RUTA PARA APROBAR SOLICITUD DE COMPRA (admin)
# ---------------------------
@app.route('/purchase_requests/approve/<int:request_id>', methods=['GET', 'POST'])
def approve_request(request_id):
    if 'user' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    req = next((r for r in purchase_requests if r['id'] == request_id), None)
    if not req:
        flash("Solicitud no encontrada.")
        return redirect(url_for('view_purchase_requests'))
    
    existing_tool = next((t for t in tools if t['name'] == req['name'] 
                                            and t['brand'] == req['brand'] 
                                            and t['model'] == req['model']), None)
    
    if request.method == 'POST':
        if existing_tool:
            for i in range(req['quantity']):
                new_instance_id = len(existing_tool['instances']) + 1
                existing_tool['instances'].append({'instance_id': new_instance_id, 'status': 'disponible'})
            flash(f"Solicitud {req['id']} aprobada. Se agregaron {req['quantity']} nueva(s) instancia(s) a la herramienta existente (SKU: {existing_tool['SKU']}).")
        else:
            sku = request.form.get('sku')
            if not sku:
                flash("Debes asignar un SKU.")
                return redirect(url_for('approve_request', request_id=request_id))
            new_tool_id = max([tool['id'] for tool in tools]) + 1 if tools else 1
            new_tool = {
                'id': new_tool_id,
                'name': req['name'],
                'brand': req['brand'],
                'model': req['model'],
                'SKU': sku,
                'instances': [{'instance_id': i+1, 'status': 'disponible'} for i in range(req['quantity'])]
            }
            tools.append(new_tool)
            flash(f"Solicitud {req['id']} aprobada y herramienta agregada con SKU {sku}.")
        purchase_requests.remove(req)
        return redirect(url_for('view_purchase_requests'))
    
    return render_template('approve_request.html', 
                           request_data=req, 
                           tool_exists=(existing_tool is not None),
                           existing_tool=existing_tool)

# ---------------------------
# RUTA PARA VER DETALLE DE UNA HERRAMIENTA
# ---------------------------
@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    tool = next((t for t in tools if t['id'] == tool_id), None)
    if not tool:
        flash('Herramienta no encontrada')
        return redirect(url_for('dashboard'))
    return render_template('tool_detail.html', tool=tool)

# ---------------------------
# RUTA PARA CAMBIAR ESTADO DE UNA INSTANCIA (toggle)
# ---------------------------
@app.route('/tool/<int:tool_id>/toggle_instance/<int:instance_id>', methods=['POST'])
def toggle_instance(tool_id, instance_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    tool = next((t for t in tools if t['id'] == tool_id), None)
    if not tool:
        flash('Herramienta no encontrada')
        return redirect(url_for('dashboard'))
    instance = next((inst for inst in tool['instances'] if inst['instance_id'] == instance_id), None)
    if not instance:
        flash('Instancia no encontrada')
        return redirect(url_for('tool_detail', tool_id=tool_id))
    if instance['status'] == 'disponible':
        instance['status'] = 'en uso'
        instance['user'] = session['user']
        flash(f"Instancia {instance_id} ahora está en uso por {session['user']}.")
    elif instance['status'] == 'en uso' and instance.get('user') == session['user']:
        instance['status'] = 'disponible'
        instance.pop('user', None)
        flash(f"Instancia {instance_id} ha sido marcada como disponible.")
    else:
        flash("No puedes modificar el estado de esta instancia.")
    return redirect(url_for('tool_detail', tool_id=tool_id))

# ---------------------------
# RUTA PARA REPORTAR DAÑO (solicitud de baja) de una instancia
# ---------------------------
@app.route('/tool/<int:tool_id>/report_removal/<int:instance_id>', methods=['GET', 'POST'])
def report_removal(tool_id, instance_id):
    if 'user' not in session or session.get('role') != 'user':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))

    tool = next((t for t in tools if t['id'] == tool_id), None)
    if not tool:
        flash("Herramienta no encontrada.")
        return redirect(url_for('dashboard'))

    instance = next((inst for inst in tool['instances'] if inst['instance_id'] == instance_id), None)
    if not instance:
        flash("Instancia no encontrada.")
        return redirect(url_for('tool_detail', tool_id=tool_id))

    if request.method == 'POST':
        justification = request.form.get('justification')
        if not justification:
            flash("Debes ingresar una justificación.")
            return redirect(url_for('report_removal', tool_id=tool_id, instance_id=instance_id))

        removal_id = len(removal_requests) + 1
        removal_requests.append({
            'id': removal_id,
            'tool_id': tool_id,
            'tool_name': tool['name'],
            'tool_brand': tool['brand'],
            'tool_model': tool['model'],
            'instance_id': instance_id,
            'justification': justification,
            'requested_by': session['user']
        })
        print("Nueva solicitud de baja:", removal_requests[-1])
        flash("Reporte de daño enviado exitosamente.")
        return redirect(url_for('tool_detail', tool_id=tool_id))

    return render_template('report_removal.html', tool=tool, instance=instance)

# ---------------------------
# RUTA PARA VER SOLICITUDES DE BAJA (removal requests) - solo admin
# ---------------------------
@app.route('/removal_requests')
def view_removal_requests():
    if 'user' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    return render_template('removal_requests.html', requests=removal_requests, tools=tools)

# ---------------------------
# RUTA PARA APROBAR SOLICITUD DE BAJA (admin)
# ---------------------------
@app.route('/removal_requests/approve/<int:removal_id>', methods=['POST'])
def approve_removal(removal_id):
    if 'user' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    
    req = next((r for r in removal_requests if r['id'] == removal_id), None)
    print("Contenido de la solicitud de baja:", req)  

    if not req:
        flash("Solicitud de baja no encontrada.")
        return redirect(url_for('view_removal_requests'))
    
    tool = next((t for t in tools if t['id'] == req.get('tool_id')), None)

    if tool:
        instance = next((inst for inst in tool['instances'] if inst['instance_id'] == req['instance_id']), None)
        if instance:
            tool['instances'].remove(instance)
        removal_requests.remove(req)
        flash(f"Solicitud de baja aprobada. Se eliminó la instancia de {req['tool_name']}.")
    else:
        flash("No se encontró la herramienta asociada a la solicitud. Verifica que los datos se están guardando correctamente.")

    return redirect(url_for('view_removal_requests'))

# ---------------------------
# RUTA PARA RECHAZAR SOLICITUD DE BAJA (admin)
# ---------------------------
@app.route('/removal_requests/reject/<int:removal_id>')
def reject_removal(removal_id):
    if 'user' not in session or session.get('role') != 'admin':
        flash("Acceso denegado.")
        return redirect(url_for('dashboard'))
    req = next((r for r in removal_requests if r['id'] == removal_id), None)
    if req:
        removal_requests.remove(req)
        flash("Solicitud de baja rechazada.")
    else:
        flash("Solicitud de baja no encontrada.")
    return redirect(url_for('view_removal_requests'))

if __name__ == '__main__':
    app.run(debug=True)