from . import db

class LineItem(db.Model):
    __tablename__ = 'line_items'

    # Ensure nonnull values for simplicity/safety
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, nullable=False)
    campaign_name = db.Column(db.String(10000), nullable=False)
    line_item_name = db.Column(db.String(10000), nullable=False)
    booked_amount = db.Column(db.Float, nullable=False)
    actual_amount = db.Column(db.Float, nullable=False)
    adjustments = db.Column(db.Float, nullable=False)
