from django.shortcuts import render, redirect, get_object_or_404
from PIL.ExifTags import TAGS, GPSTAGS
from .models import Point
from .forms import PointForm
from django.http import JsonResponse
from PIL import Image
from geopy.geocoders import Nominatim
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


def google_auth_view(request):
    # Debug information
    print(f"Number of Google social apps: {SocialApp.objects.filter(provider='google').count()}")

    # Check Sites configuration
    print("Sites configuration:")
    for site in Site.objects.all():
        print(f"Site ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

    # Check Social App to Site relationships
    google_app = SocialApp.objects.get(provider='google')
    print("\nSocial App Sites:")
    for site in google_app.sites.all():
        print(f"Site ID: {site.id}, Domain: {site.domain}")

    # Add context
    context = {
        'google_app': google_app,
        'site': Site.objects.get(id=2)
    }

    return render(request, "google_auth.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")


def check_geotag(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        img = Image.open(image)
        geotag = get_geotag_data(img)

        if geotag:
            lat, lon = get_coordinates(geotag)

            # Reverse geocoding to get city and state
            geolocator = Nominatim(user_agent="geoapp")
            location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True)

            if location and location.raw.get('address'):
                address = location.raw['address']
                city = address.get('city') or address.get('town') or address.get('village', '')
                state = address.get('state', '')
            else:
                city = ''
                state = ''

            return JsonResponse({
                'geotag_found': True,
                'latitude': lat,
                'longitude': lon,
                'city': city,
                'state': state
            })
        else:
            return JsonResponse({'geotag_found': False})

    return JsonResponse({'geotag_found': False})


def get_geotag_data(image):
    """Extract geotag data from an image."""
    info = image._getexif()
    if not info:
        return None

    geotag = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                geotag[sub_decoded] = value[t]

    return geotag

def get_coordinates(geotag):
    """Convert geotag to latitude and longitude."""
    def to_decimal(values, ref):
        d, m, s = values
        result = d + (m / 60.0) + (s / 3600.0)
        if ref in ['S', 'W']:
            result = -result
        return result

    lat = to_decimal(geotag.get('GPSLatitude'), geotag.get('GPSLatitudeRef'))
    lon = to_decimal(geotag.get('GPSLongitude'), geotag.get('GPSLongitudeRef'))
    return lat, lon

@login_required
def add_point(request):
    if request.method == 'POST':
        form = PointForm(request.POST, request.FILES)

        if form.is_valid():
            point = form.save(commit=False)

            # Set geolocation based on user input or marker
            geolocation = request.POST.get('geolocation', '')
            point.geolocation = geolocation

            # Only save without checking geotag since that has already been done
            point.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Form validation failed.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def index(request):
    points = Point.objects.all()
    form = PointForm()
    return render(request, 'points/index.html', {'form': form, 'points': points})

@login_required
def show_points(request):
    points = Point.objects.all()
    points_data = [
        {
            'id': point.id,
            'geolocation': point.geolocation,
            'date': point.date.strftime('%Y-%m-%d'),
            'city': point.city,
            'state': point.state,
            'length': point.length,
            'width': point.width,
            'fire_status': point.fire_status,
            'image': point.image.url if point.image else ''
        }
        for point in points
    ]
    return JsonResponse(points_data, safe=False)

@login_required
def delete_point(request, point_id):
    if request.method == 'POST':
        point = get_object_or_404(Point, id=point_id)
        point.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})