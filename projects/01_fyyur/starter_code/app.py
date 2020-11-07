#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (Flask, 
                  render_template,
                  request,
                  Response, 
                  flash, 
                  redirect, 
                  url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, FlaskForm
from forms import *
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import distinct
import datetime
from models import app, db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# TODO: connect to a local postgresql database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


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

    result = []

    try:
        locations = db.session.query(distinct(Venue.city), Venue.state).all()

        for location in locations:
            city = location[0]
            state = location[1]

            location_info = {"city": city, "state": state, "venues": []}

            venues = Venue.query.filter_by(city=city, state=state).all()

            for venue in venues:
                venue_name = venue.name
                venue_id = venue.id

                venue_data = {
                    "id": venue_id,
                    "name": venue_name
                }

                location_info["venues"].append(venue_data)

            result.append(location_info)
    
    except:
        db.session.rollback()
        flash("Something went wrong. Please try again.")
        return render_template("pages/home.html")

    finally:
        return render_template("pages/venues.html", areas=result)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    
    search = request.form.get("search_term", "")
    search_result = {"count": 0, "data": []}

    venue_id_name = ["id", "name"]
    venue_search_results = (db.session.query(Venue).filter(Venue.name.ilike(f"%{search}%")).options(load_only(*venue_id_name)).all())

    search_result["count"] = len(venue_search_results)

    for result in venue_search_results:
        venue_id_name = {
            "id": result.id,
            "name": result.name,
        }
        search_result["data"].append(venue_id_name)

    return render_template("pages/search_venues.html", results=search_result, search_term=request.form.get("search_term", ""))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  profile_data = []
  query = db.session.query(   Show, Venue,
                              Artist.id.label("artist_id"),
                              Artist.name.label("artist_name"),
                              Artist.image_link.label("artist_image_link")
                              ).join(Venue).filter(Venue.id==venue_id).join(Artist).group_by(Show.id, Artist.id,Venue.id,).all()  
  if query:
        genres = split_genres((query[0].Venue.genres))
        profile_data = {
                  "id": venue_id ,
                  "name": query[0].Venue.name ,
                  "genres": genres ,
                  "city": query[0].Venue.city ,
                  "state":query[0].Venue.state ,
                  "phone":query[0].Venue.phone ,
                  "facebook_link": query[0].Venue.facebook_link ,
                  "image_link":query[0].Venue.image_link ,
                  }

        upcoming_shows = []
        past_shows = []
        for d in query:
            if datetime.datetime.today() > d.Show.start_time:
                    show = {
                                "artist_id": d.artist_id ,
                                "artist_name": d.artist_name ,
                                "artist_image_link": d.artist_image_link ,
                                "start_time": str(d.Show.start_time)
                                }
                    past_shows.append(show)             
                        
            elif  datetime.datetime.today() <= d.Show.start_time:
                    show = {
                                "artist_id": d.artist_id ,
                                "artist_name": d.artist_name ,
                                "artist_image_link": d.artist_image_link ,
                                "start_time": str(d.Show.start_time)
                                }
                    upcoming_shows.append(show) 
                    
        profile_data["past_shows_count"] = len(past_shows)
        profile_data["upcoming_shows_count"] = len(upcoming_shows)                
        profile_data["past_shows"] = past_shows
        profile_data["upcoming_shows"] = upcoming_shows
        return render_template('pages/show_venue.html', venue=profile_data)
  else:
     query = db.session.query(Venue).filter(Venue.id == venue_id).all()
     genres = split_genres((query[0].genres))
     profile_data = {
                  "id": venue_id,
                  "name": query[0].name,
                  "genres": genres,
                  "city": query[0].city,
                  "state":query[0].state,
                  "phone":query[0].phone,
                  "address" :query[0].address,
                  "facebook_link": query[0].facebook_link,
                  "image_link":query[0].image_link ,
                  "upcoming_shows_count" : 0 ,
                  "past_shows_count" : 0   
                  }  
  return render_template('pages/show_venue.html', venue=profile_data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  venue_info={}
   
  try:
     #get data from request.form
    venue_info={'name' :request.form["name"]}
    #crete object of an artisi model 
    new_venue = Venue( name = request.form["name"] , 
                   city = request.form["city"] ,
                   state= request.form[ "state"],
                   phone=request.form["phone"],
                   address=request.form["address"],
                   genres =request.form.getlist("genres"),
                   image_link= request.form["image_link"],
                   facebook_link= request.form["facebook_link"]
                  )
    db.session.add(new_venue)
    db.session.commit()
  except :
    error = True
    db.session.rollback()
  finally:
    if error:
      # abort (400)
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + venue_info['name'] + ' could not be listed.')
    else:
    # on successful db insert, flash success
      flash('Venue ' + venue_info['name'] + ' was successfully listed!')
    db.session.close()
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


@app.route("/venues/<venue_id>/delete")
def delete_venue(venue_id):
    name = Venue.query.get(venue_id).name
    try:
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        db.session.delete(venue)
        db.session.commit()
        flash("Venue " + name + " was deleted successfully")
    except:
        db.session.rollback()
        flash('An error occured. Venue could not be deleted.')
    finally:
        db.session.close()
        return redirect(url_for("index"))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artist_id_name = ["id", "name"]
  artists_info = db.session.query(Artist).options(load_only(*artist_id_name)).all()
  return render_template('pages/artists.html', artists=artists_info)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search= request.form.get("search_term", "")
  search_result = {"count": 0, "data": []}
  artist_id_name = ["id", "name"]

  artist_search = (db.session.query(Artist).filter(Artist.name.ilike(f"%{search}%")).options(load_only(*artist_id_name)).all())
  search_result["count"] = len(artist_search)

  for result in artist_search:
    artist_info = {
      "id": result.id,
      "name": result.name,
      }
    search_result["data"].append(artist_info)


  return render_template('pages/search_artists.html', results=search_result, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  profile_data = []
  query = db.session.query(   Show, Artist,
                              Venue.id.label("venue_id"),
                              Venue.name.label("venue_name"),
                              Venue.image_link.label("venue_image_link")
                              ).join(Artist).filter(Artist.id==artist_id).join(Venue).group_by(Show.id, Artist.id,Venue.id,).all()  
  if query:
        genres = split_genres((query[0].Artist.genres))
        profile_data = {
                  "id": artist_id ,
                  "name": query[0].Artist.name ,
                  "genres": genres ,
                  "city": query[0].Artist.city ,
                  "state": query[0].Artist.state ,
                  "phone": query[0].Artist.phone ,
                  "facebook_link": query[0].Artist.facebook_link ,
                  "image_link": query[0].Artist.image_link , 
                  }
  
        upcoming_shows = []
        past_shows = []
        for d in query:
            if datetime.datetime.today() > d.Show.start_time:
                    show = {
                                "venue_id": d.venue_id ,
                                "venue_name": d.venue_name ,
                                "venue_image_link": d.venue_image_link ,
                                "start_time": str(d.Show.start_time)
                                }
                    past_shows.append(show)             
        
            elif  datetime.datetime.today() <= d.Show.start_time:
                    show = {
                                "venue_id": d.venue_id ,
                                "venue_name": d.venue_name ,
                                "venue_image_link": d.venue_image_link ,
                                "start_time": str(d.Show.start_time)
                                }
                    upcoming_shows.append(show) 

        profile_data["past_shows_count"] = len(past_shows)
        profile_data["upcoming_shows_count"] = len(upcoming_shows)                  
        profile_data["past_shows"] = past_shows
        profile_data["upcoming_shows"] = upcoming_shows  
        return render_template('pages/show_artist.html', artist=profile_data)
  else:
     query = db.session.query(Artist).filter(Artist.id==artist_id).all()
     genres = split_genres((query[0].genres))
     data = {
                  "id": artist_id,
                  "name": query[0].name ,
                  "genres": genres ,
                  "city": query[0].city ,
                  "state": query[0].state ,
                  "phone": query[0].phone ,
                  "facebook_link": query[0].facebook_link,
                  "image_link": query[0].image_link ,
                  "upcoming_shows_count" : 0 ,
                  "past_shows_count" : 0   
                  }  
     return render_template('pages/show_artist.html', artist=data) 

def split_genres(genres_list):
   genres_list = (genres_list).split(",")
   genres=[]
   for genre in genres_list:
              genre =''.join((filter(lambda i: i not in ['{', '"', '\'' , "}" ], genre)))
              genres.append(genre)
   return  genres 




#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    data={}
    try:
      artist = db.session.query(Artist).filter(Artist.id == artist_id).first()

      genres = {}
      genres = split_genres(artist.genres)
      
      form.name.data = artist.name
      form.genres.data = genres
      form.city.data = artist.city
      form.state.data = artist.state
      form.phone.data = artist.phone
      form.facebook_link.data = artist.facebook_link
      form.image_link.data = artist.image_link
      
      data = {
        'id' : artist_id,
        'name' : artist.name
          } 

    except:
      db.session.rollback()
      flash("Something went wrong. Please try again.")
      return redirect(url_for("index"))

    finally:
      db.session.close()
    return render_template("forms/edit_artist.html", form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()

    print(artist)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist("genres")
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    flash("Something went wrong. Please try again.")
    return redirect(url_for("index"))

  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    data={}
    try:
      venue = db.session.query(Venue).filter(Venue.id == venue_id).first()

      genres = {}
      genres = split_genres(venue.genres)
      
      form.name.data = venue.name
      form.genres.data = genres
      form.city.data = venue.city
      form.state.data = venue.state
      form.phone.data = venue.phone
      form.address.data = venue.address
      form.facebook_link.data = venue.facebook_link
      form.image_link.data = venue.image_link
      
      data = {
        'id' : venue_id,
        'name' : venue.name
          } 

    except:
      db.session.rollback()
      flash("Something went wrong. Please try again.")
      return redirect(url_for("index"))

    finally:
      db.session.close()
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()

    print(venue)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.address = request.form['address']
    venue.genres = request.form.getlist("genres")
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    
    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    flash("Something went wrong. Please try again.")
    return redirect(url_for("index"))

  finally:
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: insert form data as a new artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  error = False
  atrist_result={}
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres =request.form.getlist("genres")
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    
    atrist_result = Artist(name=name,city=city,state=state,phone=phone,genres=genres,image_link=image_link,facebook_link=facebook_link)
    db.session.add(atrist_result)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    if error:
      flash('An error occurred. Artist ' + atrist_result.name + ' could not be listed.')
    else:
      flash('Artist ' + atrist_result.name + ' was successfully listed!')
    
    db.session.close()
  return render_template('pages/home.html')




#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    show_data =[]
    show_info = db.session.query(
                            Show.id,
                            Show.start_time,
                            Artist.name.label("artist_name"),
                            Artist.image_link.label("artist_image_link"),
                            Artist.id.label("artist_id"),
                            Venue.id.label("venue_id"),
                            Venue.name.label("venue_name")
                            ).join(Artist).join(Venue).group_by(Show.id, Artist.id,Venue.id,).order_by(Show.id).all()  
    for info in show_info:
        show_info ={
        "Show.id": info.id,
        "start_time":str(info.start_time),
        "artist_id" :info.artist_id ,
        "artist_name" :info.artist_name ,
        "artist_image_link" :info.artist_image_link ,
        "venue_id" : info.venue_id ,
        "venue_name" : info.venue_name ,
          }
        show_data.append(show_info)
    return render_template('pages/shows.html', shows=show_data)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error=False
    artist = request.form['artist_id']
    venue = request.form['venue_id']
    show_start_time = request.form['start_time']
    artist_count = Artist.query.filter(Artist.id == artist).count()
  
    if artist_count > 0:
       venue_count = Venue.query.filter(Venue.id == venue).count()
       if venue_count > 0:
            try:
              new_show = Show(artist_id=artist, venue_id=venue, start_time=show_start_time)
              db.session.add(new_show)
              db.session.commit()      
            except:
              db.session.rollback()
              db.session.close()
              error=True       
            if error:
              flash('An error occurred. Show could not be listed.')
            else: 
              flash('Show was successfully listed!')
            return render_template('pages/home.html')
       else:
          flash('Invalid Venue ID.')
          form = ShowForm()
          return render_template('forms/new_show.html', form=form)  
    else: 
      flash('Invalid Artist ID.')
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)



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
