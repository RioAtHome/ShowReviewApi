import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from shows.models import Show, Review, Comment, Favorites, Character, Season, Episode 
 


@pytest.mark.django_db
def test_shows_view(fake_data):
    client = APIClient()
    resp = client.get(reverse('get_all_shows'))
    test_keys = set(['show', 'seasons', 'reviews', 'characters', 'network', 'created_at', 'updated_at'])

    for show in resp.data:
        assert test_keys.issubset(show.keys())
    assert resp.status_code == 200
    


@pytest.mark.django_db
@pytest.mark.parametrize('client, method', [
    (APIClient().post, "POST"),
    (APIClient().get, "GET"),
    (APIClient().put, "PUT"),
    (APIClient().delete, "DELETE"),
    (APIClient().patch, "PATCH")
    ])
@pytest.mark.parametrize('show', ['breaking-bad', 'better-call-saul'])
def test_show_view(fake_data, get_user, client, method, show):
    headers = {"HTTP_JWT": get_user['JWT']}
    if method == "POST":
        desired_show = Show.objects.filter(show=show).first()
        data = {'network':"amc", 'air_date':'1999-3-5', "end_date":'2022-3-4'}
        resp = client(reverse('show', kwargs={"show_name": show }), data, **headers, format='json')

        if not desired_show:
            expected_keys = set(["created_at", "updated_at", "show", "network", "air_date", "end_date", "num_of_favorites", "seasons", "reviews", "characters"])
            assert expected_keys.issubset(resp.data['data'].keys())
            assert resp.data["message"] == "Data has been added successfully"
            assert resp.status_code == 201
        else:
            expected_data = "Show With This Show Already Exists."
            assert resp.status_code == 400
            assert resp.data['show'][0].title() == expected_data

    elif method == "GET":
        desired_show = Show.objects.filter(show=show).first()        
        resp = client(reverse('show', kwargs={"show_name": show }), format='json')
       
        if desired_show:
            
            expected_keys = set(["created_at", "updated_at", "show", "network", "air_date", "end_date", "num_of_favorites", "seasons", "reviews", "characters"])
            assert expected_keys.issubset(resp.data['show'].keys())
            assert resp.status_code == 200
        else:
            assert resp.data["detail"].title() == "Not Found."
            assert resp.status_code == 404
    elif method == "PATCH":
        desired_show = Show.objects.filter(show=show).first()
        if desired_show:
            show_network = Show.objects.filter(show=show).first().network
            updated_ = Show.objects.filter(show=show).first().updated_at
            data = {'network':"fox"}
            resp = client(reverse('show', kwargs={"show_name": show }), data, **headers, format='json')
            
            assert resp.data['message'] == "Data has been updated successfully"
            
            assert resp.status_code == 200

            new_show_network = Show.objects.filter(show=show).first().network
            assert new_show_network != show_network

            new_date = Show.objects.filter(show=show).first().updated_at
            assert new_date != updated_
        else:
            data = {'network':"fox"}
            resp = client(reverse('show', kwargs={"show_name": show }), data, **headers, format='json')
            
            assert resp.status_code == 404
            assert resp.data["detail"].title() == "Not Found."
    elif method == "DELETE":
        desired_show = Show.objects.filter(show=show).first()        
        resp = client(reverse('show', kwargs={"show_name": show }), format='json')
       
        if desired_show:     
            deleted_show = Show.objects.filter(show=show).first()
            assert deleted_show is None
            assert resp.status_code == 200
        else:
            assert resp.data["detail"].title() == "Not Found."
            assert resp.status_code == 404
    else:
        resp = client(reverse('show', kwargs={"show_name": show}), )

        assert resp.status_code == 405


@pytest.mark.django_db
@pytest.mark.parametrize('client, method', [
    (APIClient().post, "POST"),
    (APIClient().get, "GET"),
    (APIClient().put, "PUT"),
    (APIClient().delete, "DELETE"),
    ])
@pytest.mark.parametrize('show', ['breaking-bad', 'better-call-saul'])
@pytest.mark.parametrize('season_num', [1, 3])
def test_season_view(fake_data, get_user, client, method, show, season_num):
    headers = {"HTTP_JWT": get_user['JWT']}
    if method == "POST":
        desired_season = Season.objects.filter(show=show, season_num=season_num).first()
        desired_show = Show.objects.filter(show=show).first()
        data = {'season_num':3}
        
        resp = client(reverse('season', kwargs={"show_name": show, "season_num":season_num }), data, **headers, format='json')
        
        if not desired_season and desired_show:
            
            assert resp.data["message"] == "Data has been added successfully"
            assert resp.status_code == 201
        else:
            assert resp.status_code == 400
    elif method == "GET":
        desired_season = Season.objects.filter(show=show, season_num=season_num).first()        
        resp = client(reverse('season', kwargs={"show_name": show, "season_num":season_num}), format='json')
       
        if desired_season:
            assert resp.status_code == 200
        else:
            assert resp.data["detail"].title() == "Not Found."
            assert resp.status_code == 404
    elif method == "DELETE":
        desired_season = Season.objects.filter(show=show, season_num=season_num).first()        
        resp = client(reverse('season', kwargs={"show_name": show, "season_num":season_num}), format='json')
       
        if desired_season:     
            deleted_Season = Season.objects.filter(show=show, season_num=season_num).first()
            assert deleted_Season is None
            assert resp.status_code == 200
        else:
            assert resp.data["detail"].title() == "Not Found."
            assert resp.status_code == 404
    else:
        resp = client(reverse('season', kwargs={"show_name": show, "season_num":season_num}), )

        assert resp.status_code == 405

@pytest.mark.django_db
@pytest.mark.parametrize('client, method', [
    (APIClient().post, "POST"),
    (APIClient().get, "GET"),
    (APIClient().put, "PUT"),
    (APIClient().delete, "DELETE"),
    (APIClient().patch, "PATCH")
    ])
@pytest.mark.parametrize('show', ['breaking-bad', 'better-call-saul'])
@pytest.mark.parametrize('char', ['jesse', 'saul'])
def test_character_view(fake_data, get_user, client, method, show, char):
    headers = {"HTTP_JWT": get_user['JWT']}
    if method == "POST":
        desired_Character = Character.objects.filter(show=show, name=char).first()
        show = Show.objects.filter(show=show).first()
        data = {'age':25, 'gender':'F', 'status':'D'}
        resp = client(reverse('character', kwargs={"show_name": show, "char_name":char}), data, **headers, format='json')
        if not desired_Character and show:
            expected_keys = set(["created_at", "updated_at", "show", "name", "age", "gender", "status"])
            assert expected_keys.issubset(resp.data['data'].keys())
            assert resp.data["message"] == "Data has been added successfully"
            assert resp.status_code == 201
        else:
            assert resp.status_code == 400

    elif method == "GET":
        desired_character = Character.objects.filter(show=show, name=char).first()        
        resp = client(reverse('character', kwargs={"show_name": show, "char_name":char}), format='json')
       
        if desired_character:
            assert resp.status_code == 200
        else:
            assert resp.data["detail"].title() == "Not Found."
            assert resp.status_code == 404
    elif method == "PATCH":
        desired_character = Character.objects.filter(show=show, name=char).first()
        if desired_character:
            character_age = Character.objects.filter(show=show, name=char).first().age
            updated_ = Character.objects.filter(show=show, name=char).first().updated_at
            data = {'age':"35"}
            resp = client(reverse('character', kwargs={"show_name": show,"char_name":char}), data, **headers, format='json')
            
            assert resp.data['message'] == "Data has been updated successfully"
            
            assert resp.status_code == 200

            new_character_age = Character.objects.filter(show=show, name=char).first().age
            assert new_character_age != character_age

            new_date = Character.objects.filter(show=show, name=char).first().updated_at
            assert new_date != updated_
        else:
            data = {'age':30}
            resp = client(reverse('character', kwargs={"show_name": show, "char_name":char}), data, **headers, format='json')
            
            assert resp.status_code == 404
            assert resp.data["detail"].title() == "Not Found."
    elif method == "DELETE":
        desired_character = Character.objects.filter(show=show, name=char).first()        
        resp = client(reverse('character', kwargs={"show_name": show, "char_name":char }), **headers, format='json')
       
        if desired_character:     
            deleted_character = Character.objects.filter(show=show, name=char).first()
            assert deleted_character is None
            assert resp.status_code == 200
        else:
            assert resp.data["detail"].title() == "Not Found."
            assert resp.status_code == 404

    else:
        resp = client(reverse('character', kwargs={"show_name": show, "char_name":char}), )

        assert resp.status_code == 405


@pytest.mark.django_db
def test_favorite_view(fake_data, get_user):
    show_favorites = Show.objects.filter(show='breaking-bad').first().num_of_favorites
    client = APIClient()

    headers = {"HTTP_JWT": get_user["JWT"]}
    resp = client.post(reverse('favorite', kwargs={'show_name': 'breaking-bad'}), **headers)

    new_show_favorites = Show.objects.filter(show='breaking-bad').first().num_of_favorites

    assert resp.status_code == 201
    assert new_show_favorites == show_favorites + 1

