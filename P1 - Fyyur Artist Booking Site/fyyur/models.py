#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
#Many to Many relationship (association table) for Shows
class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    upcoming = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
      return f'<Shows {self.id}>'

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # Done: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String()))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(300))
    website_link = db.Column(db.String(500))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    artists = db.relationship('Artist', secondary=Shows, backref=db.backref('Venue'))

    def __repr__(self):
      return f'<Venue {self.id}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # Done: implement any missing fields, as a database migration using Flask-Migrate
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(300))
    website_link = db.Column(db.String(500))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    venues = db.relationship('Venue', secondary=Shows, backref='Artist')

    def __repr__(self):
      return f'<Artist {self.id}>'
# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration. 