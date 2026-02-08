from flask import Flask, render_template, request, redirect, url_for
from Funciones.Datos import Host, User, Password, Database
from Funciones.Conexion import conectar
from ConsultasSQL.VentasVendedores import (
    obtener_ventas_vendedores, 
    obtener_total_por_vendedor, 
    agregar_a_factura,
    obtener_tiendas,
    obtener_entregas_por_tienda,
    obtener_ventas_por_vendedor_tienda
)

app = Flask(__name__)

@app.route('/')
def index():
    ventas = obtener_ventas_vendedores()
    totales_vendedores = obtener_total_por_vendedor()
    return render_template('index.html', ventas_vendedores=ventas, totales_vendedores=totales_vendedores)

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
        return redirect(referrer)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)