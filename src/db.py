from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for declarative models
Base = declarative_base()

# Define the User model corresponding to the users table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    p1 = Column(Integer)
    p2 = Column(Integer)
    q1 = Column(Integer)
    q2 = Column(Integer)
    dang = Column(Integer)
    khab = Column(Integer)
    t1 = Column(Integer)
    t2 = Column(Integer)

    def __repr__(self):
        return (f"<User(id={self.id}, p1={self.p1}, p2={self.p2}, "
                f"q1={self.q1}, q2={self.q2}, dang={self.dang}, "
                f"khab={self.khab}, t1={self.t1}, t2={self.t2})>")
    

# Create an SQLite database engine
engine = create_engine('sqlite:///sample.db')
Base.metadata.create_all(engine)  # Create the table if it doesn't exist

# Create a session
Session = sessionmaker(bind=engine)

# def create_database():
#     # This function is not needed as the table is created with Base.metadata.create_all
#     pass

def insert_user_data(id, user_data):
    session = Session()
    new_user = User(id=id, **{key: value for key, value in zip(['p1', 'p2', 'q1', 'q2', 'dang', 'khab', 't1', 't2'], user_data)})
    session.add(new_user)
    session.commit()
    session.close()

def update_user_data(id, element, value):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    
    if user:
        setattr(user, element, value)
        session.commit()
    session.close()

def get_user_info_by_id(id, requested_fields):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    
    if user:
        result = {field: getattr(user, field) for field in requested_fields if hasattr(user, field)}
        session.close()
        return result
    session.close()
    return None

def get_element(id, element):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    
    if user and hasattr(user, element):
        result = getattr(user, element)
        session.close()
        return result
    session.close()
    return None

def delete_user_by_id(id):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    
    if user:
        session.delete(user)
        session.commit()
    session.close()

def check_user_exists(id):
    session = Session()
    exists = session.query(User).filter(User.id == id).count() > 0
    session.close()
    return exists