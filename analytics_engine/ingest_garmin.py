import os
import logging
from datetime import datetime
from garminconnect import Garmin
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import insert

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback for local testing if not in Docker
    DATABASE_URL = "postgresql://user:password@localhost:5432/aerofit"

Base = declarative_base()

class Activity(Base):
    __tablename__ = 'activities'

    activity_id = Column(BigInteger, primary_key=True)
    date = Column(DateTime, nullable=False)
    activity_type = Column(String, nullable=False) # 'run' or 'race'
    avg_hr = Column(Integer)
    max_hr = Column(Integer)
    avg_speed_mps = Column(Float)
    distance_meters = Column(Float)
    duration_seconds = Column(Float)
    rpe = Column(Float, nullable=True)

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine) # Ensure table exists
    return sessionmaker(bind=engine)

def get_garmin_client(email=None, password=None):
    if not email:
        email = os.getenv("GARMIN_EMAIL")
    if not password:
        password = os.getenv("GARMIN_PASSWORD")
        
    if not email or not password:
        raise ValueError("GARMIN_EMAIL and GARMIN_PASSWORD must be set")
    
    try:
        client = Garmin(email, password)
        client.login()
        return client
    except Exception as e:
        logger.error(f"Failed to authenticate with Garmin: {e}")
        raise

def process_activities(email=None, password=None):
    try:
        Session = init_db()
        session = Session()
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e

    try:
        client = get_garmin_client(email, password)
        
        logger.info("Fetching last 50 activities...")
        activities = client.get_activities(0, 50)
        
        inserted_count = 0
        updated_count = 0
        
        for activity in activities:
            # Filter: Only running
            if activity.get('activityType', {}).get('typeKey') != 'running':
                continue
                
            # Extract Data
            activity_id = activity['activityId']
            # Parse date: "2023-10-27 08:00:00"
            try:
                start_time_local = datetime.strptime(activity['startTimeLocal'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # Handle potential ISO format differences
                start_time_local = datetime.fromisoformat(activity['startTimeLocal'])

            # Race Detection
            event_type_id = activity.get('eventType', {}).get('typeId')
            activity_name = activity.get('activityName', '')
            
            is_race = False
            if event_type_id in [3, 4]: # 3=Race, 4=Special Event
                is_race = True
            elif 'race' in activity_name.lower():
                is_race = True
                
            activity_type = 'race' if is_race else 'run'
            
            # Metrics
            avg_hr = activity.get('averageHR')
            max_hr = activity.get('maxHR')
            avg_speed = activity.get('averageSpeed')
            distance = activity.get('distance')
            duration = activity.get('duration')
            rpe = activity.get('rpe') 
            
            # Upsert Logic
            stmt = insert(Activity).values(
                activity_id=activity_id,
                date=start_time_local,
                activity_type=activity_type,
                avg_hr=avg_hr,
                max_hr=max_hr,
                avg_speed_mps=avg_speed,
                distance_meters=distance,
                duration_seconds=duration,
                rpe=rpe
            )
            
            do_update_stmt = stmt.on_conflict_do_update(
                index_elements=['activity_id'],
                set_={
                    'date': stmt.excluded.date,
                    'activity_type': stmt.excluded.activity_type,
                    'avg_hr': stmt.excluded.avg_hr,
                    'max_hr': stmt.excluded.max_hr,
                    'avg_speed_mps': stmt.excluded.avg_speed_mps,
                    'distance_meters': stmt.excluded.distance_meters,
                    'duration_seconds': stmt.excluded.duration_seconds,
                    'rpe': stmt.excluded.rpe
                }
            )
            
            # Check existence for logging
            existing = session.query(Activity).filter_by(activity_id=activity_id).first()
            
            try:
                session.execute(do_update_stmt)
                session.commit()
                
                if existing:
                    updated_count += 1
                else:
                    inserted_count += 1
                    
            except Exception as e:
                logger.error(f"Error processing activity {activity_id}: {e}")
                session.rollback()
                
        session.close()
        print(f"Fetched 50 activities. Inserted {inserted_count} new, Updated {updated_count}.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    process_activities()
