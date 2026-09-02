import pymongo
from datetime import datetime, timezone
from bson.objectid import ObjectId
from pymongo import MongoClient, TEXT

UTC = timezone.utc

# 1. Database Connection Initialization
try:
    client = MongoClient("mongodb://admin:password123@mongodb:27017/")
    db_name = 'GobiernoDB'
    
    # Check if the database already exists in the cluster
    existing_dbs = client.list_database_names()
    print(f"Existing databases: {existing_dbs}")
    
    if db_name not in existing_dbs:
        print(f"Database '{db_name}' does not exist. Initializing creation...")
    else:
        print(f"Database '{db_name}' already exists.")

    # Note: MongoDB creates the DB/Collection only when the first document is inserted.
    db = client[db_name]
    contracts = db['ContratosCLM']
    
except Exception as e:
    print(f"Connection failed: {e}")


# 2. Index Creation
# Essential for efficient searching
contracts.create_index([("nombre", TEXT), ("descripcion", TEXT)])
contracts.create_index("numero", unique=True) # Ensure 'numero' is unique

def insert_contracts_clm():
    """Inserts structured contract data following the CLM/SECOP II model."""
    documents = [
        {
            "numero": "020-2019",
            "nombre": "Suministro e instalación de equipos médicos para el Hospital San Juan",
            "entidad": "ESE Hospital Departamental San Juan",
            "descripcion": "Adquisición de ventiladores pulmonares y monitores de signos vitales para la unidad de cuidados intensivos.",
            "monto": 250000000.00,
            "fecha_inicio": datetime(2019, 5, 20, tzinfo=UTC),
            "fecha_fin": datetime(2020, 5, 19, tzinfo=UTC),
            "estado": "Liquidado",
            "tags": ["salud", "equipamiento", "hospital", "covid-19", "emergencia"]
        },
        {
            "numero": "164-2023",
            "nombre": "Mantenimiento preventivo y correctivo de la malla vial urbana",
            "entidad": "Alcaldía Municipal de Bogotá",
            "descripcion": "Intervención de huecos y bacheo en las troncales de Transmilenio y vías principales.",
            "monto": 1250000000.00,
            "fecha_inicio": datetime(2023, 1, 15, tzinfo=UTC),
            "fecha_fin": datetime(2024, 1, 14, tzinfo=UTC),
            "estado": "Activo",
            "tags": ["infraestructura", "vías", "bogotá", "mantenimiento"]
        },
        {
            "numero": "300-2024",
            "nombre": "Consultoría para el diseño del plan de ordenamiento territorial",
            "entidad": "Departamento Administrativo de Planeación",
            "descripcion": "Estudio técnico y social para la actualización de la normativa de uso de suelo.",
            "monto": 45000000.00,
            "fecha_inicio": datetime(2024, 2, 1, tzinfo=UTC),
            "fecha_fin": datetime(2024, 8, 1, tzinfo=UTC),
            "estado": "En ejecución",
            "tags": ["planeación", "consultoría", "territorio", "urbano"]
        }
    ]
    try:
        result = contracts.insert_many(documents, ordered=False)
        print(f"Data ingestion complete. Inserted IDs: {result.inserted_ids}")
    except pymongo.errors.BulkWriteError as e:
        print(f"Some documents already exist (Duplicate Key Error).")

def search_by_name(word):
    """Searches for contracts that contain a specific word in the 'nombre' field (case-insensitive)."""
    print(f"\n--- Search results for name containing: '{word}' ---")
    query = {"nombre": {"$regex": word, "$options": "i"}}
    results = list(contracts.find(query))
    if results:
        for doc in results:
            print(f"[{doc['numero']}] {doc['nombre']}")
            print(f"  Entidad: {doc['entidad']}")
            print(f"  Estado: {doc['estado']}")
            print(f"  Monto: ${doc['monto']:,.2f}")
            print("-" * 30)
    else:
        print("No contracts found with that name.")
    return results

def update_contract_status(numero, new_status):
    """Updates the 'estado' field of a contract searched by its 'numero'."""
    print(f"\n--- Updating status for contract: {numero} ---")
    query = {"numero": numero}
    update = {"$set": {"estado": new_status, "updated_at": datetime.now(UTC)}}
    
    result = contracts.update_one(query, update)
    if result.matched_count > 0:
        print(f"Success: Contract {numero} updated to '{new_status}'.")
        # Show updated document
        doc = contracts.find_one(query)
        print(f"Current State: {doc['estado']}")
    else:
        print(f"Error: No contract found with number {numero}.")

def list_all_contracts():
    """Lists all contracts in the collection."""
    print(f"\n--- Listando todos los contratos ---")
    results = list(contracts.find({}))
    if results:
        for doc in results:
            print(f"[{doc.get('numero', 'N/A')}] {doc.get('nombre', 'Sin nombre')}")
            print(f"  Entidad: {doc.get('entidad', 'N/A')}")
            print(f"  Estado: {doc.get('estado', 'N/A')}")
            print(f"  Monto: ${doc.get('monto', 0):,.2f}")
            print("-" * 30)
    else:
        print("La colección está vacía.")

def show_menu():
    print("\n" + "="*40)
    print("   GESTOR DE CONTRATOS MONGODB (CLM)")
    print("="*40)
    print("1. Insertar contratos de ejemplo")
    print("2. Buscar contrato por nombre")
    print("3. Actualizar estado por número")
    print("4. Listar todos los contratos")
    print("5. Salir")
    print("="*40)

# Execution Entry Point
if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Seleccione una opción (1-5): ")

        if choice == '1':
            insert_contracts_clm()
        elif choice == '2':
            word = input("Ingrese la palabra a buscar en el nombre: ")
            search_by_name(word)
        elif choice == '3':
            num = input("Ingrese el número del contrato: ")
            estado = input("Ingrese el nuevo estado: ")
            update_contract_status(num, estado)
        elif choice == '4':
            list_all_contracts()
        elif choice == '5':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")