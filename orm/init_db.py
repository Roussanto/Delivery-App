from engine import engine
from model import Base
from sqlalchemy import select
from sqlalchemy.orm import Session

from orm.model import Offer

Base.metadata.create_all(engine)

# Add the 4 different types of offers
with Session(engine) as session:
    Offer_1 = Offer(description="None", cost=0)
    Offer_2 = Offer(description="coffee, toast, fresh orange juice", cost=5.5)
    Offer_3 = Offer(description="coffee, soft cookie, water", cost=4)
    Offer_4 = Offer(description="coffee, bagel, mini donut", cost=4.3)

    session.add(Offer_1)
    session.add(Offer_2)
    session.add(Offer_3)
    session.add(Offer_4)

    session.commit()
