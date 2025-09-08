from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
import os

# Africa's Talking credentials (in production, use environment variables)
USERNAME = 'sandbox'  # Replace with your Africa's Talking username
API_KEY = 'your_api_key_here'  # Replace with your Africa's Talking API key

def initialize_gateway():
    """Initialize Africa's Talking gateway"""
    try:
        gateway = AfricasTalkingGateway(USERNAME, API_KEY)
        return gateway
    except AfricasTalkingGatewayException as e:
        print(f"Error initializing Africa's Talking gateway: {e}")
        return None

def send_sms(phone_number, message):
    """
    Send SMS to a phone number
    
    Args:
        phone_number (str): Recipient's phone number in international format
        message (str): Message content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        gateway = initialize_gateway()
        if not gateway:
            return False
            
        # Ensure phone number is in international format
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '+255' + phone_number[1:]  # Tanzania format
            elif phone_number.startswith('255'):
                phone_number = '+' + phone_number
        
        # Send SMS
        recipients = gateway.sendMessage(phone_number, message)
        
        # Check if message was sent successfully
        if recipients and len(recipients) > 0:
            status = recipients[0]['status']
            if status == 'Success':
                print(f"SMS sent successfully to {phone_number}")
                return True
            else:
                print(f"SMS failed to {phone_number}: {status}")
                return False
        else:
            print(f"No response from Africa's Talking for {phone_number}")
            return False
            
    except AfricasTalkingGatewayException as e:
        print(f"Error sending SMS to {phone_number}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error sending SMS: {e}")
        return False

def send_quiz_sms(phone_number, subject, question, options):
    """
    Send a quiz question via SMS
    
    Args:
        phone_number (str): Recipient's phone number
        subject (str): Subject of the quiz
        question (str): Quiz question
        options (dict): Dictionary of options (e.g., {'A': 'Option 1', 'B': 'Option 2'})
        
    Returns:
        bool: True if successful, False otherwise
    """
    message = f"SOMAPOPOTE - {subject}\n"
    message += f"Swali: {question}\n"
    
    for key, value in options.items():
        message += f"{key}. {value}\n"
    
    message += "\nJibu: Tuma JIBU [herufi ya jibu]"
    
    return send_sms(phone_number, message)

def send_lesson_reminder(phone_number, subject, time):
    """
    Send lesson reminder via SMS
    
    Args:
        phone_number (str): Recipient's phone number
        subject (str): Subject reminder
        time (str): Time for the lesson
        
    Returns:
        bool: True if successful, False otherwise
    """
    message = f"SOMAPOPOTE - Kumbukumbu\n"
    message += f"Somo la {subject} linaanza saa {time}\n"
    message += "Usikose kuwepo!"
    
    return send_sms(phone_number, message)

def send_progress_report(phone_number, student_name, progress_data):
    """
    Send student progress report to parents via SMS
    
    Args:
        phone_number (str): Parent's phone number
        student_name (str): Student's name
        progress_data (dict): Progress data including subjects and scores
        
    Returns:
        bool: True if successful, False otherwise
    """
    message = f"SOMAPOPOTE - Ripoti ya Mwanafunzi\n"
    message += f"Mwanafunzi: {student_name}\n\n"
    
    total_points = progress_data.get('total_points', 0)
    message += f"Jumla ya Pointi: {total_points}\n\n"
    
    subjects = progress_data.get('subjects', {})
    if subjects:
        message += "Matokeo kwa somo:\n"
        for subject, points in subjects.items():
            message += f"{subject}: {points} points\n"
    
    message += "\nEndelea kumshauri kujifunza zaidi."
    
    return send_sms(phone_number, message)

def send_airtime_reward_notification(phone_number, amount, reason):
    """
    Send airtime reward notification via SMS
    
    Args:
        phone_number (str): Recipient's phone number
        amount (int): Airtime amount rewarded
        reason (str): Reason for the reward
        
    Returns:
        bool: True if successful, False otherwise
    """
    message = f"SOMAPOPOTE - zawadi ya Airtime!\n"
    message += f"Hongera! Umepokea Tsh {amount} ya airtime.\n"
    message += f"Sababu: {reason}\n"
    message += "Endelea kujifunza kwa bidii!"
    
    return send_sms(phone_number, message)

def send_bulk_sms(phone_numbers, message):
    """
    Send bulk SMS to multiple phone numbers
    
    Args:
        phone_numbers (list): List of phone numbers
        message (str): Message content
        
    Returns:
        dict: Results with success count and failed numbers
    """
    results = {
        'success_count': 0,
        'failed_numbers': [],
        'total_numbers': len(phone_numbers)
    }
    
    for phone_number in phone_numbers:
        if send_sms(phone_number, message):
            results['success_count'] += 1
        else:
            results['failed_numbers'].append(phone_number)
    
    return results

def process_sms_command(phone_number, message):
    """
    Process incoming SMS commands
    
    Args:
        phone_number (str): Sender's phone number
        message (str): SMS message content
        
    Returns:
        str: Response message
    """
    message = message.strip().upper()
    
    if message.startswith('QUIZ'):
        # Send a random quiz
        return send_random_quiz(phone_number)
    
    elif message.startswith('JIBU'):
        # Process quiz answer
        return process_quiz_answer(phone_number, message)
    
    elif message.startswith('MAELEZO'):
        # Send service information
        info_message = "SOMAPOPOTE - Elimu kwa simu yako!\n"
        info_message += "Piga *384*200# kuanza\n"
        info_message += "Au tuma QUIZ kupata maswali"
        return send_sms(phone_number, info_message)
    
    elif message.startswith('MSAADA'):
        # Send help information
        help_message = "SOMAPOPOTE - Msaada\n"
        help_message += "Amri zilizopo:\n"
        help_message += "QUIZ - Pata maswali\n"
        help_message += "JIBU X - Jibu swali\n"
        help_message += "MAELEZO - Maelezo ya huduma\n"
        help_message += "MSAADA - Usaidizi"
        return send_sms(phone_number, help_message)
    
    else:
        # Unknown command
        response = "Samahani, sikuelewi amri. Tuma MSAADA kwa usaidizi."
        return send_sms(phone_number, response)

def send_random_quiz(phone_number):
    """Send a random quiz question to the user"""
    import random
    
    quizzes = [
        {
            'subject': 'Hisabati',
            'question': '3 + 5 = ?',
            'options': {'A': '7', 'B': '8', 'C': '9'}
        },
        {
            'subject': 'Sayansi',
            'question': 'Ni gani chanzo kikuu cha nishati?',
            'options': {'A': 'Jua', 'B': 'Mwezi', 'C': 'Nyota'}
        },
        {
            'subject': 'Kiswahili',
            'question': 'Nini maana ya \'elimu\'?',
            'options': {'A': 'Chakula', 'B': 'Elimu', 'C': 'Mavazi'}
        }
    ]
    
    quiz = random.choice(quizzes)
    return send_quiz_sms(phone_number, quiz['subject'], quiz['question'], quiz['options'])

def process_quiz_answer(phone_number, message):
    """Process quiz answer from user"""
    # This would typically check against a stored quiz and correct answer
    # For demo purposes, we'll assume any answer starting with JIBU B is correct
    
    parts = message.split()
    if len(parts) >= 2:
        answer = parts[1]
        
        # Simple logic: if answer is B, it's correct (for demo)
        if answer == 'B':
            response = "Sahihi! Umepata pointi + airtime 🎉"
            # In real implementation, would award airtime and update progress
        else:
            response = "Sio sahihi. Jaribu tena!"
        
        return send_sms(phone_number, response)
    else:
        response = "Tafadhali jibu kwa mfano: JIBU B"
        return send_sms(phone_number, response)
