#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, FlaskForm
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Done: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    shows = db.relationship('Shows', backref=db.backref('Venue'), lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
      return f'<Venue {self.id}, {self.name}>'

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
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    shows = db.relationship('Shows', backref=db.backref('Artist'), lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
      return f'<Artist {self.id}, {self.name}>'
    # Done: implement any missing fields, as a database migration using Flask-Migrate
    #Many to Many relationship/association table

class Shows(db.Model):
  __tablename__ = 'Shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False)
  start_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return f'<Shows {self.id}>'
# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Done?: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  places = []
  for venue in Venue.query.distinct(Venue.city).all():
    if venue.city not in places:
      venue_places = Venue.query.filter_by(city = venue.city).all()
      places_dict = {
        'city': venue.city,
        'state': venue.state,
        'venues': venue_places
      }
      data.append(places_dict)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  data = []
  for venue in venues:
    upcoming_shows = 0
    shows = db.session.query(Shows).filter(Shows.venue_id == venue.id)
    for show in shows:
      if (show.start_time > datetime.now()):
        upcoming_shows += 1
    venue_dict = {
      'id': venue.id,
      'name': venue.name,
      'upcoming_shows': upcoming_shows
    }
    data.append(venue_dict)

  response={
    'count': len(venues),
    'data': data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # Done: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  shows = db.session.query(Shows).filter(Shows.venue_id == venue_id)
  past_shows = []
  upcoming_shows = []
  for show in shows:
    artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).one()
    theshow = {
      'artist_id': show.artist_id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': str(show.start_time)
      }

    if (show.start_time < datetime.now()):
      past_shows.append(theshow)
    else:
      upcoming_shows.append(theshow)

  data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.seeking_talent,
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # Done: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  v_id = db.session.query(Venue).filter_by(id=venue_id).one()
  to_delete = v_id
  try:
    db.session.delete(to_delete)
    db.session.commit()
    flash('Venue sucessfully deleted!')
  except:
    db.session.rollback()
    flash('Venue could not be deleted.')
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Done: insert form data as a new Venue record in the db, instead
  # Done: modify data to be the data object returned from db insertion
  error = False

  new_venue = Venue()
  new_venue.name = request.form['name']
  new_venue.city = request.form['city']
  new_venue.state = request.form['state']
  new_venue.address = request.form['address']
  new_venue.phone = request.form['phone']
  new_venue.facebook_link = request.form['facebook_link']
  new_venue.genres = request.form.getlist('genres')
  new_venue.website = request.form['website']
  new_venue.image_link = request.form['image_link']
  new_venue.seeking_talent = True if 'seeking_talent' in request.form else False
  new_venue.seeking_description = request.form['seeking_description']
  try:
    db.session.add(new_venue)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    flash('There was a problem adding this Venue, please try again.')
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  edit_venue = Venue.query.filter_by(id=venue_id).one()
  form.name.data = edit_venue.name
  form.city.data = edit_venue.city
  form.state.data = edit_venue.state
  form.phone.data = edit_venue.phone
  form.genres.data = edit_venue.genres
  form.image_link.data = edit_venue.image_link
  form.facebook_link.data = edit_venue.facebook_link
  form.website.data = edit_venue.website
  form.seeking_talent.data = edit_venue.seeking_talent
  form.seeking_description.data = edit_venue.seeking_description

  # Done: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=edit_venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # Done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  facebook_link = request.form['facebook_link']
  genres = request.form.getlist('genres')
  website = request.form['website']
  image_link = request.form['image_link']
  seeking_talent = True if 'seeking_talent' in request.form else False
  seeking_description = request.form['seeking_description']
  
  try:
    edit_venue = Venue.query.filter_by(id=venue_id).one()
  
    edit_venue.name = name
    edit_venue.city = city
    edit_venue.state = state
    edit_venue.address = address
    edit_venue.phone = phone
    edit_venue.genres = genres
    edit_venue.image_link = image_link
    edit_venue.facebook_link = facebook_link
    edit_venue.website = website
    edit_venue.seeking_talent = seeking_talent
    edit_venue.seeking_description = seeking_description

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('Unable to update Venue!')
  finally:
    db.session.close()
    flash('Venue was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Done: replace with real data returned from querying the database
  artists = Artist.query.all()

  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%'+search_term+'%')).all()
  data = []
  for artist in artists:
    upcoming_shows = 0
    shows = db.session.query(Shows).filter(Shows.artist_id == artist.id)
    for show in shows:
      if (show.start_time > datetime.now()):
        upcoming_shows += 1
    artist_dict = {
      'id': artist.id,
      'name': artist.name,
      'upcoming_shows': upcoming_shows,
    }
    data.append(artist_dict)
  response ={
    'count': len(artists),
    'data': data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given aritst_id
  # Done: replace with real artist data from the artists table, using artist_id
  artist = Artist.query.get(artist_id)
  shows = db.session.query(Shows).filter(Shows.artist_id == artist_id)
  past_shows = []
  upcoming_shows = []
  for show in shows:
    venue = db.session.query(Venue.name, Venue.image_link).filter(Venue.id == show.venue_id).one()
    theshow = {
      'venue_id': show.venue_id,
      'venue_name': venue.name,
      'venue_image_link': venue.image_link,
      'start_time': str(show.start_time)
      }

    if (show.start_time < datetime.now()):
      past_shows.append(theshow)
    else:
      upcoming_shows.append(theshow)

  data = {
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  edit_artist = Artist.query.filter_by(id=artist_id).one()
  form.name.data = edit_artist.name
  form.city.data = edit_artist.city
  form.state.data = edit_artist.state
  form.phone.data = edit_artist.phone
  form.genres.data = edit_artist.genres
  form.image_link.data = edit_artist.image_link
  form.facebook_link.data = edit_artist.facebook_link
  form.website.data = edit_artist.website
  form.seeking_venue.data = edit_artist.seeking_venue
  form.seeking_description.data = edit_artist.seeking_description

  # Done: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=edit_artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Done: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  facebook_link = request.form['facebook_link']
  genres = request.form.getlist('genres')
  website = request.form['website']
  image_link = request.form['image_link']
  seeking_venue = True if 'seeking_venue' in request.form else False
  seeking_description = request.form['seeking_description']
  
  try:
    edit_artist = Artist.query.filter_by(id=artist_id).one()
  
    edit_artist.name = name
    edit_artist.city = city
    edit_artist.state = state
    edit_artist.phone = phone
    edit_artist.genres = genres
    edit_artist.image_link = image_link
    edit_artist.facebook_link = facebook_link
    edit_artist.website = website
    edit_artist.seeking_venue = seeking_venue
    edit_artist.seeking_description = seeking_description

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('Unable to update Artist!')
  finally:
    db.session.close()
    flash('Artist was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # done: insert form data as a new Venue record in the db, instead
  # done: modify data to be the data object returned from db insertion
  error = False

  new_artist = Artist()
  new_artist.name = request.form['name']
  new_artist.city = request.form['city']
  new_artist.state = request.form['state']
  new_artist.phone = request.form['phone']
  new_artist.facebook_link = request.form['facebook_link']
  new_artist.genres = request.form.getlist('genres')
  new_artist.website = request.form['website']
  new_artist.image_link = request.form['image_link']
  new_artist.seeking_venue = True if 'seeking_venue' in request.form else False
  new_artist.seeking_description = request.form['seeking_description']
  try:
    db.session.add(new_artist)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    flash('There was a problem adding this Artist, please try again.')
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # Done: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = db.session.query(Venue.name, Artist.name, Artist.image_link, Shows.venue_id, Shows.artist_id, Shows.start_time)\
    .filter(Venue.id==Shows.venue_id, Artist.id==Shows.artist_id)
  for show in shows:
    show_dict = {
      'venue_name': show[0],
      'artist_name': show[1],
      'artist_image_link': show[2],
      'venue_id': show[3],
      'artist_id': show[4],
      'start_time': str(show[5])
    }
    data.append(show_dict)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # Done: insert form data as a new Show record in the db, instead
  error = False
  show = Shows()
  show.artist_id = request.form.get('artist_id')
  show.venue_id = request.form.get('venue_id')
  show.start_time = request.form.get('start_time')
  try:
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('Error! Show was not created.')
  finally:
    db.session.close()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''