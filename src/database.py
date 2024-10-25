from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from models.product import Base, Product, ProductResponse
import os
import psycopg

class Database:

    def __init__(self):
        # docker file system path
        load_dotenv("/app/.env")
        password = os.getenv('POSTGRES_PASSWORD')

        self.engine = create_engine(f'postgresql+psycopg://admin:{password}@postgres')

        # database existence check
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'marketplace'")).fetchone()

            if not result:
                # outside of transaction 
                conn = psycopg.connect(dbname='postgres', user='admin', password=password, host='postgres')
                conn.autocommit = True
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE marketplace")
                cursor.close()
                conn.close()
                print("База данных 'marketplace' создана.")
            else:
                print("База данных 'marketplace' уже существует.")

        self.engine = create_engine(f'postgresql+psycopg://admin:{password}@postgres/marketplace')

        # create tables
        Base.metadata.create_all(self.engine)

    def getAllProducts(self, category, name, max_price, min_price, amount, currency):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            query = session.query(Product)

            if name is not None:
                query = query.filter(Product.name.like(f"%{name}%"))
            if category is not None:
                query = query.filter(Product.category.like(f"%{category}%"))
            if min_price is not None:
                query = query.filter(Product.cost >= min_price)
            if max_price is not None:
                query = query.filter(Product.cost <= max_price)
            if amount is not None:
                query = query.filter(Product.amount == amount)
            if currency is not None:
                 query = query.filter(Product.currency.like(f"%{currency}%"))

            products = query.all()
            return products

    def getProduct(self, id):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            product = session.query(Product).get(id)
            return product

    def addProduct(self, category, name, amount, cost, currency):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            product = Product(category=category, name=name, amount=amount, cost=cost, currency=currency)

            existing_product = session.query(Product).filter_by(id=product.id).first()

            if existing_product is not None:
                raise Exception("The product already exists!")

            session.merge(product)
            session.commit()
            return product
        
    def addProducts(self, products: list[ProductResponse]):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:

            added = []
            errors = 0
            for product in products:
                result = Product(product.category, product.name, product.amount, product.cost, product.currency)
                existing_product = session.query(Product).filter_by(id=result.id).first()

                if existing_product is not None:
                    added.append({ "message": "The product already exists", "product": product})
                    errors += 1
                    continue
                
                session.merge(result)
                added.append(result.toJSON())
            
            session.commit()
            return (added, errors)
        
    def deleteProducts(self, ids: list[str]):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:

            deleted = []
            errors = 0
            for id in ids:
                delete = session.query(Product).filter_by(id=id).first()

                if delete is None:
                    deleted.append({ "message": "The product does not exist", "id": id})
                    errors += 1
                    continue
                
                session.delete(delete)
                deleted.append(delete.toJSON())
            
            session.commit()
            return (deleted, errors)

    def deleteProduct(self, id):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            search = session.query(Product).filter_by(id=id).first()
            session.delete(search)
            session.commit()
            return search

    def updateProduct(self, id, category, name, amount, cost, currency):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            updatable = session.query(Product).filter_by(id=id).first()

            updatable.category = category
            updatable.name = name
            updatable.amount = amount
            updatable.cost = cost
            updatable.currency = currency

            updatable.refresh()

            session.merge(updatable)
            session.commit()
            session.refresh(updatable)

            return updatable
