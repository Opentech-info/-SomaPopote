from flask import request
from database import get_user_progress, update_user_progress, save_quiz_result
from services.gamification import award_airtime
from services.sms import send_sms

def ussd_menu():
    """Handle USSD menu navigation and logic"""
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    response = ""

    if text == "":
        # Main menu
        response = "CON Karibu SomaPopote - Elimu kwa simu yako!\n"
        response += "1. Anza Somo\n"
        response += "2. Jaribu Maswali\n"
        response += "3. Angalia Matokeo\n"
        response += "4. Wazazi & Walimu\n"
        response += "5. Sauti (Lessons kwa sauti)"

    elif text == "1":
        # Start lesson
        response = "CON Chagua somo:\n"
        response += "1. Hisabati - Namba\n"
        response += "2. Sayansi - Mazingira\n"
        response += "3. Kiswahili - Sarufi\n"
        response += "4. English - Grammar"

    elif text == "1*1":
        # Mathematics lesson
        response = "END Somo la Hisabati: Namba\n"
        response += "Leo utajifunza kuongeza na kutoa.\n"
        response += "Mfano: 2 + 2 = 4\n"
        response += "Endelea kujifunza kupitia App au SMS."

    elif text == "1*2":
        # Science lesson
        response = "END Somo la Sayansi: Mazingira\n"
        response += "Leo utajifunza kuhusu mazingira.\n"
        response += "Tunahitaji kulinda mazingira yetu.\n"
        response += "Panda miti na usitupie takataka."

    elif text == "1*3":
        # Swahili lesson
        response = "END Somo la Kiswahili: Sarufi\n"
        response += "Leo utajifunza kuhusu vitenzi.\n"
        response += "Mfano: Ninaenda, Unakwenda, Anakwenda\n"
        response += "Endelea kujifunza zaidi."

    elif text == "1*4":
        # English lesson
        response = "END Somo la English: Grammar\n"
        response += "Today you will learn about verbs.\n"
        response += "Example: I go, You go, He/She goes\n"
        response += "Keep learning!"

    elif text == "2":
        # Quiz menu
        response = "CON Chenga somo la maswali:\n"
        response += "1. Hisabati\n"
        response += "2. Sayansi\n"
        response += "3. Kiswahili\n"
        response += "4. English"

    elif text == "2*1":
        # Mathematics quiz
        response = "CON Swali la Hisabati:\n"
        response += "2 + 2 = ?\n"
        response += "1. 3\n"
        response += "2. 4\n"
        response += "3. 5"

    elif text == "2*1*2":
        # Correct answer for math quiz
        save_quiz_result(phone_number, "Hisabati", True)
        award_airtime(phone_number, 100)  # Award 100 TZS
        update_user_progress(phone_number, "Hisabati", 10)
        response = "END Sahihi! Umeshinda pointi 10 + Tsh 100 ya airtime 🎉\n"
        response += "Endelea kujifunza!"

    elif text == "2*1*1" or text == "2*1*3":
        # Wrong answer for math quiz
        save_quiz_result(phone_number, "Hisabati", False)
        response = "END Sio sahihi. Jaribu tena!\n"
        response += "Jibu sahihi ni 4.\n"
        response += "Usisahau kujifunza zaidi."

    elif text == "2*2":
        # Science quiz
        response = "CON Swali la Sayansi:\n"
        response += "Ni gani muhimu kwa mazingira?\n"
        response += "1. Miti\n"
        response += "2. Takataka\n"
        response += "3. Moshi"

    elif text == "2*2*1":
        # Correct answer for science quiz
        save_quiz_result(phone_number, "Sayansi", True)
        award_airtime(phone_number, 100)
        update_user_progress(phone_number, "Sayansi", 10)
        response = "END Sahihi! Umeshinda pointi 10 + Tsh 100 ya airtime 🎉\n"
        response += "Miti ni muhimu kwa mazingira!"

    elif text == "3":
        # Check results
        progress = get_user_progress(phone_number)
        if progress:
            total_points = progress.get('total_points', 0)
            response = f"END Matokeo yako:\n"
            response += f"Jumla ya pointi: {total_points}\n"
            for subject, points in progress.get('subjects', {}).items():
                response += f"{subject}: {points} points\n"
            response += "Endelea kujifunza!"
        else:
            response = "END Haujaanza kujifunza bado.\n"
            response += "Anza somo kupiga 1 kwenye menyu kuu."

    elif text == "4":
        # Parent/Teacher menu
        response = "CON Wazazi/Walimu:\n"
        response += "1. Angalia Mahudhurio\n"
        response += "2. Tuma Ujumbe kwa Wazazi\n"
        response += "3. Angalia Matokeo ya Mwanafunzi"

    elif text == "4*1":
        # Check attendance (simplified)
        response = "END Mahudhurio:\n"
        response += "Jumatatu: Present\n"
        response += "Jumanne: Present\n"
        response += "Jumatano: Absent\n"
        response += "Alhamisi: Present"

    elif text == "4*2":
        # Send message to parents
        response = "CON Andika ujumbe wa kutuma kwa wazazi:\n"
        response += "(Tuma ujumbe lako, mfano: Mkutano wa wazazi Jumatano)"

    elif text.startswith("4*2*"):
        # Process the message to send
        message = text.split("*", 2)[2] if len(text.split("*")) > 2 else ""
        if message:
            # In real implementation, this would send to all parent numbers
            response = f"END Ujumbe wako '{message}' umetumwa kwa wazazi."
        else:
            response = "END Hitilafu: Tafadhali andika ujumbe."

    elif text == "4*3":
        # Check student results
        response = "CON Weka namba ya simu ya mwanafunzi:"

    elif text.startswith("4*3*"):
        student_phone = text.split("*", 2)[2] if len(text.split("*")) > 2 else ""
        if student_phone:
            progress = get_user_progress(student_phone)
            if progress:
                total_points = progress.get('total_points', 0)
                response = f"END Matokeo ya mwanafunzi {student_phone}:\n"
                response += f"Jumla ya pointi: {total_points}\n"
                for subject, points in progress.get('subjects', {}).items():
                    response += f"{subject}: {points} points\n"
            else:
                response = "END Hakuna matokeo yaliyopatikana kwa namba hiyo."
        else:
            response = "END Hitilafu: Tafadhali weka namba sahihi ya simu."

    elif text == "5":
        # Voice lessons menu
        response = "CON Sauti Lessons:\n"
        response += "1. Piga simu kusikiliza somo\n"
        response += "2. Weka namba ya simu kupokea simu"

    elif text == "5*1":
        # Provide voice lesson number
        response = "END Piga +255714123456 kusikiliza somo la sauti.\n"
        response += "Somu zitapatikana kwa lugha ya Kiswahili na English."

    elif text == "5*2":
        # Request callback for voice lesson
        response = "END Tafadhali subiri tutakupigia simu kutoa somo.\n"
        response += "Simu itatolewa ndani ya dakika 5."

    else:
        response = "END Asante kwa kutumia SomaPopote.\n"
        response += "Piga simu tena kwa elimu zaidi."

    return response
