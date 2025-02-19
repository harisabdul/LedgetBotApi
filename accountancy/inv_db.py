from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .acc_db import Base, engine, sessionmaker # Assuming Base is defined elsewhere

class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description



def create_brand(name, description):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if account group already exists
    existing_brand = session.query(Brand).filter_by(name=name).first()
    
    if existing_brand is None:
        brand = Brand(name, description)
        session.add(brand)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Brand '{name}' already exists.")




class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name


def create_category(name):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if account group already exists
    existing_item = session.query(Category).filter_by(name=name).first()
    
    if existing_item is None:
        category = Category(name)
        session.add(category)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Category '{name}' already exists.")


class SubCategory(Base):
    __tablename__ = 'sub_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)

    def __init__(self, name, category_id=None):
        self.name = name
        self.category_id = category_id

def create_sub_category(name, category_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    # Check if account group already exists
    existing_item = session.query(SubCategory).filter_by(name=name, category_id=category_id).first()
    
    if existing_item is None:
        sub_category = SubCategory(name, category_id)
        session.add(sub_category)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Handle exception if necessary
    else:
        print(f"Sub Category '{name}' already exists.")

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)
    quantity = Column(Integer, nullable=True)
    fifo_value = Column(Float, nullable=True)
    lifo_value = Column(Float, nullable=True)
    weighted_average_value = Column(Float, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=True)
    batch_number = Column(String(50), nullable=True)

    def __init__(self, product_id, quantity, fifo_value=None, lifo_value=None, weighted_average_value=None, last_updated=None, batch_number=None):
        self.product_id = product_id
        self.quantity = quantity
        self.fifo_value = fifo_value
        self.lifo_value = lifo_value
        self.weighted_average_value = weighted_average_value
        self.last_updated = last_updated
        self.batch_number = batch_number


class BaseUnit(Base):
    __tablename__ = 'base_unit'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(String(50), nullable=False) 
    symbol_qty = Column(Float, nullable=False)

    def __init__(self, name, symbol, symbol_qty):
        self.name = name
        self.symbol = symbol
        self.symbol_qty = symbol_qty

class UnitDetails(Base):
    __tablename__ = 'unit_details'
    id = Column(Integer, primary_key=True)
    bas_unit_id = Column(Integer, ForeignKey('base_unit.id'), nullable=False)
    unit_name = Column(String(50), nullable=False)
    base_unit_qty = Column(Float, nullable=False)

    def __init__(self, base_unit_id, unit_name, base_unit_qty):
        self.base_unit_id = base_unit_id
        self.unit_name = unit_name
        self.base_unit_qty = base_unit_qty


class Supplier(Base):
    __tablename__ = 'supplier' 
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(150), nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(50), nullable=True)
    gstin = Column(String(50), nullable=True)
    trn = Column(String(50), nullable=True)
    pan = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    registration_type = Column(String(50), nullable=True)
    registration_ref = Column(String(50), nullable=True)
    credit_limit = Column(Float, nullable=True)
    credit_days = Column(Integer, nullable=True)
    date_created = Column(DateTime, default=datetime.now(), nullable=True)
    date_updated = Column(DateTime, default=datetime.now(), nullable=True)

    def __init__(self, name, address=None, phone=None, email=None, gstin=None, trn=None, pan=None, is_active=True, registration_type=None, registration_ref=None, credit_limit=None, credit_days=None, date_created=None, date_updated=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.gstin = gstin
        self.trn = trn
        self.pan = pan
        self.is_active = is_active
        self.registration_type = registration_type
        self.registration_ref = registration_ref
        self.credit_limit = credit_limit
        self.credit_days = credit_days
        self.date_created = date_created
        self.date_updated = date_updated

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(150), nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(50), nullable=True)
    gstin = Column(String(50), nullable=True)
    trn = Column(String(50), nullable=True)
    pan = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    registration_type = Column(String(50), nullable=True)
    registration_ref = Column(String(50), nullable=True)
    credit_limit = Column(Float, nullable=True)
    credit_days = Column(Integer, nullable=True)
    date_created = Column(DateTime, default=datetime.now(), nullable=True)
    date_updated = Column(DateTime, default=datetime.now(), nullable=True)

    def __init__(self, name, address=None, phone=None, email=None, gstin=None, trn=None, pan=None, is_active=True, registration_type=None, registration_ref=None, credit_limit=None, credit_days=None, date_created=None, date_updated=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.gstin = gstin
        self.trn = trn
        self.pan = pan
        self.is_active = is_active
        self.registration_type = registration_type
        self.registration_ref = registration_ref
        self.credit_limit = credit_limit
        self.credit_days = credit_days
        self.date_created = date_created
        self.date_updated = date_updated


class GSTDetails(Base):
    __tablename__ = 'gst_details'
    id = Column(Integer, primary_key=True)
    gst_percentage = Column(Float, nullable=True)
    cgst_percentage = Column(Float, nullable=True)
    sgst_percentage = Column(Float, nullable=True)
    igst_percentage = Column(Float, nullable=True)
    hsn_code = Column(String(50), nullable=True)

    def __init__(self, gst_percentage, cgst_percentage=None, sgst_percentage=None, igst_percentage=None, hsn_code=None):
        self.gst_percentage = gst_percentage
        self.cgst_percentage = cgst_percentage
        self.sgst_percentage = sgst_percentage
        self.igst_percentage = igst_percentage
        self.hsn_code = hsn_code


class VATDetails(Base):
    __tablename__ = 'vat_details'
    id = Column(Integer, primary_key=True)
    hsn_code = Column(String(50), nullable=True)
    vat_percentage = Column(Float, nullable=True)

    def __init__(self, hsn_code, vat_percentage):
        self.hsn_code = hsn_code
        self.vat_percentage = vat_percentage



class BatchDetails(Base):
    __tablename__ = 'batch_details'
    id = Column(Integer, primary_key=True)
    batch_number = Column(String(50), nullable=True)
    manufacture_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)
    quantity = Column(Integer, nullable=True)

class CostingDetails(Base):
    __tablename__ = 'costing_details'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)
    raw_material_requirement = Column(Text, nullable=True)
    labor_requirement = Column(Float, nullable=True)
    machine_hour_requirement = Column(Float, nullable=True)
    overheads = Column(Float, nullable=True)
    activity_based_cost = Column(Float, nullable=True)
    standard_cost = Column(Float, nullable=True)

class LicenseDetails(Base):
    __tablename__ = 'license_details'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=True)
    license_number = Column(String(100), nullable=True)
    issuing_authority = Column(String(100), nullable=True)
    expiry_date = Column(DateTime, nullable=True)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    cost = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(150), nullable=True)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=True)
    sub_category_id = Column(Integer, ForeignKey('sub_category.id'), nullable=True)
    tax_percentage = Column(Float, nullable=True)
    item_code = Column(String(50), nullable=True)
    qr_code = Column(String(50), nullable=True)
    hsn_code = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    expiry_period_days = Column(Integer, nullable=True)
    warranty_period_days = Column(Integer, nullable=True)
    extra_charges = Column(Float, nullable=True)
    extra_charges_description = Column(String(150), nullable=True)
    reference_details = Column(String(150), nullable=True)
    reference_number = Column(String(100), nullable=True)  # IMEI, serial number, etc.
    base_unit_id = Column(Integer, ForeignKey('base_unit.id'), nullable=True)
    box_unit = Column(Integer, ForeignKey('unit_details.id'), nullable=True)
    carton_unit = Column(Integer, ForeignKey('unit_details.id'), nullable=True)
    pallet_unit = Column(Integer, ForeignKey('unit_details.id'), nullable=True)
    tax_type = Column(String(150), nullable=True)
    vat = Column(Integer, ForeignKey('vat_details.id'), nullable=True)
    gst = Column(Integer, ForeignKey('gst_details.id'), nullable=True)


    def __init__(self, name, category_id, cost, price, description=None, brand_id=None, sub_category_id=None, tax_percentage=None, item_code=None, qr_code=None, hsn_code=None, is_active=True, expiry_period_days=None, warranty_period_days=None, extra_charges=None, extra_charges_description=None, reference_details=None, reference_number=None, base_unit_id=None, box_unit=None, carton_unit=None, pallet_unit=None, tax_type=None, vat=None, gst=None):
        self.name = name
        self.category_id = category_id
        self.cost = cost
        self.price = price
        self.description = description
        self.brand_id = brand_id
        self.sub_category_id = sub_category_id
        self.tax_percentage = tax_percentage
        self.item_code = item_code
        self.qr_code = qr_code
        self.hsn_code = hsn_code
        self.is_active = is_active
        self.expiry_period_days = expiry_period_days
        self.warranty_period_days = warranty_period_days
        self.extra_charges = extra_charges
        self.extra_charges_description = extra_charges_description
        self.reference_details = reference_details
        self.reference_number = reference_number
        self.base_unit_id = base_unit_id
        self.box_unit = box_unit
        self.carton_unit = carton_unit
        self.pallet_unit = pallet_unit
        self.tax_type = tax_type
        self.vat = vat
        self.gst = gst


class InventoryMovement(Base):
    __tablename__ = 'inventory_movement'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(String(50), nullable=False)
    movement_date_time = Column(DateTime, default=datetime.now(), nullable=False)
    batch_number = Column(String(50), nullable=True)
    reference_number = Column(String(50), nullable=True)
    reference_details = Column(String(150), nullable=True)
    from_location = Column(String(150), nullable=True)
    to_location = Column(String(150), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=True)
    paid = Column(Boolean, default=False, nullable=True)
    payment_date = Column(DateTime, nullable=True)

    def __init__(self, product_id, quantity, movement_type, batch_number=None, reference_number=None, reference_details=None, from_location=None, to_location=None, is_active=True, supplier_id=None, customer_id=None, paid=False, payment_date=None):
        self.product_id = product_id
        self.quantity = quantity
        self.movement_type = movement_type
        self.batch_number = batch_number
        self.reference_number = reference_number
        self.reference_details = reference_details
        self.from_location = from_location
        self.to_location = to_location
        self.is_active = is_active
        self.supplier_id = supplier_id
        self.customer_id = customer_id
        self.paid = paid
        self.payment_date = payment_date

