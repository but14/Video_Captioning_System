import psycopg2
from datetime import datetime

# Thiết lập kết nối
def get_connection():
    return psycopg2.connect(
        host='localhost',
        port="5432",      
        database= 'video_caption',
        user='postgres',
        password='long1407' 
    )

# Lưu feature path vào DB
def insert_feature_path(video_name, feature_path):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO video_features (video_name, feature_path, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (video_name) DO NOTHING
        """, (video_name, feature_path, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("DB Insert Error:", e)

def get_feature_path(video_name):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT feature_path FROM video_features WHERE video_name = %s", (video_name,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print("DB Select Error:", e)
        return None
