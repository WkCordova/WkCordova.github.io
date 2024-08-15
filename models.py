import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data/cita_perfecta.db')

def init_db():
    print(f"Initializing database at {DB_PATH}")
    if not os.path.exists(DB_PATH):
        print("Database file does not exist. Creating new database.")
    else:
        print("Database file exists. Initializing tables if not present.")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS establishments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ruc TEXT NOT NULL,
                commercial_name TEXT NOT NULL,
                legal_name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT,
                contact_name TEXT,
                establishment_type TEXT NOT NULL CHECK (establishment_type IN ('Restaurante', 'Transporte', 'Hotel')),
                logo_image TEXT
            )
        ''')
        conn.commit()
    print("Database initialized successfully.")

    add_initial_data()

def add_initial_data():
    establishments = [
        ('1234567890', 'La Casa de la Pasta', 'La Casa de la Pasta S.A.', 'Av. Principal 123', '098-123-4567', 'Carlos Rossi', 'Restaurante', 'https://media-cdn.tripadvisor.com/media/photo-s/12/62/5c/92/vista-exterior-del-restaurante.jpg'),
        ('0987654321', 'Transporte Seguro', 'Transporte Seguro S.A.', 'Calle Secundaria 456', '099-876-5432', 'Ana Martinez', 'Transporte', 'https://pbs.twimg.com/profile_images/991672982794883072/AcADkpVv_400x400.jpg'),
        ('1122334455', 'Hotel Paradiso', 'Hotel Paradiso S.A.', 'Av. Las Flores 789', '097-112-3344', 'Laura Vega', 'Hotel', 'https://images.adsttc.com/media/images/5d30/0be2/284d/d1d0/8600/0038/newsletter/-_Featured_Image.jpg?1563429772'),
        ('2233445566', 'El Buen Sabor', 'El Buen Sabor S.A.', 'Calle de los Álamos 321', '096-223-3445', 'Miguel Gomez', 'Restaurante', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRW4g2Wr0VQijPDpbnQ-NmIpuw0lleR-Vfxmw&s'),
        ('3344556677', 'Viaje Express', 'Viaje Express S.A.', 'Av. Libertador 654', '095-334-4556', 'Pedro Ruiz', 'Transporte', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSd4lKAByhlVpNmnI11_JLmTCcCKoNBZOpYVg&s'),
        ('4455667788', 'Hotel El Sol', 'Hotel El Sol S.A.', 'Calle del Sol 987', '094-445-5667', 'Sofia Perez', 'Hotel', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShZv0QnjlJfVqG1oWvHtYbbqo_FcBLJeNPUw&s'),
        ('5566778899', 'Pizza World', 'Pizza World S.A.', 'Av. Mundo 321', '093-556-6778', 'Lucia Fernandez', 'Restaurante', 'https://calipizzaec.com/wp-content/uploads/2021/05/Inicio-Cali-Pizza-1-1024x577.jpg'),
        ('6677889900', 'Transporte Rápido', 'Transporte Rápido S.A.', 'Calle Rapida 432', '092-667-7889', 'Jorge Herrera', 'Transporte', 'https://www.comfenalcoantioquia.com.co/wcm/connect/9f6a0cf0-88ae-4a64-b3e8-39fb82a24383/1/transportes-rapido-ochoa-155.png?MOD=AJPERES'),
        ('7788990011', 'Hotel Luna', 'Hotel Luna S.A.', 'Av. Lunar 543', '091-778-8990', 'Mariana Torres', 'Hotel', 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0b/41/e6/59/pool--v12235321.jpg?w=700&h=-1&s=1'),
        ('8899001122', 'Sushi House', 'Sushi House S.A.', 'Calle Oriental 654', '090-889-0011', 'Akira Tanaka', 'Restaurante', 'https://static.vecteezy.com/system/resources/previews/004/909/727/original/logo-sushi-free-vector.jpg')
    ]

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM establishments')
        cursor.executemany('''
            INSERT INTO establishments (ruc, commercial_name, legal_name, address, phone, contact_name, establishment_type, logo_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', establishments)
        conn.commit()
    print("Initial data added successfully.")

class Establishment:
    def __init__(self, ruc, commercial_name, legal_name, address, phone, contact_name, establishment_type, logo_image):
        self.ruc = ruc
        self.commercial_name = commercial_name
        self.legal_name = legal_name
        self.address = address
        self.phone = phone
        self.contact_name = contact_name
        self.establishment_type = establishment_type
        self.logo_image = logo_image

    @staticmethod
    def get_all():
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM establishments")
            rows = cursor.fetchall()
            return [Establishment(*row[1:]) for row in rows]

    @staticmethod
    def add(establishment):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO establishments (ruc, commercial_name, legal_name, address, phone, contact_name, establishment_type, logo_image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (establishment.ruc, establishment.commercial_name, establishment.legal_name, establishment.address, establishment.phone, establishment.contact_name, establishment.establishment_type, establishment.logo_image))
            conn.commit()

    @staticmethod
    def update(establishment_data):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE establishments SET
                    ruc = ?, commercial_name = ?, legal_name = ?, address = ?, phone = ?, contact_name = ?, establishment_type = ?, logo_image = ?
                WHERE ruc = ?
            ''', (
                establishment_data['ruc'], establishment_data['commercial_name'], establishment_data['legal_name'], establishment_data['address'], establishment_data['phone'], establishment_data['contact_name'], establishment_data['establishment_type'], establishment_data['logo_image'], establishment_data['ruc']
            ))
            conn.commit()

    @staticmethod
    def delete_by_ruc(ruc):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM establishments WHERE ruc = ?', (ruc,))
            conn.commit()



