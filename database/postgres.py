import psycopg2

class PostgreSQL:
  def __init__(self,p_database,p_user,p_password,p_host,p_port):
    self.connection = psycopg2.connect(
      database=p_database,
      user=p_user,
      password=p_password,
      host=p_host,
      port=p_port
    )
    self.cursor = self.connection.cursor()

  def insert_array(self,p_data,p_query):
    try:
      v_bulk_count,v_cant_registros,v_registros_insertados = 10,0,0
      C = []
      for data in p_data:
        C.append(data)
        v_cant_registros = v_cant_registros + 1

        if v_cant_registros%v_bulk_count == 0:
          #print(len(C),v_cant_registros%v_bulk_count,v_cant_registros)
          self.cursor.executemany(p_query, C)
          v_registros_insertados=v_registros_insertados + self.cursor.rowcount
          self.connection.commit()
          C = []

      # Cargando lo faltante
      self.cursor.executemany(p_query, C)
      v_registros_insertados=v_registros_insertados + self.cursor.rowcount
      self.connection.commit()

      print(f'Finalizacion la insercion [Registros Array] -> {len(p_data)} | [Registros Base de datos] -> {v_registros_insertados}')
    except Exception as e:
      print(C)
      raise Exception(f'PostgreSQL.insert_array: {e}')
  
  def execute_query (self,p_query):
    try:
      self.cursor.execute(p_query)
      self.connection.commit()
      print(f'Se ejecuto: {p_query}\ncorrectamente.')
    except Exception as e:
      raise Exception(f'PostgreSQL.execute_query: {e}')
    
  def execute_store_procedure (self,p_store_procedure,p_params):
    try:
      self.connection.autocommit = True
      self.cursor.execute(f'CALL {p_store_procedure}(%s)',p_params)
      self.connection.autocommit = False
      print(f'Se ejecuto: {p_store_procedure}\ncorrectamente.')
    except Exception as e:
      raise Exception(f'PostgreSQL.execute_store_procedure: {e}')