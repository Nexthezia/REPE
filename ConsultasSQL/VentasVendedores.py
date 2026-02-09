from Funciones import Conexion

def obtener_ventas_vendedores():
    conexion = Conexion.conectar()
    if conexion is None:
        return []

    cursor = conexion.cursor()
    query = """
        SELECT id, cliente, telefono, numero_guia, ubicacion, encargado, total, fecha_entrega, entregado
        FROM entregas
        ORDER BY fecha_entrega DESC, id DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

def obtener_total_por_vendedor():
    conexion = Conexion.conectar()
    if conexion is None:
        return []

    cursor = conexion.cursor()
    query = """
        SELECT encargado, COUNT(*) as cantidad, SUM(total) as total_vendido
        FROM entregas
        GROUP BY encargado
        ORDER BY total_vendido DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

def agregar_a_factura(id_entrega, monto_adicional):
    conexion = Conexion.conectar()
    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()
        # Verificar si está entregado
        query_check = "SELECT entregado FROM entregas WHERE id = %s"
        cursor.execute(query_check, (id_entrega,))
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] == 1:
            print(f"No se puede agregar a factura. El pedido {id_entrega} ya fue entregado.")
            return False
        
        query = """
            UPDATE entregas 
            SET total = total + %s 
            WHERE id = %s
        """
        cursor.execute(query, (monto_adicional, id_entrega))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al actualizar factura: {e}")
        return False

def obtener_tiendas():
    conexion = Conexion.conectar()
    if conexion is None:
        return []

    cursor = conexion.cursor()
    query = """
        SELECT DISTINCT ubicacion
        FROM entregas
        ORDER BY ubicacion
    """
    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return [row[0] for row in resultados]

def obtener_entregas_por_tienda(tienda):
    conexion = Conexion.conectar()
    if conexion is None:
        return []

    cursor = conexion.cursor()
    query = """
        SELECT id, cliente, telefono, numero_guia, ubicacion, encargado, total, fecha_entrega, entregado
        FROM entregas
        WHERE ubicacion = %s
        ORDER BY fecha_entrega DESC, id DESC
    """
    cursor.execute(query, (tienda,))
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

def obtener_ventas_por_vendedor_tienda(tienda):
    conexion = Conexion.conectar()
    if conexion is None:
        return []

    cursor = conexion.cursor()
    query = """
        SELECT encargado, COUNT(*) as cantidad, SUM(total) as total_vendido
        FROM entregas
        WHERE ubicacion = %s
        GROUP BY encargado
        ORDER BY total_vendido DESC
    """
    cursor.execute(query, (tienda,))
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

def marcar_como_entregado(id_entrega):
    conexion = Conexion.conectar()
    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()
        query = """
            UPDATE entregas 
            SET entregado = 1 
            WHERE id = %s
        """
        cursor.execute(query, (id_entrega,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print(f"Error al marcar como entregado: {e}")
        return False

def obtener_entregas_por_fecha(fecha):
    conexion = Conexion.conectar()
    if conexion is None:
        return []

    cursor = conexion.cursor()
    query = """
        SELECT id, cliente, telefono, numero_guia, ubicacion, encargado, total, fecha_entrega, entregado
        FROM entregas
        WHERE DATE(fecha_entrega) = %s
        ORDER BY id DESC
    """
    cursor.execute(query, (fecha,))
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados