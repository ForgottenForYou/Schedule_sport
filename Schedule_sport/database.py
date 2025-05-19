import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('sports_school.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Таблица тренеров
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS coaches (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            specialization TEXT
        )
        ''')

        # Таблица групп
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age_range TEXT,
            sport_type TEXT
        )
        ''')

        # Таблица расписания
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY,
            day_of_week INTEGER,
            start_time TEXT,
            end_time TEXT,
            group_id INTEGER,
            coach_id INTEGER,
            location TEXT,
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (coach_id) REFERENCES coaches (id)
        )
        ''')

        self.conn.commit()

    def add_coach(self, name, phone, specialization):
        self.cursor.execute('''
        INSERT INTO coaches (name, phone, specialization)
        VALUES (?, ?, ?)
        ''', (name, phone, specialization))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_coaches(self):
        self.cursor.execute('SELECT id, name FROM coaches')
        return self.cursor.fetchall()

    def get_coach_details(self, coach_id):
        self.cursor.execute('SELECT name, phone, specialization FROM coaches WHERE id = ?', (coach_id,))
        return self.cursor.fetchone()

    def add_group(self, name, age_range, sport_type):
        self.cursor.execute('''
        INSERT INTO groups (name, age_range, sport_type)
        VALUES (?, ?, ?)
        ''', (name, age_range, sport_type))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_groups(self):
        self.cursor.execute('SELECT id, name FROM groups')
        return self.cursor.fetchall()

    def get_group_details(self, group_id):
        self.cursor.execute('SELECT name, age_range, sport_type FROM groups WHERE id = ?', (group_id,))
        return self.cursor.fetchone()

    def add_schedule(self, day_of_week, start_time, end_time, group_id, coach_id, location):
        self.cursor.execute('''
        INSERT INTO schedule (day_of_week, start_time, end_time, group_id, coach_id, location)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (day_of_week, start_time, end_time, group_id, coach_id, location))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_schedule_for_day(self, day_of_week):
        self.cursor.execute('''
        SELECT s.id, s.start_time, s.end_time, g.name, c.name, s.location
        FROM schedule s
        JOIN groups g ON s.group_id = g.id
        JOIN coaches c ON s.coach_id = c.id
        WHERE s.day_of_week = ?
        ORDER BY s.start_time
        ''', (day_of_week,))
        return self.cursor.fetchall()

    def get_schedule_for_day_filtered(self, day_of_week, group_id=None, coach_id=None):
        """Получить расписание на день с фильтрацией по группе и/или тренеру"""
        query = '''
        SELECT s.id, s.start_time, s.end_time, g.name, c.name, s.location
        FROM schedule s
        JOIN groups g ON s.group_id = g.id
        JOIN coaches c ON s.coach_id = c.id
        WHERE s.day_of_week = ?
        '''
        params = [day_of_week]

        if group_id is not None:
            query += ' AND s.group_id = ?'
            params.append(group_id)

        if coach_id is not None:
            query += ' AND s.coach_id = ?'
            params.append(coach_id)

        query += ' ORDER BY s.start_time'

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_all_schedule(self):
        self.cursor.execute('''
        SELECT s.id, s.day_of_week, s.start_time, s.end_time, g.name, c.name, s.location
        FROM schedule s
        JOIN groups g ON s.group_id = g.id
        JOIN coaches c ON s.coach_id = c.id
        ORDER BY s.day_of_week, s.start_time
        ''')
        return self.cursor.fetchall()

    def get_all_schedule_filtered(self, group_id=None, coach_id=None):
        """Получить все расписание с фильтрацией по группе и/или тренеру"""
        query = '''
        SELECT s.id, s.day_of_week, s.start_time, s.end_time, g.name, c.name, s.location
        FROM schedule s
        JOIN groups g ON s.group_id = g.id
        JOIN coaches c ON s.coach_id = c.id
        '''
        params = []

        conditions = []
        if group_id is not None:
            conditions.append('s.group_id = ?')
            params.append(group_id)

        if coach_id is not None:
            conditions.append('s.coach_id = ?')
            params.append(coach_id)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        query += ' ORDER BY s.day_of_week, s.start_time'

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def delete_schedule_item(self, item_id):
        self.cursor.execute('DELETE FROM schedule WHERE id = ?', (item_id,))
        self.conn.commit()

    def get_schedule_item(self, item_id):
        self.cursor.execute('''
        SELECT s.day_of_week, s.start_time, s.end_time, s.group_id, s.coach_id, s.location
        FROM schedule s
        WHERE s.id = ?
        ''', (item_id,))
        return self.cursor.fetchone()

    def update_schedule_item(self, item_id, day_of_week, start_time, end_time, group_id, coach_id, location):
        self.cursor.execute('''
        UPDATE schedule
        SET day_of_week = ?, start_time = ?, end_time = ?, group_id = ?, coach_id = ?, location = ?
        WHERE id = ?
        ''', (day_of_week, start_time, end_time, group_id, coach_id, location, item_id))
        self.conn.commit()

    def close(self):
        self.conn.close()