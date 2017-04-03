from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Members(db.Model):
	__tablename__='Members'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	dfaps = db.Column(db.Float)
		
	def AddMember(self, Member):
		tmpMembers = Members()
		tmpMembers.name = Member
		db.session.add(tmpMembers)
		db.session.commit()
		
	def GetAllMembers(self):
		return Members.query.order_by(Members.name).all()
	
	def GetMember(self, Member):
		return Members.query.filter_by(name=Member).first()
		
	def UpdateMember(self, Member, DFAPs, Increment):
		Member = Members.query.filter_by(name=Member).first()
		if Member and DFAPs:
			if Increment and Member.dfaps:
				Member.dfaps = float(Member.dfaps) + float(DFAPs)
			else:
				Member.dfaps = float(DFAPs)
			db.session.commit()
	
class StoreItems(db.Model):
	__tablename__='StoreItems'
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Integer)
	cost = db.Column(db.Float)
	donatedby = db.Column(db.Text)
	dateadded = db.Column(db.DateTime)
	items_id = db.Column(db.Integer, db.ForeignKey('Items.id'))
	addedby_member_id = db.Column(db.Integer, db.ForeignKey('Members.id'))
	
class CartItems(db.Model):
	__tablename__='CartItems'
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Integer)
	dateadded = db.Column(db.DateTime)
	datefulfilled = db.Column(db.DateTime)
	member_id = db.Column(db.Integer, db.ForeignKey('Members.id'))
	storeitem_id = db.Column(db.Integer, db.ForeignKey('Items.id'))
	fulfilledby_member_id = db.Column(db.Integer, db.ForeignKey('Members.id'))
	
class Items(db.Model):
	__tablename__='Items'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Integer)
	notes = db.Column(db.Text)
	image_id = db.Column(db.Integer, db.ForeignKey('Images.id'))

class Images(db.Model):
	__tablename__='Images'
	id = db.Column(db.Integer, primary_key=True)
	image = db.Column(db.LargeBinary)	
