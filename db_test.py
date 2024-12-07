import psycopg2
import socket

try:
    connection = psycopg2.connect(
        dbname="mylms_database",
        user="mylms_database_user",
        password="mPa4s0pANFIKIqbUzUPYWGvwvsRePWfj",
        host="dpg-ct7f67q3esus73br84v0-a.oregon-postgres.render.com",
        port="5432"
    )
    print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")

# #########

try:
    ip = socket.gethostbyname("dpg-ct7f67q3esus73br84v0-a.oregon-postgres.render.com")
    print(f"Resolved to IP: {ip}")
except socket.gaierror as e:
    print(f"DNS resolution error: {e}")