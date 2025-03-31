import csv
import os

def csv_to_sql_insert(csv_file, table_name, columns):
    """
    Genera sentencias INSERT INTO SQL a partir de un archivo CSV.
    
    Args:
        csv_file (str): Ruta al archivo CSV
        table_name (str): Nombre de la tabla SQL
        columns (list): Lista de columnas de la tabla
    
    Returns:
        str: Sentencias SQL INSERT generadas
    """
    if not os.path.exists(csv_file):
        return f"Error: El archivo {csv_file} no existe."
    
    inserts = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Opcionalmente saltar la primera fila si contiene encabezados
            has_header = input("¿El archivo CSV tiene encabezados? (s/n): ").lower() == 's'
            if has_header:
                next(reader)
            
            # Generar las sentencias INSERT
            for row in reader:
                # Formatear cada valor adecuadamente (números sin comillas, texto con comillas)
                formatted_values = []
                for i, value in enumerate(row):
                    # Si la columna tiene un nombre que contiene "ID" o termina con "_id", tratarla como número
                    if "ID_" in columns[i].upper() or columns[i].upper().endswith("_ID"):
                        formatted_values.append(value.strip())
                    else:
                        # Escapar comillas simples en el texto
                        value = value.replace("'", "''")
                        formatted_values.append(f"'{value}'")
                
                values_str = ', '.join(formatted_values)
                insert = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_str});"
                inserts.append(insert)
    
    except Exception as e:
        return f"Error al procesar el archivo CSV: {str(e)}"
    
    return '\n'.join(inserts)

def main():
    print("Generador de sentencias INSERT SQL desde CSV")
    print("-----------------------------------------")
    
    csv_file = input("Ingresa la ruta del archivo CSV: ")
    table_name = input("Ingresa el nombre de la tabla SQL: ")
    
    columns_input = input("Ingresa los nombres de las columnas separados por coma: ")
    columns = [col.strip() for col in columns_input.split(',')]
    
    print("\nGenerando sentencias INSERT...\n")
    
    result = csv_to_sql_insert(csv_file, table_name, columns)
    
    print(result)
    
    # Opcionalmente guardar a un archivo
    save_option = input("\n¿Deseas guardar las sentencias SQL a un archivo? (s/n): ").lower()
    if save_option == 's':
        output_file = input("Ingresa el nombre del archivo de salida: ")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(result)
        print(f"Las sentencias SQL se han guardado en {output_file}")

if __name__ == "__main__":
    main()