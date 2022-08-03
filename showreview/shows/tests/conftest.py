import pytest
from shows.models import Show, Review, Comment, Favorites, Character, Season, Episode 



@pytest.fixture
def fake_data():

    breaking_bad = Show(show='breaking-bad', network='amc', air_date='2008-3-4', end_date='2013-2-3')
    the_boys = Show(show='the-boys', network='amazon', air_date='2018-3-4')
    futurama = Show(show='futurama', network='fox', air_date='2000-3-4', end_date='2015-2-3')

    breaking_bad.save()
    the_boys.save()
    futurama.save()

    Character(show=breaking_bad, name="jesse", age=25, gender='M', status='A').save()
    Character(show=breaking_bad, name="walter", age=55, gender='M', status='D').save()

    Character(show=the_boys, name="homelander", age=35, gender='M', status='A').save()
    Character(show=the_boys, name="butcher", age=40, gender='M', status='A').save()

    Character(show=futurama, name="bender", age=14, gender='M', status='A').save()
    Character(show=futurama, name="leela", age=14, gender='F', status='A').save()

    b1 = Season(show=breaking_bad, season_num=1)
    b2 = Season(show=breaking_bad, season_num=2)

    f1 = Season(show=futurama, season_num=1)
    f2 = Season(show=futurama, season_num=2)

    t1 = Season(show=the_boys, season_num=1)
    t2 = Season(show=the_boys, season_num=2)
    
    b1.save()
    b2.save()

    f1.save()
    f2.save()

    t1.save()
    t2.save()

    Episode(show=breaking_bad, season=b1, title="Pilot", epi_num=1, release_date='2008-2-4').save() 
    Episode(show=breaking_bad, season=b2, title="OHH, meth", epi_num=1, release_date='2009-2-4').save()
    
    
    Episode(show=futurama, season=f1, title="Pilot 3000", epi_num=1, release_date='2000-4-6').save()    
    Episode(show=futurama, season=f2, title="In the year 3000", epi_num=1, release_date='2001-4-5').save()
    

    Episode(show=the_boys, season=t1, title="Sthsthtest", epi_num=1, release_date='2018-5-6').save()    
    Episode(show=the_boys, season=t2, title="OHH, another test title", epi_num=1, release_date='2019-5-6').save()
    
    r1 = Review(id='1', username="rioathome", show=breaking_bad, text="Amazing show, wow ggs and all")

    r2 = Review(id='2', username="rio", show=the_boys, text="Good show buddy")

    r3 = Review(id='3', username="oday", show=futurama, text="Maybe fox's only good cartoon")

    r1.save()
    r2.save()
    r3.save()


    Comment(username='rioathome', show=futurama, review=r2, text='Great review rio').save()
    Comment(username='rioathome', show=the_boys, review=r3, text='Great review oday').save()

    Comment(username='rio', show=breaking_bad, review=r1, text='Great review rioathome').save()
    Comment(username='rio', show=the_boys, review=r3, text='Great review oday').save()

    Comment(username='oday', show=breaking_bad, review=r1, text='Great review rioathome').save()
    Comment(username='oday', show=futurama, review=r2, text='Great review rio').save()

    Favorites(username='rioathome', show=breaking_bad).save()
    Favorites(username='rioathome', show=the_boys).save()
    
    Favorites(username='rio', show=the_boys).save()
    Favorites(username='rio', show=futurama).save()
    
    Favorites(username='oday', show=futurama).save()
    Favorites(username='oday', show=breaking_bad).save()


@pytest.fixture
def get_user():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c3IiOiJyaW9hdGhvbWUiLCJyb2wiOjEsImlhdCI6MTUxNjIzOTAyMn0.w54V6HrRfTfuOININNPWSVZfNkcHuw5yc6kztAUnDGQ"
    data = {"username": "rioathome", "JWT": token, "role": 1}


    return data
