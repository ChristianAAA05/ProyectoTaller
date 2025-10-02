#!/usr/bin/env python3

import mysql.connector

def check_database():
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='abel_taller',
            password='Cr1sab3l;;',
            database='taller_mecanico'
        )

        cursor = conn.cursor()

        # Check if employees table exists and count records
        cursor.execute("SHOW TABLES LIKE 'gestion_empleado'")
        table_exists = cursor.fetchone()

        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM gestion_empleado")
            count = cursor.fetchone()[0]
            print(f"✅ Found {count} employees in the database")

            if count > 0:
                cursor.execute("SELECT nombre, puesto, telefono, correo_electronico FROM gestion_empleado")
                employees = cursor.fetchall()
                print("\n📋 Employee Details:")
                print("-" * 50)
                for emp in employees:
                    print(f"Name: {emp[0]}")
                    print(f"Position: {emp[1]}")
                    print(f"Phone: {emp[2]}")
                    print(f"Email: {emp[3]}")
                    print("-" * 50)
            else:
                print("❌ No employees found in database")
        else:
            print("❌ Table 'gestion_empleado' does not exist")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        if err.errno == 1049:  # Database doesn't exist
            print("❌ Database 'taller_mecanico' does not exist")
        elif err.errno == 1045:  # Access denied
            print("❌ Access denied - check username/password")
        elif err.errno == 2003:  # Can't connect to MySQL server
            print("❌ Cannot connect to MySQL server - check if MySQL is running")
        else:
            print(f"❌ MySQL Error: {err}")
    except ImportError:
        print("❌ MySQL connector not installed")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("🔍 Checking database connection and employees...")
    check_database()
