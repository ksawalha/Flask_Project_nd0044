from flask import Blueprint, render_template,request,flash,redirect,url_for
from forms import *
from models import (Venue,db)
import sys
from app import datetime,dateutil


venues_bp = Blueprint('venues_bp', __name__, template_folder='templates',static_folder='static', static_url_path='assets')


@venues_bp.route('/')
def venues():
 data = []
    queried_venues = Venue.query.distinct(Venue.state, Venue.city,).all()
    for queried_venue in queried_venues:
        location = {
            "state": queried_venue.state,
            "city":  queried_venue.city,
        }
        venues = Venue.query.filter_by(state=queried_venue.state,city=queried_venue.city).all()
     
        venue_location = []
        for venue in venues:
            new_venue={}
            new_venue['id'] = venue.id
            new_venue['name']= venue.name
            new_venue['num_upcoming_shows'] = len(venue.shows)
            venue_location.append(new_venue)
        location["venues"] = venue_location
        data.append(location)
    return render_template('pages/venues.html', areas=data);


@venues_bp.route('/<int:venue_id>')
def show_venue(venue_id):
 
  venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  upcoming_shows_count = 0
  past_shows_count = 0
  present_time =  dateutil.parser.parse(str(datetime.now()))

  for show in venue.shows:
    if dateutil.parser.parse(show.start_time) > present_time:
      upcoming_shows_details={}
      upcoming_shows_details['artist_id'] = show.artist_id
      upcoming_shows_details['artist_name'] = show.artist.name
      upcoming_shows_details['artist_image_link'] = show.artist.image_link
      upcoming_shows_details['start_time'] = show.start_time
      upcoming_shows.append(upcoming_shows_details)
      upcoming_shows_count += 1               
    elif dateutil.parser.parse(show.start_time) < present_time:
      past_shows_details={}
      past_shows_details['artist_id'] = show.artist_id
      past_shows_details['artist_name'] = show.artist.name
      past_shows_details['artist_image_link'] = show.artist.image_link
      past_shows_details['start_time'] = show.start_time
      past_shows.append(past_shows_details)
      past_shows_count += 1
                

  data={
    "id": venue.id,
    "name": venue.name,
    "genres":venue.genres.split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
    "upcoming_shows": upcoming_shows,
     "past_shows": past_shows
   
  }
  return render_template('pages/show_venue.html', venue=data)


@venues_bp.route('/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@venues_bp.route('/create', methods=['POST'])
def create_venue_submission():

    error = False
    try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website_link = request.form['website_link']
      genres =','.join(request.form.getlist('genres')) 
      seeking_talent = True if request.form.get('seeking_talent') == 'y' else False 
      seeking_description = request.form['seeking_description']


      new_venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website_link=website_link,genres=genres, seeking_talent=seeking_talent,seeking_description=seeking_description)
    
      db.session.add(new_venue)
      db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(error)
        print(sys.exc_info())
    finally:
        db.session.close()
        if error
            flash('An error occured. Venue ' + request.form['name'] + ' Could not be listed!')
        else:   
            
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


@venues_bp.route('/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):

    venue = Venue.query.get(venue_id)
    try:
      db.session.delete(venue)
      db.session.commit()
      flash(f'Venue was deleted successfully')
    except:
      db.session.rollback()
      flash(f'There was an error while delteing venue')
    finally:
      db.session.close()

    return render_template('pages/home.html')

@venues_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venue_info=Venue.query.get(venue_id)
  venue={
    "id": venue_info.id,
    "name":venue_info.name,
    "city": venue_info.city,
    "state": venue_info.state,
    "genres": venue_info.genres,
    "phone": venue_info.phone,
    "website_link": venue_info.website_link,
    "facebook_link": venue_info.facebook_link,
    "image_link": venue_info.image_link,
    "seeking_talent":venue_info.seeking_talent,
    "seeking_description": venue_info.seeking_description
  }
  form = VenueForm(obj=venue_info)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@venues_bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  error = False
  try:  
    venue.name = request.form['name']
    venue.genres = request.form['genres']
    venue.state = request.form['state']
    venue.city = request.form['city']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.website_link = request.form['website_link']
    venue.facebook_link = request.form['facebook_link']
    venue.seeking_talent =  True if request.form.get('seeking_talent') == 'y' else False 
    venue.seeking_description = request.form['seeking_description']
    venue.image_link= request.form['image_link']
    db.session.commit()
  except:
   error = True
   db.session.rollback()
  finally:
   db.session.close()
  if error:
     flash("Oops....Something isn't right")
  else:
    flash("Venue " + request.form['name'] + " was edited succesfully")
  return redirect(url_for('show_venue', venue_id=venue_id))
