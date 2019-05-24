from app import app, db
import datetime

class Resource(db.Model):
    """
    Class to represent the resource model
    """
    __tablename__ = 'resources'

    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_link = db.Column(db.Text, nullable=False)
    resource_status = db.Column(db.String(255), nullable=False)
    resource_categories = db.Column(db.Text, nullable=True)
    resource_created_on = db.Column(db.DateTime, nullable=False)
    resource_updated_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, link, categories, status):
        self.resource_link = link
        self.resource_categories = categories
        self.resource_status = status
        self.resource_created_on = datetime.datetime.utcnow()
        self.resource_updated_on = datetime.datetime.utcnow()

    def save(self):
        """
        Persist an resource in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self, an_resource):
        """
        Update some resource data
        :param an_resource: resource
        :return:
        """

        self.resource_link = an_resource.resource_link if an_resource.resource_link else self.resource_link
        self.resource_categories = an_resource.resource_categories if an_resource.resource_categories else self.resource_categories
        self.resource_status = an_resource.resource_status if an_resource.resource_status else self.resource_status
        self.resource_updated_on = datetime.datetime.utcnow()

        db.session.commit()

    def delete(self):
        """
        Delete an resource from the database
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
        Json representation of the resource model.
        :return:
        """
        return {
            'id': self.resource_id,
            'link': self.resource_link,
            'categories': self.resource_categories,
            'status': self.resource_status,
            'created_on': self.resource_created_on.isoformat(),
            'modified_on': self.resource_updated_on.isoformat()
        }