from ..utils.decorators import token_required
from ..api import api_bp
from flask import jsonify
from ..db import get_db_connection

@api_bp.route("/student_panel", methods=["GET"])
@token_required
def student_panel(current_user):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT 
                    sub.descriptive_title as Subject, 
                    CONCAT(ins_prof.first_name, ' ', ins_prof.last_name) as Instructor
                FROM tbl_users user

                INNER JOIN tbl_profiles prof
                ON user.profile_id = prof.id

                INNER JOIN tbl_students stud
                ON prof.id = stud.profile_id

                INNER JOIN tbl_enrollments enr
                ON stud.id = enr.student_id

                INNER JOIN tbl_classes cls
                ON enr.class_id = cls.id

                INNER JOIN tbl_subjects sub
                ON cls.subject_id = sub.id

                INNER JOIN tbl_instructors ins
                ON cls.instructor_id = ins.id

                INNER JOIN tbl_profiles ins_prof
                ON ins.profile_id = ins_prof.id

                WHERE user.id = %s AND user.email = %s;
        """
        # print(f"DEBUG: Searching for ID: {current_user['id']} and Email: {current_user['email']}")

        cursor.execute(query, (current_user["id"], current_user["email"]))  
        results = cursor.fetchall()

        result_list = []
        for row in results:
            result_list.append({
                "subject": row["Subject"],
                "instructor": row["Instructor"]
            })

        return jsonify(result_list), 200
             
    except Exception as e:
        return jsonify({"message": f"Error retrieving data {e}"}), 500

