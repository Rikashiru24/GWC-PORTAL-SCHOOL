from ..api import api_bp
from ..db import get_db_connection
from flask import jsonify

# fetching from tbl_users
@api_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT p.first_name, p.last_name, u.email FROM tbl_users u
                       INNER JOIN tbl_profiles p
                       ON u.profile_id=p.id""")
        results = cursor.fetchall()

        if results:
            users_list = []
            for row in results:
                users_list.append({
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"]
                })
            return jsonify(users_list), 200
        return jsonify({"message": "Unable to fetch users"}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()