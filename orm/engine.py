from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:Roussanto171!@localhost:3306/income",
    pool_pre_ping=True
)
