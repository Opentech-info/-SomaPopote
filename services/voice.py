import africastalking
import random

# Africa's Talking credentials (in production, use environment variables)
USERNAME = 'sandbox'  # Replace with your Africa's Talking username
API_KEY = 'your_api_key_here'  # Replace with your Africa's Talking API key

def initialize_voice_gateway():
    """Initialize Africa's Talking voice gateway"""
    try:
        # Initialize Africa's Talking
        africastalking.initialize(USERNAME, API_KEY)
        voice = africastalking.Voice
        return voice
    except Exception as e:
        print(f"Error initializing Africa's Talking voice gateway: {e}")
        return None

def voice_lesson():
    """
    Generate IVR response for voice lessons
    
    Returns:
        str: XML response for IVR
    """
    # This would typically be called by Africa's Talking voice service
    # when a user calls the dedicated voice number
    
    # Generate a random lesson for demo
    lesson = get_random_lesson()
    
    # Create IVR response XML
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'
    
    # Play welcome message
    response += '<GetDigits finishOnKey="#" timeout="20">'
    response += '<Say voice="man" language="sw-TZ">'
    response += 'Karibu SomaPopote. Elimu kwa sauti. '
    response += 'Bonyeza moja kwa somo la Hisabati. '
    response += 'Bonyeza mbili kwa somo la Sayansi. '
    response += 'Bonyeza tatu kwa somo la Kiswahili. '
    response += 'Bonyeza nne kwa somo la English. '
    response += 'Bonyeza tano kusikiliza maelezo zaidi. '
    response += '</Say>'
    response += '</GetDigits>'
    
    response += '</Response>'
    
    return response

def get_random_lesson():
    """Get a random lesson for voice playback"""
    lessons = [
        {
            'subject': 'Hisabati',
            'title': 'Kuongeza Namba',
            'content': [
                'Leo tutajifunza kuongeza namba.',
                'Tunaona mfano. Mbili pamoja na mbili ni nne.',
                'Tatu pamoja na tatu ni sita.',
                'Nne pamoja na nne ni nane.',
                'Endelea kujifunza kuongeza namba kila siku.'
            ]
        },
        {
            'subject': 'Sayansi',
            'title': 'Mazingira',
            'content': [
                'Leo tutajifunza kuhusu mazingira.',
                'Mazingira ni vitu vinavyotuzunguka.',
                'Tunahitaji kulinda mazingira yetu.',
                'Panda miti kwa ajili ya hewa safi.',
                'Usitupie takataka barabarani.',
                'Tunaweza kufanya dunia kuwa nzuri.'
            ]
        },
        {
            'subject': 'Kiswahili',
            'title': 'Vitenzi',
            'content': [
                'Leo tutajifunza vitenzi vya Kiswahili.',
                'Mfano wa vitenzi. Ninaenda, unakwenda, anakwenda.',
                'Tunasoma, mnasoma, wanasoma.',
                'Ninapika, unapika, anapika.',
                'Vitenzi vinatufaa kusema vitu tunavyofanya.'
            ]
        },
        {
            'subject': 'English',
            'title': 'Verbs',
            'content': [
                'Today we will learn about English verbs.',
                'Verbs are action words.',
                'Example. I go, you go, he goes.',
                'We read, you read, they read.',
                'She writes, he writes, they write.',
                'Keep learning English every day.'
            ]
        }
    ]
    
    return random.choice(lessons)

def generate_lesson_audio_response(lesson_choice):
    """
    Generate audio response for specific lesson choice
    
    Args:
        lesson_choice (str): User's lesson choice (1-5)
        
    Returns:
        str: XML response for IVR
    """
    lessons = {
        '1': {
            'subject': 'Hisabati',
            'title': 'Kuongeza Namba',
            'content': [
                'Somo la Hisabati. Kuongeza namba.',
                'Mfano wa kwanza. Moja pamoja na moja ni mbili.',
                'Mfano wa pili. Mbili pamoja na mbili ni nne.',
                'Mfano wa tatu. Tatu pamoja na tatu ni sita.',
                'Endelea kujifunza hisabati kila siku.'
            ]
        },
        '2': {
            'subject': 'Sayansi',
            'title': 'Mazingira',
            'content': [
                'Somo la Sayansi. Kuhusu mazingira.',
                'Mazingira ni vitu vinavyotuzunguka.',
                'Miti ni muhimu kwa mazingira.',
                'Miti hutoa hewa safi ya kupumulia.',
                'Tunahitaji kupanda miti mingi.',
                'Tunahitaji kulinda mazingira yetu.'
            ]
        },
        '3': {
            'subject': 'Kiswahili',
            'title': 'Sarufi',
            'content': [
                'Somo la Kiswahili. Kuhusu sarufi.',
                'Leo tunajifunza vitenzi.',
                'Mfano. Ninaenda shuleni.',
                'Unakwenda sokoni.',
                'Anakwenda hospitalini.',
                'Vitenzi vinatufaa kusema tunachofanya.'
            ]
        },
        '4': {
            'subject': 'English',
            'title': 'Grammar',
            'content': [
                'English lesson. About grammar.',
                'Today we learn about verbs.',
                'Example. I go to school.',
                'You go to market.',
                'He goes to hospital.',
                'Verbs help us say what we do.'
            ]
        },
        '5': {
            'subject': 'Maelezo',
            'title': 'Kuhusu SomaPopote',
            'content': [
                'Karibu kwenye maelezo ya SomaPopote.',
                'SomaPopote ni programu ya kielimu.',
                'Inakusaidia kujifunza kupitia simu yako.',
                'Unaweza kupata maswali na kujibu.',
                'Unaweza kushinda airtime kwa kujibu maswali.',
                'Piga simu tena kwa somo jingine.'
            ]
        }
    }
    
    lesson = lessons.get(lesson_choice, lessons['5'])
    
    # Create IVR response XML
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'
    
    # Play lesson content
    response += '<Say voice="man" language="sw-TZ">'
    for line in lesson['content']:
        response += line + '. '
    response += '</Say>'
    
    # Ask if user wants another lesson
    response += '<GetDigits finishOnKey="#" timeout="15">'
    response += '<Say voice="man" language="sw-TZ">'
    response += 'Bonyeza moja kusikiliza somo jingine. '
    response += 'Bonyeza mbili kumaliza. '
    response += '</Say>'
    response += '</GetDigits>'
    
    response += '</Response>'
    
    return response

def make_voice_call(phone_number, lesson_type='general'):
    """
    Make outbound voice call for lesson delivery
    
    Args:
        phone_number (str): Recipient's phone number
        lesson_type (str): Type of lesson to deliver
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        gateway = initialize_voice_gateway()
        if not gateway:
            return False
            
        # Ensure phone number is in international format
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '+255' + phone_number[1:]  # Tanzania format
            elif phone_number.startswith('255'):
                phone_number = '+' + phone_number
        
        # Make voice call using new API syntax
        call = gateway.call(phone_number, '+255714123456')  # Your Africa's Talking voice number
        
        if call:
            print(f"Voice call initiated to {phone_number}")
            return True
        else:
            print(f"Failed to initiate voice call to {phone_number}")
            return False
            
    except Exception as e:
        print(f"Error making voice call to {phone_number}: {e}")
        return False

def schedule_voice_lesson(phone_number, scheduled_time):
    """
    Schedule a voice lesson for a specific time
    
    Args:
        phone_number (str): Student's phone number
        scheduled_time (str): Time to call (e.g., "14:00")
        
    Returns:
        bool: True if scheduled successfully, False otherwise
    """
    # In a real implementation, this would integrate with a scheduling system
    # For demo purposes, we'll just log the scheduling request
    
    try:
        print(f"Voice lesson scheduled for {phone_number} at {scheduled_time}")
        
        # Here you would integrate with a task scheduler like Celery
        # or use Africa's Talking scheduling features
        
        return True
    except Exception as e:
        print(f"Error scheduling voice lesson: {e}")
        return False

def get_voice_menu():
    """Get voice menu options"""
    menu_options = {
        'main_menu': {
            'prompt': 'Karibu SomaPopote. Bonyeza.',
            'options': {
                '1': 'Somo la Hisabati',
                '2': 'Somo la Sayansi', 
                '3': 'Somo la Kiswahili',
                '4': 'Somo la English',
                '5': 'Maelezo zaidi'
            }
        }
    }
    
    return menu_options

def create_voice_quiz():
    """Create a voice-based quiz"""
    quizzes = [
        {
            'question': 'Mbili pamoja na mbili ni ngapi?',
            'options': ['Tatu', 'Nne', 'Tano'],
            'correct_answer': 'Nfour',
            'subject': 'Hisabati'
        },
        {
            'question': 'Ni gani muhimu kwa mazingira?',
            'options': ['Takataka', 'Miti', 'Moshi'],
            'correct_answer': 'Miti',
            'subject': 'Sayansi'
        },
        {
            'question': 'Nani anasoma?',
            'options': ['Mimi', 'Wewe', 'Yeye'],
            'correct_answer': 'Mimi',
            'subject': 'Kiswahili'
        }
    ]
    
    return random.choice(quizzes)

def generate_voice_quiz_response():
    """Generate IVR response for voice quiz"""
    quiz = create_voice_quiz()
    
    response = '<?xml version="1.0" encoding="UTF-8"?>'
    response += '<Response>'
    
    response += '<GetDigits finishOnKey="#" timeout="25">'
    response += '<Say voice="man" language="sw-TZ">'
    response += f'Swali la {quiz["subject"]}. '
    response += f'{quiz["question"]} '
    
    for i, option in enumerate(quiz['options'], 1):
        response += f'Bonyeza {i} kwa {option}. '
    
    response += '</Say>'
    response += '</GetDigits>'
    
    response += '</Response>'
    
    return response
