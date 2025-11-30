import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_name='chat_app.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.create_sample_data()
    
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create all necessary tables"""
        
        # Users table (existing)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                display_name TEXT,
                date_of_birth DATE,
                country TEXT,
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Messages table (existing - for direct messages)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                image_path TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id)
            )
        ''')
        
        # Add image_path column if it doesn't exist (for existing databases)
        try:
            self.cursor.execute('ALTER TABLE messages ADD COLUMN image_path TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Add edited/deleted columns if they don't exist
        try:
            self.cursor.execute('ALTER TABLE messages ADD COLUMN is_edited INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        try:
            self.cursor.execute('ALTER TABLE messages ADD COLUMN is_deleted INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        try:
            self.cursor.execute('ALTER TABLE messages ADD COLUMN forwarded_from_id INTEGER')
        except sqlite3.OperationalError:
            pass
        try:
            self.cursor.execute('ALTER TABLE messages ADD COLUMN edited_at TIMESTAMP')
        except sqlite3.OperationalError:
            pass
        
        # Groups table (NEW)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL,
                group_description TEXT,
                group_avatar TEXT DEFAULT '👥',
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        ''')
        
        # Group members table (NEW) - Junction table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT DEFAULT 'member' CHECK(role IN ('admin', 'member')),
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                invited_by INTEGER,
                FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (invited_by) REFERENCES users(user_id),
                UNIQUE(group_id, user_id)
            )
        ''')
        
        # Group invites table (NEW)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_invites (
                invite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                inviter_id INTEGER NOT NULL,
                invitee_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'declined')),
                invited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responded_at TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
                FOREIGN KEY (inviter_id) REFERENCES users(user_id),
                FOREIGN KEY (invitee_id) REFERENCES users(user_id),
                UNIQUE(group_id, invitee_id)
            )
        ''')
        
        # Group messages table (NEW)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS group_messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                sender_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                image_path TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(group_id) ON DELETE CASCADE,
                FOREIGN KEY (sender_id) REFERENCES users(user_id)
            )
        ''')
        
        # Add image_path column if it doesn't exist (for existing databases)
        try:
            self.cursor.execute('ALTER TABLE group_messages ADD COLUMN image_path TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Add edited/deleted columns if they don't exist
        try:
            self.cursor.execute('ALTER TABLE group_messages ADD COLUMN is_edited INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        try:
            self.cursor.execute('ALTER TABLE group_messages ADD COLUMN is_deleted INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        try:
            self.cursor.execute('ALTER TABLE group_messages ADD COLUMN forwarded_from_id INTEGER')
        except sqlite3.OperationalError:
            pass
        try:
            self.cursor.execute('ALTER TABLE group_messages ADD COLUMN edited_at TIMESTAMP')
        except sqlite3.OperationalError:
            pass
        
        # Friend requests table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS friend_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                requester_id INTEGER NOT NULL,
                recipient_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'declined')),
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responded_at TIMESTAMP,
                FOREIGN KEY (requester_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (recipient_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(requester_id, recipient_id)
            )
        ''')
        
        # Friendships table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS friendships (
                friendship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user1_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (user2_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(user1_id, user2_id)
            )
        ''')
        
        # Blocked users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocked_users (
                block_id INTEGER PRIMARY KEY AUTOINCREMENT,
                blocker_id INTEGER NOT NULL,
                blocked_id INTEGER NOT NULL,
                blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (blocker_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (blocked_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(blocker_id, blocked_id)
            )
        ''')
        
        # Streaks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER NOT NULL,
                user2_id INTEGER NOT NULL,
                streak_count INTEGER DEFAULT 0,
                last_active_date DATE,
                user1_last_message_date DATE,
                user2_last_message_date DATE,
                FOREIGN KEY (user1_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (user2_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(user1_id, user2_id)
            )
        ''')
        
        # Message reactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_reactions (
                reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                reaction_type TEXT NOT NULL,
                message_type TEXT NOT NULL CHECK(message_type IN ('direct', 'group')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(message_id, user_id, message_type)
            )
        ''')
        
        # Read receipts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS read_receipts (
                receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                message_type TEXT NOT NULL CHECK(message_type IN ('direct', 'group')),
                read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(message_id, user_id, message_type)
            )
        ''')
        
        self.conn.commit()
    
    def create_sample_data(self):
        """Create sample users if they don't exist"""
        try:
            # Check if users already exist
            self.cursor.execute("SELECT COUNT(*) FROM users")
            if self.cursor.fetchone()[0] == 0:
                # Create sample users
                users = [
                    ('alice', 'password123', 'Alice Johnson'),
                    ('bob', 'password123', 'Bob Smith'),
                    ('charlie', 'password123', 'Charlie Brown')
                ]
                
                for username, password, display_name in users:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    self.cursor.execute('''
                        INSERT INTO users (username, password_hash, display_name)
                        VALUES (?, ?, ?)
                    ''', (username, password_hash, display_name))
                
                self.conn.commit()
        except sqlite3.IntegrityError:
            pass
    
    # ============= EXISTING USER METHODS =============
    
    def login_user(self, username, password):
        """Verify user credentials"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = self.cursor.fetchone()
        return dict(user) if user else None
    
    def register_user(self, username, password, display_name=None, date_of_birth=None, country=None, bio=None):
        """Register a new user"""
        try:
            # Check if username already exists
            self.cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
            if self.cursor.fetchone():
                return False, "Username already exists"
            
            # Hash password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Insert new user
            self.cursor.execute('''
                INSERT INTO users (username, password_hash, display_name, date_of_birth, country, bio)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, password_hash, display_name, date_of_birth, country, bio))
            
            self.conn.commit()
            return True, "Registration successful"
        except Exception as e:
            return False, str(e)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = self.cursor.fetchone()
        return dict(user) if user else None
    
    def get_all_users(self):
        """Get all users"""
        self.cursor.execute('SELECT * FROM users ORDER BY username')
        return [dict(row) for row in self.cursor.fetchall()]
    
    def update_profile(self, user_id, display_name, date_of_birth, country, bio):
        """Update user profile"""
        try:
            self.cursor.execute('''
                UPDATE users 
                SET display_name = ?, date_of_birth = ?, country = ?, bio = ?
                WHERE user_id = ?
            ''', (display_name, date_of_birth, country, bio, user_id))
            self.conn.commit()
            return True
        except:
            return False
    
    def change_password(self, user_id, new_password):
        """Change user password"""
        try:
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            self.cursor.execute('''
                UPDATE users SET password_hash = ? WHERE user_id = ?
            ''', (password_hash, user_id))
            self.conn.commit()
            return True
        except:
            return False
    
    # ============= EXISTING MESSAGE METHODS =============
    
    def send_message(self, sender_id, receiver_id, message_text, image_path=None):
        """Send a direct message"""
        try:
            # Check if users are blocked
            if self.is_blocked(sender_id, receiver_id):
                return False, "Cannot send message: user is blocked", None, 0
            
            # Check if users are friends
            if not self.are_friends(sender_id, receiver_id):
                return False, "You must be friends to send messages", None, 0
            
            self.cursor.execute('''
                INSERT INTO messages (sender_id, receiver_id, message_text, image_path)
                VALUES (?, ?, ?, ?)
            ''', (sender_id, receiver_id, message_text, image_path))
            
            message_id = self.cursor.lastrowid
            
            # Update streak
            streak_count = self.update_streak(sender_id, receiver_id)
            
            self.conn.commit()
            return True, "Message sent", message_id, streak_count
        except Exception as e:
            return False, str(e), None, 0
    
    def get_conversation(self, user1_id, user2_id):
        """Get conversation between two users"""
        self.cursor.execute('''
            SELECT m.*, u.username as sender_name, u.display_name
            FROM messages m
            JOIN users u ON m.sender_id = u.user_id
            WHERE ((m.sender_id = ? AND m.receiver_id = ?)
               OR (m.sender_id = ? AND m.receiver_id = ?))
            ORDER BY m.sent_at ASC
        ''', (user1_id, user2_id, user2_id, user1_id))
        
        messages = []
        for row in self.cursor.fetchall():
            msg = dict(row)
            msg['sender_name'] = msg['display_name'] or msg['sender_name']
            msg['sent_at'] = datetime.strptime(msg['sent_at'], '%Y-%m-%d %H:%M:%S')
            # Set defaults for new fields
            if 'is_edited' not in msg or msg['is_edited'] is None:
                msg['is_edited'] = 0
            if 'is_deleted' not in msg or msg['is_deleted'] is None:
                msg['is_deleted'] = 0
            messages.append(msg)
        
        return messages
    
    # ============= FRIEND REQUEST METHODS =============
    
    def send_friend_request(self, requester_id, recipient_username):
        """Send a friend request"""
        try:
            # Get recipient user
            self.cursor.execute('SELECT user_id FROM users WHERE username = ?', (recipient_username,))
            recipient = self.cursor.fetchone()
            
            if not recipient:
                return False, "User not found"
            
            recipient_id = recipient['user_id']
            
            # Can't friend yourself
            if requester_id == recipient_id:
                return False, "Cannot send friend request to yourself"
            
            # Check if already friends
            self.cursor.execute('''
                SELECT * FROM friendships 
                WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
            ''', (requester_id, recipient_id, recipient_id, requester_id))
            
            if self.cursor.fetchone():
                return False, "Already friends"
            
            # Check if request already exists
            self.cursor.execute('''
                SELECT * FROM friend_requests 
                WHERE ((requester_id = ? AND recipient_id = ?) OR (requester_id = ? AND recipient_id = ?))
                AND status = 'pending'
            ''', (requester_id, recipient_id, recipient_id, requester_id))
            
            if self.cursor.fetchone():
                return False, "Friend request already sent"
            
            # Create friend request
            self.cursor.execute('''
                INSERT INTO friend_requests (requester_id, recipient_id)
                VALUES (?, ?)
            ''', (requester_id, recipient_id))
            
            self.conn.commit()
            return True, "Friend request sent"
        except Exception as e:
            return False, str(e)
    
    def get_pending_friend_requests(self, user_id):
        """Get all pending friend requests received by a user"""
        self.cursor.execute('''
            SELECT fr.*, u.username, u.display_name
            FROM friend_requests fr
            JOIN users u ON fr.requester_id = u.user_id
            WHERE fr.recipient_id = ? AND fr.status = 'pending'
            ORDER BY fr.requested_at DESC
        ''', (user_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def respond_to_friend_request(self, request_id, user_id, accept=True):
        """Accept or decline a friend request"""
        try:
            # Get request details
            self.cursor.execute('''
                SELECT * FROM friend_requests WHERE request_id = ? AND recipient_id = ?
            ''', (request_id, user_id))
            
            request = self.cursor.fetchone()
            if not request:
                return False, "Request not found"
            
            request = dict(request)
            status = 'accepted' if accept else 'declined'
            
            # Update request status
            self.cursor.execute('''
                UPDATE friend_requests 
                SET status = ?, responded_at = CURRENT_TIMESTAMP
                WHERE request_id = ?
            ''', (status, request_id))
            
            # If accepted, create friendship
            if accept:
                self.cursor.execute('''
                    INSERT INTO friendships (user1_id, user2_id)
                    VALUES (?, ?)
                ''', (request['requester_id'], user_id))
            
            self.conn.commit()
            return True, f"Friend request {status}"
        except Exception as e:
            return False, str(e)
    
    def are_friends(self, user1_id, user2_id):
        """Check if two users are friends"""
        self.cursor.execute('''
            SELECT * FROM friendships 
            WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
        ''', (user1_id, user2_id, user2_id, user1_id))
        
        return self.cursor.fetchone() is not None
    
    def get_friends(self, user_id):
        """Get all friends of a user"""
        self.cursor.execute('''
            SELECT u.user_id, u.username, u.display_name, u.date_of_birth, u.country, u.bio
            FROM friendships f
            JOIN users u ON (
                CASE 
                    WHEN f.user1_id = ? THEN f.user2_id = u.user_id
                    ELSE f.user1_id = u.user_id
                END
            )
            WHERE f.user1_id = ? OR f.user2_id = ?
            ORDER BY u.username
        ''', (user_id, user_id, user_id))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def remove_friendship(self, user1_id, user2_id):
        """Remove friendship"""
        try:
            self.cursor.execute('''
                DELETE FROM friendships 
                WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
            ''', (user1_id, user2_id, user2_id, user1_id))
            
            self.conn.commit()
            return True
        except:
            return False
    
    # ============= BLOCKING METHODS =============
    
    def block_user(self, blocker_id, blocked_username):
        """Block a user"""
        try:
            # Get blocked user
            self.cursor.execute('SELECT user_id FROM users WHERE username = ?', (blocked_username,))
            blocked = self.cursor.fetchone()
            
            if not blocked:
                return False, "User not found"
            
            blocked_id = blocked['user_id']
            
            # Can't block yourself
            if blocker_id == blocked_id:
                return False, "Cannot block yourself"
            
            # Check if already blocked
            self.cursor.execute('''
                SELECT * FROM blocked_users 
                WHERE blocker_id = ? AND blocked_id = ?
            ''', (blocker_id, blocked_id))
            
            if self.cursor.fetchone():
                return False, "User already blocked"
            
            # Delete friendship if exists
            self.cursor.execute('''
                DELETE FROM friendships 
                WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
            ''', (blocker_id, blocked_id, blocked_id, blocker_id))
            
            # Delete messages between users
            self.cursor.execute('''
                DELETE FROM messages 
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ''', (blocker_id, blocked_id, blocked_id, blocker_id))
            
            # Block user
            self.cursor.execute('''
                INSERT INTO blocked_users (blocker_id, blocked_id)
                VALUES (?, ?)
            ''', (blocker_id, blocked_id))
            
            self.conn.commit()
            return True, "User blocked"
        except Exception as e:
            return False, str(e)
    
    def unblock_user(self, blocker_id, blocked_id):
        """Unblock a user"""
        try:
            self.cursor.execute('''
                DELETE FROM blocked_users 
                WHERE blocker_id = ? AND blocked_id = ?
            ''', (blocker_id, blocked_id))
            
            self.conn.commit()
            return True
        except:
            return False
    
    def get_blocked_users(self, user_id):
        """Get all users blocked by this user"""
        self.cursor.execute('''
            SELECT bu.*, u.username, u.display_name
            FROM blocked_users bu
            JOIN users u ON bu.blocked_id = u.user_id
            WHERE bu.blocker_id = ?
            ORDER BY bu.blocked_at DESC
        ''', (user_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def is_blocked(self, user1_id, user2_id):
        """Check if user1 has blocked user2 or vice versa"""
        self.cursor.execute('''
            SELECT * FROM blocked_users 
            WHERE (blocker_id = ? AND blocked_id = ?) OR (blocker_id = ? AND blocked_id = ?)
        ''', (user1_id, user2_id, user2_id, user1_id))
        
        return self.cursor.fetchone() is not None
    
    # ============= STREAK METHODS =============
    
    def update_streak(self, sender_id, receiver_id):
        """Update or create streak between two users
        A streak day counts when both users send at least one message to each other.
        Streak increments each consecutive day where both users messaged.
        """
        try:
            from datetime import datetime, timedelta
            today = datetime.now().date()
            
            # Get existing streak
            self.cursor.execute('''
                SELECT * FROM streaks 
                WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
            ''', (sender_id, receiver_id, receiver_id, sender_id))
            
            streak = self.cursor.fetchone()
            
            # Determine which user is user1 and which is user2 (consistent ordering)
            if sender_id < receiver_id:
                user1_id, user2_id = sender_id, receiver_id
                is_sender_user1 = True
            else:
                user1_id, user2_id = receiver_id, sender_id
                is_sender_user1 = False
            
            if streak:
                streak = dict(streak)
                last_active = datetime.strptime(streak['last_active_date'], '%Y-%m-%d').date() if streak['last_active_date'] else None
                
                # Update the sender's last message date
                if is_sender_user1:
                    self.cursor.execute('''
                        UPDATE streaks 
                        SET user1_last_message_date = ?, last_active_date = ?
                        WHERE streak_id = ?
                    ''', (today, today, streak['streak_id']))
                else:
                    self.cursor.execute('''
                        UPDATE streaks 
                        SET user2_last_message_date = ?, last_active_date = ?
                        WHERE streak_id = ?
                    ''', (today, today, streak['streak_id']))
                
                # Get updated status
                self.cursor.execute('SELECT * FROM streaks WHERE streak_id = ?', (streak['streak_id'],))
                updated_streak = dict(self.cursor.fetchone())
                
                user1_msg_today = updated_streak['user1_last_message_date'] == str(today)
                user2_msg_today = updated_streak['user2_last_message_date'] == str(today)
                
                # Check if streak should reset (more than 1 day since last active)
                if last_active and (today - last_active).days > 1:
                    # Reset streak
                    self.cursor.execute('''
                        UPDATE streaks 
                        SET streak_count = 0
                        WHERE streak_id = ?
                    ''', (streak['streak_id'],))
                    new_streak_count = 0
                # Check if both users messaged today
                elif user1_msg_today and user2_msg_today:
                    # Both messaged today - check if we should increment
                    if last_active:
                        days_since = (today - last_active).days
                        if days_since == 0:
                            # Still today, don't increment
                            new_streak_count = updated_streak['streak_count']
                        elif days_since == 1:
                            # New day, increment streak
                            self.cursor.execute('''
                                UPDATE streaks 
                                SET streak_count = streak_count + 1
                                WHERE streak_id = ?
                            ''', (streak['streak_id'],))
                            new_streak_count = updated_streak['streak_count'] + 1
                        else:
                            # More than 1 day gap, reset
                            self.cursor.execute('''
                                UPDATE streaks 
                                SET streak_count = 0
                                WHERE streak_id = ?
                            ''', (streak['streak_id'],))
                            new_streak_count = 0
                    else:
                        # First time both messaged
                        new_streak_count = 0
                else:
                    # Not both users messaged today yet
                    new_streak_count = updated_streak['streak_count']
            else:
                # Create new streak
                user1_msg_date = today if is_sender_user1 else None
                user2_msg_date = today if not is_sender_user1 else None
                
                self.cursor.execute('''
                    INSERT INTO streaks (user1_id, user2_id, streak_count, last_active_date, 
                                       user1_last_message_date, user2_last_message_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user1_id, user2_id, 0, today, user1_msg_date, user2_msg_date))
                new_streak_count = 0
            
            self.conn.commit()
            return new_streak_count
        except Exception as e:
            print(f"Error updating streak: {e}")
            return 0
    
    def get_streak(self, user1_id, user2_id):
        """Get streak information between two users"""
        self.cursor.execute('''
            SELECT * FROM streaks 
            WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
        ''', (user1_id, user2_id, user2_id, user1_id))
        
        streak = self.cursor.fetchone()
        return dict(streak) if streak else None
    
    # ============= NEW GROUP METHODS =============
    
    def create_group(self, group_name, group_description, created_by, group_avatar='👥'):
        """Create a new group"""
        try:
            self.cursor.execute('''
                INSERT INTO groups (group_name, group_description, group_avatar, created_by)
                VALUES (?, ?, ?, ?)
            ''', (group_name, group_description, group_avatar, created_by))
            
            group_id = self.cursor.lastrowid
            
            # Automatically add creator as admin
            self.cursor.execute('''
                INSERT INTO group_members (group_id, user_id, role, invited_by)
                VALUES (?, ?, 'admin', ?)
            ''', (group_id, created_by, created_by))
            
            self.conn.commit()
            return group_id
        except Exception as e:
            print(f"Error creating group: {e}")
            return None
    
    def get_user_groups(self, user_id):
        """Get all groups a user is a member of"""
        self.cursor.execute('''
            SELECT g.*, gm.role, gm.joined_at,
                   u.username as creator_username, u.display_name as creator_name,
                   (SELECT COUNT(*) FROM group_members WHERE group_id = g.group_id) as member_count
            FROM groups g
            JOIN group_members gm ON g.group_id = gm.group_id
            JOIN users u ON g.created_by = u.user_id
            WHERE gm.user_id = ?
            ORDER BY g.created_at DESC
        ''', (user_id,))
        
        groups = []
        for row in self.cursor.fetchall():
            group = dict(row)
            groups.append(group)
        
        return groups
    
    def get_group_by_id(self, group_id):
        """Get group details by ID"""
        self.cursor.execute('''
            SELECT g.*, u.username as creator_username, u.display_name as creator_name,
                   (SELECT COUNT(*) FROM group_members WHERE group_id = g.group_id) as member_count
            FROM groups g
            JOIN users u ON g.created_by = u.user_id
            WHERE g.group_id = ?
        ''', (group_id,))
        
        group = self.cursor.fetchone()
        return dict(group) if group else None
    
    def get_group_members(self, group_id):
        """Get all members of a group"""
        self.cursor.execute('''
            SELECT u.user_id, u.username, u.display_name, gm.role, gm.joined_at
            FROM group_members gm
            JOIN users u ON gm.user_id = u.user_id
            WHERE gm.group_id = ?
            ORDER BY gm.role DESC, gm.joined_at ASC
        ''', (group_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def invite_to_group(self, group_id, inviter_id, invitee_id):
        """Send a group invitation"""
        try:
            # Check if user is already a member
            self.cursor.execute('''
                SELECT * FROM group_members 
                WHERE group_id = ? AND user_id = ?
            ''', (group_id, invitee_id))
            
            if self.cursor.fetchone():
                return False, "User is already a member"
            
            # Check if invitation already exists
            self.cursor.execute('''
                SELECT * FROM group_invites 
                WHERE group_id = ? AND invitee_id = ? AND status = 'pending'
            ''', (group_id, invitee_id))
            
            if self.cursor.fetchone():
                return False, "Invitation already sent"
            
            # Create invitation
            self.cursor.execute('''
                INSERT INTO group_invites (group_id, inviter_id, invitee_id)
                VALUES (?, ?, ?)
            ''', (group_id, inviter_id, invitee_id))
            
            self.conn.commit()
            return True, "Invitation sent"
        except Exception as e:
            print(f"Error inviting to group: {e}")
            return False, str(e)
    
    def get_pending_invites(self, user_id):
        """Get all pending group invitations for a user"""
        self.cursor.execute('''
            SELECT gi.*, g.group_name, g.group_description, g.group_avatar,
                   u.username as inviter_username, u.display_name as inviter_name
            FROM group_invites gi
            JOIN groups g ON gi.group_id = g.group_id
            JOIN users u ON gi.inviter_id = u.user_id
            WHERE gi.invitee_id = ? AND gi.status = 'pending'
            ORDER BY gi.invited_at DESC
        ''', (user_id,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def respond_to_invite(self, invite_id, user_id, accept=True):
        """Accept or decline a group invitation"""
        try:
            # Get invite details
            self.cursor.execute('''
                SELECT * FROM group_invites WHERE invite_id = ? AND invitee_id = ?
            ''', (invite_id, user_id))
            
            invite = self.cursor.fetchone()
            if not invite:
                return False, "Invitation not found"
            
            invite = dict(invite)
            status = 'accepted' if accept else 'declined'
            
            # Update invite status
            self.cursor.execute('''
                UPDATE group_invites 
                SET status = ?, responded_at = CURRENT_TIMESTAMP
                WHERE invite_id = ?
            ''', (status, invite_id))
            
            # If accepted, add user to group
            if accept:
                self.cursor.execute('''
                    INSERT INTO group_members (group_id, user_id, role, invited_by)
                    VALUES (?, ?, 'member', ?)
                ''', (invite['group_id'], user_id, invite['inviter_id']))
            
            self.conn.commit()
            return True, f"Invitation {status}"
        except Exception as e:
            print(f"Error responding to invite: {e}")
            return False, str(e)
    
    def send_group_message(self, group_id, sender_id, message_text, image_path=None):
        """Send a message to a group"""
        try:
            # Verify user is a member
            self.cursor.execute('''
                SELECT * FROM group_members 
                WHERE group_id = ? AND user_id = ?
            ''', (group_id, sender_id))
            
            if not self.cursor.fetchone():
                return False
            
            # Send message
            self.cursor.execute('''
                INSERT INTO group_messages (group_id, sender_id, message_text, image_path)
                VALUES (?, ?, ?, ?)
            ''', (group_id, sender_id, message_text, image_path))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error sending group message: {e}")
            return False
    
    def get_group_messages(self, group_id, user_id):
        """Get all messages from a group (if user is a member)"""
        # Verify user is a member
        self.cursor.execute('''
            SELECT * FROM group_members 
            WHERE group_id = ? AND user_id = ?
        ''', (group_id, user_id))
        
        if not self.cursor.fetchone():
            return []
        
        # Get messages
        self.cursor.execute('''
            SELECT gm.*, u.username as sender_name, u.display_name
            FROM group_messages gm
            JOIN users u ON gm.sender_id = u.user_id
            WHERE gm.group_id = ?
            ORDER BY gm.sent_at ASC
        ''', (group_id,))
        
        messages = []
        for row in self.cursor.fetchall():
            msg = dict(row)
            msg['sender_name'] = msg['display_name'] or msg['sender_name']
            msg['sent_at'] = datetime.strptime(msg['sent_at'], '%Y-%m-%d %H:%M:%S')
            # Set defaults for new fields
            if 'is_edited' not in msg or msg['is_edited'] is None:
                msg['is_edited'] = 0
            if 'is_deleted' not in msg or msg['is_deleted'] is None:
                msg['is_deleted'] = 0
            messages.append(msg)
        
        return messages
    
    def leave_group(self, group_id, user_id):
        """Leave a group"""
        try:
            self.cursor.execute('''
                DELETE FROM group_members 
                WHERE group_id = ? AND user_id = ?
            ''', (group_id, user_id))
            
            self.conn.commit()
            return True
        except:
            return False
    
    def remove_member(self, group_id, admin_id, member_id):
        """Remove a member from group (admin only)"""
        try:
            # Verify admin status
            self.cursor.execute('''
                SELECT role FROM group_members 
                WHERE group_id = ? AND user_id = ?
            ''', (group_id, admin_id))
            
            result = self.cursor.fetchone()
            if not result or result['role'] != 'admin':
                return False, "Only admins can remove members"
            
            # Remove member
            self.cursor.execute('''
                DELETE FROM group_members 
                WHERE group_id = ? AND user_id = ?
            ''', (group_id, member_id))
            
            self.conn.commit()
            return True, "Member removed"
        except Exception as e:
            return False, str(e)
    
    # ============= MESSAGE REACTIONS =============
    
    def add_reaction(self, message_id, user_id, reaction_type, message_type='direct'):
        """Add a reaction to a message"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO message_reactions (message_id, user_id, reaction_type, message_type)
                VALUES (?, ?, ?, ?)
            ''', (message_id, user_id, reaction_type, message_type))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding reaction: {e}")
            return False
    
    def remove_reaction(self, message_id, user_id, message_type='direct'):
        """Remove a reaction from a message"""
        try:
            self.cursor.execute('''
                DELETE FROM message_reactions 
                WHERE message_id = ? AND user_id = ? AND message_type = ?
            ''', (message_id, user_id, message_type))
            self.conn.commit()
            return True
        except Exception as e:
            return False
    
    def get_message_reactions(self, message_id, message_type='direct'):
        """Get all reactions for a message"""
        self.cursor.execute('''
            SELECT mr.*, u.username, u.display_name
            FROM message_reactions mr
            JOIN users u ON mr.user_id = u.user_id
            WHERE mr.message_id = ? AND mr.message_type = ?
        ''', (message_id, message_type))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ============= READ RECEIPTS =============
    
    def mark_as_read(self, message_id, user_id, message_type='direct'):
        """Mark a message as read"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO read_receipts (message_id, user_id, message_type, read_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (message_id, user_id, message_type))
            self.conn.commit()
            return True
        except Exception as e:
            return False
    
    def mark_conversation_as_read(self, user1_id, user2_id, reader_id):
        """Mark all messages in a conversation as read"""
        try:
            self.cursor.execute('''
                SELECT message_id FROM messages
                WHERE ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?))
                AND receiver_id = ? AND is_deleted = 0
            ''', (user1_id, user2_id, user2_id, user1_id, reader_id))
            
            messages = self.cursor.fetchall()
            for msg in messages:
                self.mark_as_read(msg['message_id'], reader_id, 'direct')
            
            return True
        except Exception as e:
            return False
    
    def is_message_read(self, message_id, user_id, message_type='direct'):
        """Check if a message is read by a user"""
        self.cursor.execute('''
            SELECT * FROM read_receipts 
            WHERE message_id = ? AND user_id = ? AND message_type = ?
        ''', (message_id, user_id, message_type))
        return self.cursor.fetchone() is not None
    
    # ============= MESSAGE EDITING/DELETING =============
    
    def edit_message(self, message_id, new_text, message_type='direct'):
        """Edit a message"""
        try:
            table = 'messages' if message_type == 'direct' else 'group_messages'
            self.cursor.execute(f'''
                UPDATE {table}
                SET message_text = ?, is_edited = 1, edited_at = CURRENT_TIMESTAMP
                WHERE message_id = ?
            ''', (new_text, message_id))
            self.conn.commit()
            return True
        except Exception as e:
            return False
    
    def delete_message(self, message_id, message_type='direct'):
        """Delete a message from database (hard delete)"""
        try:
            table = 'messages' if message_type == 'direct' else 'group_messages'
            
            # First verify message exists
            self.cursor.execute(f'SELECT message_id FROM {table} WHERE message_id = ?', (message_id,))
            if not self.cursor.fetchone():
                print(f"Message {message_id} not found")
                return False
            
            # Delete the message
            self.cursor.execute(f'DELETE FROM {table} WHERE message_id = ?', (message_id,))
            
            # Also delete associated reactions and read receipts
            self.cursor.execute('''
                DELETE FROM message_reactions 
                WHERE message_id = ? AND message_type = ?
            ''', (message_id, message_type))
            
            self.cursor.execute('''
                DELETE FROM read_receipts 
                WHERE message_id = ? AND message_type = ?
            ''', (message_id, message_type))
            
            self.conn.commit()
            
            # Verify deletion
            rows_affected = self.cursor.rowcount
            if rows_affected > 0:
                return True
            else:
                print(f"Warning: No rows deleted for message_id {message_id}")
                return False
        except Exception as e:
            print(f"Error deleting message: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_message_by_id(self, message_id, message_type='direct'):
        """Get a message by ID"""
        table = 'messages' if message_type == 'direct' else 'group_messages'
        self.cursor.execute(f'SELECT * FROM {table} WHERE message_id = ?', (message_id,))
        msg = self.cursor.fetchone()
        return dict(msg) if msg else None
    
    # ============= MESSAGE FORWARDING =============
    
    def forward_message(self, message_id, sender_id, receiver_id, message_type='direct', forward_type='direct'):
        """Forward a message to another chat"""
        try:
            # Get original message
            original = self.get_message_by_id(message_id, message_type)
            if not original:
                return False, "Message not found"
            
            # Create forwarded message
            forwarded_text = f"Forwarded: {original['message_text']}"
            if forward_type == 'direct':
                success, msg, new_msg_id, _ = self.send_message(sender_id, receiver_id, forwarded_text, original.get('image_path'))
                if success and new_msg_id:
                    # Update to mark as forwarded
                    self.cursor.execute('''
                        UPDATE messages SET forwarded_from_id = ?
                        WHERE message_id = ?
                    ''', (message_id, new_msg_id))
                    self.conn.commit()
                return success, msg
            else:
                # Forward to group
                success = self.send_group_message(receiver_id, sender_id, forwarded_text, original.get('image_path'))
                if success:
                    new_msg_id = self.cursor.lastrowid
                    self.cursor.execute('''
                        UPDATE group_messages SET forwarded_from_id = ?
                        WHERE message_id = ?
                    ''', (message_id, new_msg_id))
                    self.conn.commit()
                return success, "Message forwarded"
        except Exception as e:
            return False, str(e)
    
    # ============= MESSAGE SEARCH =============
    
    def search_messages(self, user_id, search_query, chat_with_id=None, group_id=None):
        """Search messages in conversations"""
        results = []
        
        if chat_with_id:
            # Search in direct messages
            self.cursor.execute('''
                SELECT m.*, u.username as sender_name, u.display_name
                FROM messages m
                JOIN users u ON m.sender_id = u.user_id
                WHERE ((m.sender_id = ? AND m.receiver_id = ?) OR (m.sender_id = ? AND m.receiver_id = ?))
                AND m.message_text LIKE ?
                ORDER BY m.sent_at DESC
            ''', (user_id, chat_with_id, chat_with_id, user_id, f'%{search_query}%'))
            
            for row in self.cursor.fetchall():
                msg = dict(row)
                msg['sender_name'] = msg['display_name'] or msg['sender_name']
                msg['sent_at'] = datetime.strptime(msg['sent_at'], '%Y-%m-%d %H:%M:%S')
                results.append(msg)
        
        elif group_id:
            # Search in group messages
            self.cursor.execute('''
                SELECT gm.*, u.username as sender_name, u.display_name
                FROM group_messages gm
                JOIN users u ON gm.sender_id = u.user_id
                WHERE gm.group_id = ? AND gm.message_text LIKE ?
                ORDER BY gm.sent_at DESC
            ''', (group_id, f'%{search_query}%'))
            
            for row in self.cursor.fetchall():
                msg = dict(row)
                msg['sender_name'] = msg['display_name'] or msg['sender_name']
                msg['sent_at'] = datetime.strptime(msg['sent_at'], '%Y-%m-%d %H:%M:%S')
                results.append(msg)
        
        return results
    
    # ============= CLEAR CHAT =============
    
    def clear_conversation(self, user1_id, user2_id):
        """Clear all messages in a conversation"""
        try:
            self.cursor.execute('''
                DELETE FROM messages
                WHERE ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?))
            ''', (user1_id, user2_id, user2_id, user1_id))
            self.conn.commit()
            return True
        except Exception as e:
            return False
    
    def clear_group_chat(self, group_id):
        """Clear all messages in a group chat"""
        try:
            self.cursor.execute('''
                DELETE FROM group_messages WHERE group_id = ?
            ''', (group_id,))
            self.conn.commit()
            return True
        except Exception as e:
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Test the database
if __name__ == "__main__":
    db = Database()
    print("Database created successfully!")
    
    # Test: Create a group
    group_id = db.create_group("Python Developers", "A group for Python enthusiasts", 1, "🐍")
    if group_id:
        print(f"Created group with ID: {group_id}")
        
        # Test: Invite user to group
        success, msg = db.invite_to_group(group_id, 1, 2)
        print(f"Invite status: {msg}")
        
        # Test: Get pending invites
        invites = db.get_pending_invites(2)
        print(f"User 2 has {len(invites)} pending invites")
    
    db.close()