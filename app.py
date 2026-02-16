from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from ConsultasSQL.VentasVendedores import (
    obtener_ventas_vendedores, 
    obtener_total_por_vendedor, 
    agregar_a_factura,
    obtener_tiendas,
    obtener_entregas_por_tienda,
    obtener_ventas_por_vendedor_tienda,
    marcar_como_entregado,
    obtener_entregas_por_fecha,
    obtener_vendedores_unicos,
    obtener_ventas_por_vendedor,
    generar_excel_ventas
)
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    ventas = obtener_ventas_vendedores()
    totales_vendedores = obtener_total_por_vendedor()
    return render_template('index.html', ventas_vendedores=ventas, totales_vendedores=totales_vendedores)

@app.route('/vendedores')
def vendedores():
    ventas = obtener_ventas_vendedores()
    totales_vendedores = obtener_total_por_vendedor()
    return render_template('vendedores.html', ventas_vendedores=ventas, totales_vendedores=totales_vendedores)

@app.route('/tiendas')
def tiendas():
    lista_tiendas = obtener_tiendas()
    return render_template('tiendas.html', tiendas=lista_tiendas)

@app.route('/tienda/<tienda>')
def tienda_detalle(tienda):
    tienda_nombre = tienda.replace('_', ' ')
    entregas = obtener_entregas_por_tienda(tienda_nombre)
    vendedores = obtener_ventas_por_vendedor_tienda(tienda_nombre)
    return render_template('entregas_tienda.html', tienda=tienda_nombre, entregas=entregas, vendedores=vendedores)

@app.route('/agregar_a_factura/<int:id_entrega>', methods=['POST'])
def agregar_monto_factura(id_entrega):
    monto = request.form.get('monto')
    referrer = request.referrer
    
    if monto:
        try:
            monto = float(monto)
            agregar_a_factura(id_entrega, monto)
        except ValueError:
            pass

    if referrer:
        if '#' in referrer:
            referrer = referrer.split('#')[0]
        return redirect(f"{referrer}#{id_entrega}")
    return redirect(url_for('index', _anchor=str(id_entrega)))

@app.route('/marcar_entregado/<int:id_entrega>', methods=['POST'])
def marcar_entregado(id_entrega):
    resultado = marcar_como_entregado(id_entrega)
    
    # Si es una petición AJAX, devolver JSON
    if request.headers.get('Content-Type') == 'application/json':
        return jsonify({'success': resultado})
    
    # Si viene del formulario tradicional, redirigir al referrer
    referrer = request.referrer
    if referrer:
        if '#' in referrer:
            referrer = referrer.split('#')[0]
        return redirect(f"{referrer}#{id_entrega}")
    return redirect(url_for('index', _anchor=str(id_entrega)))

@app.route('/entregas_por_fecha', methods=['GET', 'POST'])
def entregas_por_fecha():
    entregas = []
    fecha_filtro = None
    
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        if fecha:
            fecha_filtro = fecha
            entregas = obtener_entregas_por_fecha(fecha)
    
    return render_template('entregas_fecha.html', entregas=entregas, fecha=fecha_filtro)

@app.route('/filtro_vendedor', methods=['GET', 'POST'])
def filtro_vendedor():
    vendedores = obtener_vendedores_unicos()
    ventas = []
    vendedor_filtro = None
    
    if request.method == 'POST':
        vendedor = request.form.get('vendedor')
        if vendedor:
            vendedor_filtro = vendedor
            ventas = obtener_ventas_por_vendedor(vendedor)
    
    return render_template('filtro_vendedor.html', vendedores=vendedores, ventas=ventas, vendedor_filtro=vendedor_filtro)

@app.route('/descargar_excel_todos')
def descargar_excel_todos():
    wb, nombre_archivo = generar_excel_ventas()
    
    # Guardar en memoria
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=nombre_archivo
    )

@app.route('/descargar_excel_vendedor/<vendedor>')
def descargar_excel_vendedor(vendedor):
    wb, nombre_archivo = generar_excel_ventas(vendedor)
    
    # Guardar en memoria
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=nombre_archivo
    )

@app.route('/descargar_excel_tienda/<tienda>')
def descargar_excel_tienda(tienda):
    tienda_nombre = tienda.replace('_', ' ')
    wb, nombre_archivo = generar_excel_ventas(tienda=tienda_nombre)
    
    # Guardar en memoria
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=nombre_archivo
    )

@app.route('/descargar_excel_multitienda')
def descargar_excel_multitienda():
    print("Solicitud recibida: Descargar Excel por tiendas")
    wb, nombre_archivo = generar_excel_ventas(separar_por_tiendas=True)
    
    # Guardar en memoria
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=nombre_archivo
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')