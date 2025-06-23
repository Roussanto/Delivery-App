from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:Roussanto171!@localhost:3306/income_dummy",
    pool_pre_ping=True
)

Session = sessionmaker(bind=engine)
session = Session()

