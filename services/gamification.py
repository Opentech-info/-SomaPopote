from africastalking.AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
from database import get_user_points, update_user_points, log_reward
import datetime

# Africa's Talking credentials (in production, use environment variables)
USERNAME = 'sandbox'  # Replace with your Africa's Talking username
API_KEY = 'your_api_key_here'  # Replace with your Africa's Talking API key

# Reward configuration
REWARD_CONFIG = {
    'quiz_correct': {
        'points': 10,
        'airtime': 100,  # TZS
        'message': 'Sahihi! Umepata {points} points na Tsh {airtime} ya airtime!'
    },
    'lesson_completed': {
        'points': 5,
        'airtime': 50,
        'message': 'Hongera! Umekamilisha somo na kupata {points} points!'
    },
    'daily_streak': {
        'points': 20,
        'airtime': 200,
        'message': 'Streak ya siku 3! Umepata {points} points na Tsh {airtime}!'
    },
    'weekly_top': {
        'points': 50,
        'airtime': 500,
        'message': 'Mshindi wa wiki! Umepata {points} points na Tsh {airtime}!'
    }
}

def initialize_airtime_gateway():
    """Initialize Africa's Talking gateway for airtime"""
    try:
        gateway = AfricasTalkingGateway(USERNAME, API_KEY)
        return gateway
    except AfricasTalkingGatewayException as e:
        print(f"Error initializing airtime gateway: {e}")
        return None

def award_airtime(phone_number, amount):
    """
    Send airtime to a phone number
    
    Args:
        phone_number (str): Recipient's phone number
        amount (int): Airtime amount in TZS
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        gateway = initialize_airtime_gateway()
        if not gateway:
            return False
            
        # Ensure phone number is in international format
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '+255' + phone_number[1:]  # Tanzania format
            elif phone_number.startswith('255'):
                phone_number = '+' + phone_number
        
        # Send airtime
        result = gateway.sendAirtime(phone_number, str(amount))
        
        if result and len(result) > 0:
            status = result[0]['status']
            if status == 'Sent':
                print(f"Airtime sent successfully to {phone_number}: Tsh {amount}")
                return True
            else:
                print(f"Airtime failed to {phone_number}: {status}")
                return False
        else:
            print(f"No response from Africa's Talking for airtime to {phone_number}")
            return False
            
    except AfricasTalkingGatewayException as e:
        print(f"Error sending airtime to {phone_number}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error sending airtime: {e}")
        return False

def award_points(phone_number, points, reason):
    """
    Award learning points to a user
    
    Args:
        phone_number (str): User's phone number
        points (int): Points to award
        reason (str): Reason for awarding points
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get current points
        current_points = get_user_points(phone_number)
        
        # Update points
        new_points = current_points + points
        success = update_user_points(phone_number, new_points)
        
        if success:
            # Log the reward
            log_reward(phone_number, 'points', points, reason)
            print(f"Awarded {points} points to {phone_number} for {reason}")
            return True
        else:
            print(f"Failed to award points to {phone_number}")
            return False
            
    except Exception as e:
        print(f"Error awarding points: {e}")
        return False

def process_quiz_reward(phone_number, is_correct):
    """
    Process reward for quiz completion
    
    Args:
        phone_number (str): User's phone number
        is_correct (bool): Whether the answer was correct
        
    Returns:
        dict: Reward information
    """
    if is_correct:
        reward_config = REWARD_CONFIG['quiz_correct']
        
        # Award points
        points_success = award_points(phone_number, reward_config['points'], 'Correct quiz answer')
        
        # Award airtime
        airtime_success = award_airtime(phone_number, reward_config['airtime'])
        
        return {
            'success': points_success and airtime_success,
            'points': reward_config['points'],
            'airtime': reward_config['airtime'],
            'message': reward_config['message'].format(
                points=reward_config['points'],
                airtime=reward_config['airtime']
            )
        }
    else:
        return {
            'success': False,
            'points': 0,
            'airtime': 0,
            'message': 'Jaribu tena! Endelea kujifunza.'
        }

def process_lesson_completion_reward(phone_number, subject):
    """
    Process reward for lesson completion
    
    Args:
        phone_number (str): User's phone number
        subject (str): Subject completed
        
    Returns:
        dict: Reward information
    """
    reward_config = REWARD_CONFIG['lesson_completed']
    
    # Award points
    points_success = award_points(phone_number, reward_config['points'], f'Completed {subject} lesson')
    
    # Award airtime
    airtime_success = award_airtime(phone_number, reward_config['airtime'])
    
    return {
        'success': points_success and airtime_success,
        'points': reward_config['points'],
        'airtime': reward_config['airtime'],
        'message': reward_config['message'].format(
            points=reward_config['points'],
            airtime=reward_config['airtime']
        )
    }

def check_and_award_streak_bonus(phone_number):
    """
    Check user's learning streak and award bonus if applicable
    
    Args:
        phone_number (str): User's phone number
        
    Returns:
        dict: Streak bonus information
    """
    # This would typically check the database for consecutive days of activity
    # For demo purposes, we'll simulate a 3-day streak
    
    # In real implementation, you would:
    # 1. Get user's activity history
    # 2. Count consecutive days of activity
    # 3. Award bonus if streak threshold is met
    
    # Simulating a 3-day streak
    streak_days = 3
    
    if streak_days >= 3:
        reward_config = REWARD_CONFIG['daily_streak']
        
        # Award points
        points_success = award_points(phone_number, reward_config['points'], f'{streak_days}-day streak bonus')
        
        # Award airtime
        airtime_success = award_airtime(phone_number, reward_config['airtime'])
        
        return {
            'success': points_success and airtime_success,
            'points': reward_config['points'],
            'airtime': reward_config['airtime'],
            'streak_days': streak_days,
            'message': reward_config['message'].format(
                points=reward_config['points'],
                airtime=reward_config['airtime']
            )
        }
    
    return {
        'success': False,
        'points': 0,
        'airtime': 0,
        'streak_days': streak_days,
        'message': f'Endelea kujifunza! Unazo siku {streak_days} za mfululizo.'
    }

def get_leaderboard(limit=10):
    """
    Get weekly leaderboard of top performers
    
    Args:
        limit (int): Number of top users to return
        
    Returns:
        list: Leaderboard data
    """
    # This would typically query the database for top performers
    # For demo purposes, we'll return mock data
    
    mock_leaderboard = [
        {'phone_number': '+255714123456', 'points': 450, 'name': 'Juma'},
        {'phone_number': '+255714123457', 'points': 380, 'name': 'Asha'},
        {'phone_number': '+255714123458', 'points': 320, 'name': 'Fatuma'},
        {'phone_number': '+255714123459', 'points': 280, 'name': 'Bakari'},
        {'phone_number': '+255714123460', 'points': 250, 'name': 'Zainab'},
    ]
    
    return mock_leaderboard[:limit]

def award_weekly_top_performer():
    """
    Award bonus to weekly top performer
    
    Returns:
        dict: Award information
    """
    leaderboard = get_leaderboard(1)
    
    if leaderboard:
        top_performer = leaderboard[0]
        reward_config = REWARD_CONFIG['weekly_top']
        
        # Award points
        points_success = award_points(
            top_performer['phone_number'], 
            reward_config['points'], 
            'Weekly top performer bonus'
        )
        
        # Award airtime
        airtime_success = award_airtime(top_performer['phone_number'], reward_config['airtime'])
        
        return {
            'success': points_success and airtime_success,
            'phone_number': top_performer['phone_number'],
            'points': reward_config['points'],
            'airtime': reward_config['airtime'],
            'message': f"Hongera {top_performer['name']}! Ume mshindi wa wiki!"
        }
    
    return {
        'success': False,
        'message': 'Hakuna mshindi wa wiki hii.'
    }

def get_user_achievements(phone_number):
    """
    Get user's achievements and badges
    
    Args:
        phone_number (str): User's phone number
        
    Returns:
        dict: User achievements
    """
    # This would typically query the database for user achievements
    # For demo purposes, we'll return mock data based on points
    
    current_points = get_user_points(phone_number)
    
    achievements = []
    
    if current_points >= 50:
        achievements.append({
            'name': 'Mwanafunzi Mzuri',
            'description': 'Umepata angalau pointi 50',
            'icon': '🌟'
        })
    
    if current_points >= 100:
        achievements.append({
            'name': 'Mshindi',
            'description': 'Umepata angalau pointi 100',
            'icon': '🏆'
        })
    
    if current_points >= 200:
        achievements.append({
            'name': 'Mtaalamu',
            'description': 'Umepata angalau pointi 200',
            'icon': '🎓'
        })
    
    if current_points >= 500:
        achievements.append({
            'name': 'Mfanyakazi Bora',
            'description': 'Umepata angalau pointi 500',
            'icon': '👑'
        })
    
    return {
        'phone_number': phone_number,
        'total_points': current_points,
        'achievements': achievements
    }

def create_referral_program(phone_number, referred_by=None):
    """
    Create or handle referral program
    
    Args:
        phone_number (str): User's phone number
        referred_by (str): Phone number of user who referred them
        
    Returns:
        dict: Referral program information
    """
    referral_bonus = {
        'points': 25,
        'airtime': 150,
        'message': 'Umepokea zawadi ya rafiki! {points} points + Tsh {airtime}'
    }
    
    if referred_by:
        # Award bonus to both referrer and referred
        # Award to referrer
        award_points(referred_by, referral_bonus['points'], 'Referral bonus')
        award_airtime(referred_by, referral_bonus['airtime'])
        
        # Award to referred user
        award_points(phone_number, referral_bonus['points'], 'Referral welcome bonus')
        award_airtime(phone_number, referral_bonus['airtime'])
        
        return {
            'success': True,
            'message': referral_bonus['message'].format(
                points=referral_bonus['points'],
                airtime=referral_bonus['airtime']
            )
        }
    
    return {
        'success': False,
        'message': 'Tumia namba ya rafiki kwenye usajili kupokea zawadi.'
    }
