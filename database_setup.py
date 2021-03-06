from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    item = relationship('Item', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'name': self.name,
                'id': self.id,
                'user_id': self.user_id
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_name = Column(String, ForeignKey('category.name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # price = Column(String(8))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
               'name': self.name,
               'description': self.description,
               'id': self.id,
               # 'price': self.price,
               'category_name': self.category_name,
               'user_id': self.user_id
        }


engine = create_engine('sqlite:///catalog1.db')

Base.metadata.create_all(engine)
