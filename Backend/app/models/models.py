from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Boolean, Numeric, func, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from database.database import Base

class Circuit(Base):
    __tablename__ = "circuits"
    
    circuit_id = Column(String(100), primary_key=True)
    circuit_name = Column(String(255), nullable=False)
    location = Column(String(255))
    country = Column(String(100))
    latitude = Column(Numeric(10, 6))
    longitude = Column(Numeric(10, 6))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    races = relationship("Race", back_populates="circuit")

class Race(Base):
    __tablename__ = "races"
    
    race_id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    race_name = Column(String(255), nullable=False)
    circuit_id = Column(String(100), ForeignKey('circuits.circuit_id'), nullable=False)
    circuit_name = Column(String(255))
    country = Column(String(100))
    date = Column(Date)
    start_datetime = Column(DateTime(timezone=True))
    end_datetime = Column(DateTime(timezone=True))
    is_sprint = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    circuit = relationship("Circuit", back_populates="races")
    results = relationship("RaceResult", back_populates="race")

class Driver(Base):
    __tablename__ = "drivers"
    
    driver_id = Column(String(100), primary_key=True)
    driver_number = Column(Integer)
    driver_code = Column(String(10))
    driver_forename = Column(String(100))
    driver_surname = Column(String(100))
    driver_full_name = Column(String(200))
    nationality = Column(String(100))
    team_id = Column(String(100), ForeignKey('teams.team_id'), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    results = relationship("RaceResult", back_populates="driver")
    predictions = relationship("Prediction", back_populates="predicted_winner")
    driver_standings = relationship("DriverStanding", back_populates="driver")

class Team(Base):
    __tablename__ = "teams"
    
    team_id = Column(String(100), primary_key=True)
    team_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    results = relationship("RaceResult", back_populates="team")
    team_standings = relationship("TeamStanding", back_populates="team")

class RaceResult(Base):
    __tablename__ = "race_results"
    __table_args__ = (
        UniqueConstraint('race_id', 'driver_id', name='uq_race_result'),
    )
    
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Data contract columns (required for auto-updater)
    race_id = Column(Integer, ForeignKey('races.race_id'))
    circuit_id = Column(String(100), ForeignKey('circuits.circuit_id'))
    driver_id = Column(String(100), ForeignKey('drivers.driver_id'))
    team_id = Column(String(100), ForeignKey('teams.team_id'))
    grid_position = Column(Float)
    finish_position = Column(Float)
    points_scored = Column(Float)
    race_date = Column(Date)
    weather_condition = Column(String(50))  # "dry", "wet", "mixed"
    
    # Additional columns for backward compatibility
    position_text = Column(String(10))
    laps_completed = Column(Integer)
    status = Column(String(255))
    time = Column(String(50))
    finished = Column(Boolean)
    dnf = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    race = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    team = relationship("Team", back_populates="results")
    circuit = relationship("Circuit")

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    weather_id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey('races.race_id'))
    temperature = Column(Numeric(5, 2))
    humidity = Column(Integer)
    rainfall = Column(Numeric(5, 2))
    wind_speed = Column(Numeric(5, 2))
    conditions = Column(String(100))
    forecast_time = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    race = relationship("Race")

class Prediction(Base):
    __tablename__ = "predictions"
    
    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey('races.race_id'))
    predicted_winner_id = Column(String(100), ForeignKey('drivers.driver_id'))
    confidence_score = Column(Numeric(5, 2))
    predicted_top_3 = Column(String)  # JSON string
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    race = relationship("Race")
    predicted_winner = relationship("Driver", back_populates="predictions")

class DriverStanding(Base):
    __tablename__ = "driver_standings"
    
    standing_id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    driver_id = Column(String(100), ForeignKey('drivers.driver_id'))
    position = Column(Integer)
    points = Column(Numeric(6, 2))
    wins = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    driver = relationship("Driver", back_populates="driver_standings")

class TeamStanding(Base):
    __tablename__ = "team_standings"
    
    standing_id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    team_id = Column(String(100), ForeignKey('teams.team_id'))
    position = Column(Integer)
    points = Column(Numeric(6, 2))
    wins = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    team = relationship("Team", back_populates="team_standings")