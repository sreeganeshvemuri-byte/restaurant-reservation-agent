"""SQLite Database Schema and Initialization for Table Turner."""
import sqlite3
from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Tuple
import json
from contextlib import contextmanager

class TableTurnerDB:
    """Scalable SQLite database for Table Turner reservation system."""
    
    def __init__(self, db_path: str = "table_turner.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Get database connection with automatic cleanup."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database tables with indexes."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    phone_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_reservations INTEGER DEFAULT 0,
                    last_reservation_date TEXT
                )
            """)
            
            # Create index on name for searching
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_name ON users(name)
            """)
            
            # Restaurants table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS restaurants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    cuisine TEXT NOT NULL,
                    location TEXT NOT NULL,
                    city TEXT NOT NULL,
                    address TEXT,
                    phone TEXT,
                    rating REAL DEFAULT 4.0,
                    price_range TEXT,
                    description TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for efficient searching
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_restaurants_cuisine ON restaurants(cuisine)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_restaurants_location ON restaurants(location)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_restaurants_name ON restaurants(name)
            """)
            
            # Tables table (physical tables in each restaurant)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    restaurant_id INTEGER NOT NULL,
                    table_number INTEGER NOT NULL,
                    capacity INTEGER NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
                    UNIQUE(restaurant_id, table_number)
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tables_restaurant ON tables(restaurant_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tables_capacity ON tables(capacity)
            """)
            
            # Time slots table (available time slots)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS time_slots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time_slot TEXT NOT NULL UNIQUE,
                    slot_order INTEGER NOT NULL
                )
            """)
            
            # Reservations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reservation_id TEXT UNIQUE NOT NULL,
                    restaurant_id INTEGER NOT NULL,
                    table_id INTEGER NOT NULL,
                    phone_number TEXT NOT NULL,
                    customer_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time_slot TEXT NOT NULL,
                    party_size INTEGER NOT NULL,
                    status TEXT DEFAULT 'confirmed',
                    special_requests TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
                    FOREIGN KEY (table_id) REFERENCES tables(id),
                    FOREIGN KEY (phone_number) REFERENCES users(phone_number)
                )
            """)
            
            # Create composite indexes for efficient querying
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reservations_date_time 
                ON reservations(date, time_slot)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reservations_restaurant_date 
                ON reservations(restaurant_id, date)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reservations_phone 
                ON reservations(phone_number, created_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reservations_status 
                ON reservations(status)
            """)
            
            # Reservation counter for unique IDs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservation_counter (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    next_id INTEGER DEFAULT 1000
                )
            """)
            
            cursor.execute("""
                INSERT OR IGNORE INTO reservation_counter (id, next_id) VALUES (1, 1000)
            """)
            
            conn.commit()
    
    def seed_data(self):
        """Populate initial data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if already seeded
            cursor.execute("SELECT COUNT(*) FROM restaurants")
            if cursor.fetchone()[0] > 0:
                return  # Already seeded
            
            # Insert restaurants
            restaurants_data = [
                (1, "Spice Garden", "Indian", "Koramangala", "Bangalore", "123 Main St", "080-1234567", 4.5, "$$", "Authentic Indian cuisine"),
                (2, "Curry House", "Indian", "Indiranagar", "Bangalore", "45 Church St", "080-2345678", 4.3, "$$", "South Indian specialties"),
                (3, "Maharaja Palace", "Indian", "MG Road", "Bangalore", "78 MG Road", "080-3456789", 4.7, "$$$", "Royal dining experience"),
                (4, "Bella Italia", "Italian", "Koramangala", "Bangalore", "90 Pizza Lane", "080-4567890", 4.6, "$$$", "Authentic Italian"),
                (5, "Luigi's Kitchen", "Italian", "Brigade Road", "Bangalore", "12 Pasta St", "080-5678901", 4.2, "$$", "Homemade pasta"),
                (6, "Dragon Wok", "Chinese", "Koramangala", "Bangalore", "34 Wok Ave", "080-6789012", 4.4, "$$", "Szechuan & dim sum"),
                (7, "Golden Chopsticks", "Chinese", "Commercial Street", "Bangalore", "56 Noodle Rd", "080-7890123", 4.1, "$", "Quick Chinese"),
                (8, "The Continental", "Continental", "Indiranagar", "Bangalore", "89 Fine Dine", "080-8901234", 4.6, "$$$", "Steaks & grills"),
                (9, "Taco Fiesta", "Mexican", "Koramangala", "Bangalore", "23 Taco St", "080-9012345", 4.3, "$$", "Mexican favorites"),
                (10, "Sakura Sushi", "Japanese", "UB City", "Bangalore", "67 Sushi Lane", "080-0123456", 4.7, "$$$", "Fresh sushi & sashimi"),
            ]
            
            cursor.executemany("""
                INSERT INTO restaurants (id, name, cuisine, location, city, address, phone, rating, price_range, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, restaurants_data)
            
            # Insert tables for each restaurant
            # Each restaurant gets 3 tables of each size (2, 4, 6)
            tables_data = []
            table_id = 1
            for restaurant_id in range(1, 11):
                table_num = 1
                # 3 tables of size 2
                for _ in range(3):
                    tables_data.append((table_id, restaurant_id, table_num, 2))
                    table_id += 1
                    table_num += 1
                # 3 tables of size 4
                for _ in range(3):
                    tables_data.append((table_id, restaurant_id, table_num, 4))
                    table_id += 1
                    table_num += 1
                # 3 tables of size 6
                for _ in range(3):
                    tables_data.append((table_id, restaurant_id, table_num, 6))
                    table_id += 1
                    table_num += 1
            
            cursor.executemany("""
                INSERT INTO tables (id, restaurant_id, table_number, capacity)
                VALUES (?, ?, ?, ?)
            """, tables_data)
            
            # Insert time slots (30-minute intervals from 11:00 to 23:00)
            time_slots_data = []
            start_time = time(11, 0)
            current = datetime.combine(datetime.today(), start_time)
            end = datetime.combine(datetime.today(), time(23, 0))
            slot_order = 0
            
            while current <= end:
                time_slots_data.append((current.strftime("%H:%M"), slot_order))
                current += timedelta(minutes=30)
                slot_order += 1
            
            cursor.executemany("""
                INSERT INTO time_slots (time_slot, slot_order)
                VALUES (?, ?)
            """, time_slots_data)
            
            conn.commit()
    
    # User operations
    def check_user_exists(self, phone_number: str) -> bool:
        """Check if user exists."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM users WHERE phone_number = ?
            """, (phone_number,))
            return cursor.fetchone()[0] > 0
    
    def get_user(self, phone_number: str) -> Optional[Dict]:
        """Get user details."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE phone_number = ?
            """, (phone_number,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create_user(self, phone_number: str, name: str, email: str = None) -> Dict:
        """Create new user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (phone_number, name, email)
                VALUES (?, ?, ?)
            """, (phone_number, name, email))
            
            return {
                "phone_number": phone_number,
                "name": name,
                "email": email,
                "created_at": datetime.now().isoformat()
            }
    
    def get_user_reservations(self, phone_number: str, limit: int = 5) -> List[Dict]:
        """Get recent reservations for a user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, rest.name as restaurant_name, rest.location
                FROM reservations r
                JOIN restaurants rest ON r.restaurant_id = rest.id
                WHERE r.phone_number = ? AND r.status = 'confirmed'
                ORDER BY r.created_at DESC
                LIMIT ?
            """, (phone_number, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    # Restaurant operations
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Dict]:
        """Get restaurant by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM restaurants WHERE id = ? AND is_active = 1
            """, (restaurant_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict]:
        """Get restaurant by name (partial match)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM restaurants 
                WHERE name LIKE ? AND is_active = 1
                ORDER BY rating DESC
                LIMIT 1
            """, (f"%{name}%",))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def search_restaurants(self, cuisine: str = None, location: str = None) -> List[Dict]:
        """Search restaurants with filters."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM restaurants WHERE is_active = 1"
            params = []
            
            if cuisine:
                query += " AND cuisine LIKE ?"
                params.append(f"%{cuisine}%")
            
            if location:
                query += " AND location LIKE ?"
                params.append(f"%{location}%")
            
            query += " ORDER BY rating DESC"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # Time slot and availability operations
    def get_available_slots(self, restaurant_id: int, date: str, party_size: int) -> List[Dict]:
        """Get available time slots for a restaurant on a specific date.
        
        This is optimized with SQL joins and indexes for scalability.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Find all tables that can accommodate the party size
            cursor.execute("""
                SELECT id, table_number, capacity
                FROM tables
                WHERE restaurant_id = ? AND capacity >= ? AND is_active = 1
                ORDER BY capacity ASC
            """, (restaurant_id, party_size))
            
            suitable_tables = [dict(row) for row in cursor.fetchall()]
            
            if not suitable_tables:
                return []
            
            # Get all time slots
            cursor.execute("""
                SELECT time_slot, slot_order
                FROM time_slots
                ORDER BY slot_order
            """)
            all_time_slots = [dict(row) for row in cursor.fetchall()]
            
            # For each time slot, check if any suitable table is available
            available_slots = []
            
            for time_slot_data in all_time_slots:
                time_slot = time_slot_data['time_slot']
                
                # Check which tables are booked at this time
                cursor.execute("""
                    SELECT table_id
                    FROM reservations
                    WHERE restaurant_id = ? 
                    AND date = ? 
                    AND time_slot = ?
                    AND status = 'confirmed'
                """, (restaurant_id, date, time_slot))
                
                booked_table_ids = {row[0] for row in cursor.fetchall()}
                
                # Find first available table
                for table in suitable_tables:
                    if table['id'] not in booked_table_ids:
                        available_slots.append({
                            "time": time_slot,
                            "table_id": table['id'],
                            "table_number": table['table_number'],
                            "table_capacity": table['capacity'],
                            "available": True
                        })
                        break  # Found an available table for this slot
            
            return available_slots
    
    def find_nearest_available_slot(self, restaurant_id: int, date: str, 
                                    requested_time: str, party_size: int) -> Optional[Dict]:
        """Find nearest available slot after requested time."""
        available_slots = self.get_available_slots(restaurant_id, date, party_size)
        
        # Filter slots >= requested time
        requested_time_obj = datetime.strptime(requested_time, "%H:%M").time()
        future_slots = [
            slot for slot in available_slots
            if datetime.strptime(slot["time"], "%H:%M").time() >= requested_time_obj
        ]
        
        return future_slots[0] if future_slots else None
    
    def validate_booking_advance(self, booking_date: str) -> Tuple[bool, str]:
        """Validate booking is within 3 days from today."""
        current_date = datetime.now().date()
        try:
            target_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
            
            if target_date < current_date:
                return False, "Cannot book for past dates"
            
            days_diff = (target_date - current_date).days
            if days_diff > 3:
                return False, f"Bookings can only be made up to 3 days in advance. You're trying to book {days_diff} days ahead."
            
            return True, "Valid date"
        except ValueError:
            return False, "Invalid date format. Please use YYYY-MM-DD"
    
    def create_reservation(self, restaurant_id: int, table_id: int, phone_number: str,
                          customer_name: str, date: str, time_slot: str, 
                          party_size: int) -> Tuple[Optional[Dict], str]:
        """Create a new reservation with transaction safety."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Validate date
                is_valid, message = self.validate_booking_advance(date)
                if not is_valid:
                    return None, message
                
                # Check if table is still available (race condition protection)
                cursor.execute("""
                    SELECT COUNT(*) FROM reservations
                    WHERE table_id = ? AND date = ? AND time_slot = ? AND status = 'confirmed'
                """, (table_id, date, time_slot))
                
                if cursor.fetchone()[0] > 0:
                    return None, "This table has just been booked. Please choose another slot."
                
                # Generate unique reservation ID
                cursor.execute("""
                    UPDATE reservation_counter SET next_id = next_id + 1 WHERE id = 1
                    RETURNING next_id - 1
                """)
                reservation_number = cursor.fetchone()[0]
                reservation_id = f"TT{reservation_number}"
                
                # Create reservation
                cursor.execute("""
                    INSERT INTO reservations 
                    (reservation_id, restaurant_id, table_id, phone_number, customer_name, 
                     date, time_slot, party_size, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'confirmed')
                """, (reservation_id, restaurant_id, table_id, phone_number, customer_name,
                      date, time_slot, party_size))
                
                # Update user's reservation count
                cursor.execute("""
                    UPDATE users 
                    SET total_reservations = total_reservations + 1,
                        last_reservation_date = ?
                    WHERE phone_number = ?
                """, (date, phone_number))
                
                # Get the created reservation with restaurant details
                cursor.execute("""
                    SELECT r.*, rest.name as restaurant_name, rest.location,
                           t.table_number, t.capacity as table_capacity
                    FROM reservations r
                    JOIN restaurants rest ON r.restaurant_id = rest.id
                    JOIN tables t ON r.table_id = t.id
                    WHERE r.reservation_id = ?
                """, (reservation_id,))
                
                reservation = dict(cursor.fetchone())
                conn.commit()
                
                return reservation, "Reservation created successfully"
                
            except sqlite3.IntegrityError as e:
                return None, f"Database error: {str(e)}"
            except Exception as e:
                return None, f"Error creating reservation: {str(e)}"
    
    def get_reservation_by_id(self, reservation_id: str) -> Optional[Dict]:
        """Get reservation details by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, rest.name as restaurant_name, rest.location,
                       rest.address, rest.phone as restaurant_phone,
                       t.table_number, t.capacity as table_capacity
                FROM reservations r
                JOIN restaurants rest ON r.restaurant_id = rest.id
                JOIN tables t ON r.table_id = t.id
                WHERE r.reservation_id = ?
            """, (reservation_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def cancel_reservation(self, reservation_id: str) -> Tuple[bool, str]:
        """Cancel a reservation."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reservations
                SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP
                WHERE reservation_id = ? AND status = 'confirmed'
            """, (reservation_id,))
            
            if cursor.rowcount > 0:
                return True, "Reservation cancelled successfully"
            return False, "Reservation not found or already cancelled"
    
    # Helper functions
    def get_current_datetime(self) -> datetime:
        """Get current datetime."""
        return datetime.now()
    
    def parse_relative_date(self, user_input: str, current_date: datetime) -> Optional[str]:
        """Parse relative dates like 'today', 'tomorrow', 'next Saturday'."""
        user_input_lower = user_input.lower()
        
        if "today" in user_input_lower:
            return current_date.strftime("%Y-%m-%d")
        elif "tomorrow" in user_input_lower:
            return (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "day after tomorrow" in user_input_lower:
            return (current_date + timedelta(days=2)).strftime("%Y-%m-%d")
        elif "next" in user_input_lower:
            days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            for i, day in enumerate(days_of_week):
                if day in user_input_lower:
                    current_weekday = current_date.weekday()
                    days_ahead = (i - current_weekday) % 7
                    if days_ahead == 0:
                        days_ahead = 7
                    target_date = current_date + timedelta(days=days_ahead)
                    return target_date.strftime("%Y-%m-%d")
        
        return None
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM restaurants WHERE is_active = 1")
            total_restaurants = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM reservations WHERE status = 'confirmed'")
            active_reservations = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM reservations")
            total_reservations = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tables")
            total_tables = cursor.fetchone()[0]
            
            return {
                "restaurants": total_restaurants,
                "users": total_users,
                "active_reservations": active_reservations,
                "total_reservations": total_reservations,
                "total_tables": total_tables
            }
