import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS log_channels (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER,
                    guild_id INTEGER,
                    reason TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def set_log_channel(guild_id, channel_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('REPLACE INTO log_channels (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel_id))
    conn.commit()
    conn.close()

def get_log_channel(guild_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT channel_id FROM log_channels WHERE guild_id = ?', (guild_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_warning(user_id, guild_id, reason):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('INSERT INTO warnings (user_id, guild_id, reason) VALUES (?, ?, ?)', (user_id, guild_id, reason))
    conn.commit()
    conn.close()

def get_warnings(user_id, guild_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT reason, timestamp FROM warnings WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
    results = c.fetchall()
    conn.close()
    return results
