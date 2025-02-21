import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS log_channels (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER
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
