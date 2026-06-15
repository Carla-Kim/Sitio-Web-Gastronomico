from datetime import datetime

def formato_fecha(lista):
                    
    for r in lista:
        if isinstance(r, dict) and 'fecha' in r and r['fecha']:
            try:
                val = r['fecha']
                
                if isinstance(val, datetime):
                    dt = val
                    
                else:
                    fecha_str = str(val).replace('T', ' ').strip()
                    dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                
                r['fecha'] = f"{dt.strftime('%Y-%m-%d')} hora: {dt.strftime('%H:%M')}"
                
            except Exception as e:
                print(f"Error crítico en formato_fecha: {e}")
                