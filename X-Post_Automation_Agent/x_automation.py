import tweepy
import os
import schedule
import time
import datetime
import logging

#client_id M09ZdHB0SzIyWE84dWU5Y1JrWGw6MTpjaQ
#clientsecret e4iPCWn0NcwmK2SyridUgTqoH84JhgvcIfV5niyKK8_hcbG_wF
# Global variable to hold the authenticated Tweepy client.It's initialized to None and set after successful authentication.
twitter_client = None

# Configure logging to save bot activity to a file
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. Twitter API Credentials ---

API_KEY = "ohY4uAJeJT0JLf2ltHLkCbVLU"
API_SECRET = "dWd8MqiwfjTbgU0AUgvFj0mrZLF6zWIpsdkNNXz17GL4klY35M"
ACCESS_TOKEN = "1939935941075816448-1Nfvu50OYaIeQ06U7ZtRpQ1LDbmE41"
ACCESS_TOKEN_SECRET = "dihbFQ5noFpp72GvjchiDyEj4jwNsIrYYnmsZPyYQj702"


#--2. Twitter API Functions
def authenticate_twitter_api():
    global twitter_client
    
   
    # It now only checks if any of the key variables are empty or None.
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        logging.critical("API credentials are not fully set. Please ensure API_KEY, API_SECRET, ACCESS_TOKEN, and ACCESS_TOKEN_SECRET variables are populated.")
        print("Error: API credentials are not fully set. Please update them in the script. 🚨")
        return False
    
    try:
        twitter_client = tweepy.Client(
            consumer_key = API_KEY,
            consumer_secret = API_SECRET,
            access_token = ACCESS_TOKEN,
            access_token_secret = ACCESS_TOKEN_SECRET
        )
        logging.info("Authentication successful with Twitter API.")
        print("Authentication successful! 🎉") 
        return True
    
    except Exception as e:
        logging.critical(f"Authentication failed: {e}")
        print(f"Authentication failed: {e} 😞 Check your API keys and network connection.")
        return False
    

def post_tweet(tweet_text):
    """
    Posts a given tweet_text to X.com using the authenticated Twitter client.
    Logs the outcome and prints messages to the console.
    Returns the tweet data (ID, text) if successful, None otherwise.
    """
    # Ensures that the Twitter client has been successfully authenticated before attempting to post.
    if not twitter_client:
        logging.error("Twitter client not authenticated. Cannot post tweet.")
        print("Error: Twitter client not authenticated. Cannot post tweet. 🚫")
        return None

    try:
        # Use the create_tweet method from the tweepy.Client to publish the tweet.
        response = twitter_client.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        tweet_text_posted = response.data['text']
        logging.info(f"Tweet posted successfully! ID: {tweet_id}, Text: '{tweet_text_posted}'")
        print(f"Tweet posted successfully! 🚀 Tweet ID: {tweet_id}, Text: '{tweet_text_posted}'")
        return response.data
    except tweepy.TweepyException as e:
        # Catches specific errors related to Twitter API interactions (e.g., duplicate tweet, rate limits).
        logging.error(f"Error posting tweet (TweepyException): {e}")
        print(f"Error posting tweet: {e}. Check API limits or tweet content. 🤕")
        return None
    except Exception as e:
        # Catches any other unexpected errors during the tweeting process.
        logging.critical(f"An unexpected error occurred while posting tweet: {e}")
        print(f"An unexpected error occurred while posting tweet: {e}. Please review the code or logs. 🐛")
        return None
    
# --- 3. Content Generation ---

def get_daily_tweet_content():
    """
    Generates dynamic tweet content based on the current day of the week.
    You can customize the messages for each day here.
    """
    today = datetime.date.today()
    day_of_week = today.strftime("%A") # Gets the full weekday name (e.g., "Monday", "Tuesday")
    
    # Dictionary containing custom messages for each day of the week.
    # The current location context (Uganda/Kampala) is integrated into the messages.
    messages = {
        "Monday": "Good morning from Kampala! Starting the week with some Python automation. Let's build something cool! #MondayMotivation #Uganda 🇺🇬",
        "Tuesday": "It's Tuesday in the Pearl of Africa! Working on my AI agent to automate social media posts. Progress is key! 💡 #Python #Automation",
        "Wednesday": "Happy Hump Day from Uganda! Halfway through the week, and my bot is still tweeting. What's your favorite part of coding? 💻 #WednesdayWisdom",
        "Thursday": "Almost the weekend in Kampala! My automated posts are running smoothly. What tech are you exploring today? ✨ #TechInnovation",
        "Friday": "TGIF from Uganda! Wishing everyone a fantastic weekend. My bot's last post for the work week is out! 🎉 #WeekendVibes",
        "Saturday": "Saturday vibes! Whether you're coding or relaxing in Uganda, make it count. My bot is taking a break too! ☀️ #SaturdayFun",
        "Sunday": "Sunday chill. Time to recharge and reflect before a new week in Kampala. Peaceful moments. 😌 #Relaxation"
    }
    
    # Fallback message if for some reason the day of the week isn't found (shouldn't happen with strftime).
    default_message = f"Hello from my Python automation script on {day_of_week}, {today.strftime('%Y-%m-%d')}! This is an automated update. #PythonBot #Learning"
    
    return messages.get(day_of_week, default_message)

# --- 4. Scheduling the Task ---

def daily_post_job():
    """
    The main job function that the scheduler will execute daily.
    It orchestrates content generation and tweeting.
    """
    print(f"\n--- Running daily post job at {time.strftime('%H:%M:%S')} EAT ---")
    logging.info(f"Attempting to run daily post job.")
    
    # Before posting, re-check if the Twitter client is still authenticated.
    # This handles cases where connection might have dropped or tokens expired.
    if not twitter_client:
        print("Twitter client not authenticated. Attempting re-authentication...")
        logging.warning("Twitter client not authenticated during daily job. Attempting re-authentication.")
        if not authenticate_twitter_api(): # Try to re-authenticate
            print("Failed to re-authenticate. Skipping post for today. 🔴")
            logging.error("Failed to re-authenticate during daily job. Skipping post.")
            return # Exit the job if re-authentication fails

    content = get_daily_tweet_content() # Get the tweet text for today
    post_tweet(content) # Post the tweet
    print("--- Daily post job finished ---")
    logging.info("Daily post job completed.")

# --- 5. Main Execution Block ---

# This block ensures that the code inside it only runs when the script is executed directly,
# not when it's imported as a module into another script.
if __name__ == "__main__":
    print("Starting Twitter Automation Bot... 🤖")
    logging.info("Bot starting up.")
    
    # 5.1 Authenticate with Twitter API upon bot startup.
    # If this initial authentication fails, the bot cannot function, so it exits.
    if not authenticate_twitter_api():
        print("Bot could not start due to initial authentication failure. Please check your credentials in the script and your network connection. Exiting.")
        logging.critical("Bot terminated due to initial authentication failure.")
        exit() # Stop the script if authentication fails

    # --- FOR TESTING: Trigger an immediate post after successful auth ---
    # Uncomment the line below if you want the bot to post immediately upon running the script
    # This is useful for quick testing without waiting for the scheduled time.
    print("Triggering immediate post for testing purposes...")
    daily_post_job() # Call the job function once immediately
    # --- END TESTING SECTION ---

    # 5.2 Schedule the job to run 2 minutes from now.
    # Get the current time
    now = datetime.datetime.now()
    # Calculate the time 2 minutes from now
    future_time = now + datetime.timedelta(minutes=2)
    # Format it as HH:MM
    time_to_schedule = future_time.strftime("%H:%M") 

    schedule.every().day.at(time_to_schedule).do(daily_post_job) # Schedule for 2 minutes from now
    
    print(f"Scheduler initialized. The bot will attempt to post daily at {time_to_schedule} EAT (local time).")
    print("Keep this window/terminal open for the scheduler to run. Use Ctrl+C to stop the bot.")
    logging.info(f"Scheduler started successfully and waiting for tasks. Next post scheduled for {time_to_schedule}.")

    # 5.3 Main loop to keep the script running and check for scheduled tasks.
    # The 'while True' loop continuously checks if any scheduled jobs are due.
    while True:
        try:
            schedule.run_pending() # Executes any scheduled jobs that are ready to run.
            time.sleep(1) # Pauses the loop for 1 second to prevent high CPU usage.
        except KeyboardInterrupt:
            # Allows the user to gracefully stop the bot by pressing Ctrl+C in the terminal.
            print("\nBot stopped by user (Ctrl+C). Exiting.")
            logging.info("Bot stopped by user (KeyboardInterrupt).")
            break 
        except Exception as e:
            # Catches any unexpected errors that might occur within the scheduler loop itself.
            logging.error(f"An unexpected error occurred in the main scheduler loop: {e}")
            print(f"An unexpected error occurred in the main scheduler loop: {e}. Waiting 5 seconds before retrying...")
            time.sleep(5) # Waits for a few seconds before retrying after an error.
            
            
#