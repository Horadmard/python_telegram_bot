from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for declarative models
Base = declarative_base()

# Define the User model corresponding to the users table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    stu_num = Column(Integer)
    lname = Column(String)
    fname = Column(String)
    dis_code = Column(String)

    def __repr__(self):
        return (f"<User(id={self.id}, stu_num={self.stu_num}, lname={self.lname}, fname={self.fname}, "
                f"dis_code={self.dis_code})>")
    

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
    new_user = User(id=id, **{key: value for key, value in zip(['stu_num', 'lname', 'fname', 'dis_code'], user_data)})
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