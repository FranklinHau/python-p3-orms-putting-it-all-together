import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        # Constructor to initialize the dog instance with name and breed attributes
        self.id = id
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        # Class method to create a dogs table if it doesn't exist
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
            """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Class method to drop the dogs table if it exists
        CURSOR.execute("DROP TABLE IF EXISTS dogs")
        CONN.commit()
        
    def save(self):
        # Saves an instance of the Dog to the database
        if hasattr(self, "id"):
            sql = """
                UPDATE dogs SET name = ?, breed = ? WHERE id = ? 
                """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
        else:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
                """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            self.id = CURSOR.lastrowid
        CONN.commit()
    
    @classmethod
    def create (cls, name, breed):
        # Creates a new Dog instance and saves it to the database 
        dog = cls(name, breed)
        dog.save()
        return dog 
    @classmethod
    def new_from_db(cls, row):
        #Creates a new Dog instance from a database row
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog 
    @classmethod
    def get_all(cls):
        # Returns a list of all Dog instances from the database
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]
    @classmethod
    def find_by_name(cls, name):
        # Finds and returns a Dog instance by its name from the database
        sql = """
            SELECT * FROM dogs
            WHERE name = ? 
            LIMIT 1
            """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(row) if row else None
    @classmethod
    def find_by_id(cls, id):
        #Finds and returns a Dog instance by its ID from the database
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
            """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(row) if row else None 
    @classmethod
    def find_or_create_by(cls, name, breed):
        # Finds a Dogs instance by name and breed or creates a new one if it does not exist.
        dog = cls.find_by_name(name)
        if dog and dog.breed == breed:
            return dog
        else: 
            new_dog = cls(name, breed)
            new_dog.save()
            return new_dog
    def save(self):
        # Saves the instance to the database and updates its id. 
        if self.id:
            self.update()
        else:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
                """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
    def update(self):
        # Updates the instance's corresponding record in the database.
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE ID = ? 
            """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
    