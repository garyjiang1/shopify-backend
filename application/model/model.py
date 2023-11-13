from application import db

class Has(db.Model):
    __tablename__ = 'has'

    w_id = db.Column(db.ForeignKey('warehouse.id'), primary_key=True)
    i_id = db.Column(db.ForeignKey('inventory.id'), primary_key=True)
    amount = db.Column(db.Integer)
    
    def __init__(self, w_id, i_id, amount):
        self.w_id = w_id
        self.i_id = i_id
        self.amount = amount

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.String(200))
    capacity = db.Column(db.Integer, nullable=False)
    current_load = db.Column(db.Integer)
    #inventories = db.relationship("Inventory", secondary=has, backref=db.backref("warehouse", lazy="joined"))
    created_time = db.Column(db.DateTime)
    updated_time = db.Column(db.DateTime)
    
    def __init__(self, name, address, capacity, created_time, current_load):
        self.name = name
        self.address = address
        self.capacity = capacity
        self.created_time = created_time
        self.updated_time = created_time
        self.current_load = current_load
    
    holds = db.relationship('Inventory', secondary='has', lazy='subquery',
        backref=db.backref('warehouse', lazy=True))

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    not_allocated = db.Column(db.Integer, nullable=False)
    updated_time = db.Column(db.DateTime)
    
    def __init__(self, name, price, amount, updated_time):
        self.name = name
        self.price = price
        self.amount = amount
        self.not_allocated = amount
        self.updated_time = updated_time
    