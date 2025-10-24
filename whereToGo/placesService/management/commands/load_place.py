import json
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from placesService.models import Place, Image


class Command(BaseCommand):
    help = 'Loads a single Place from a URL containing a JSON structure.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The URL of the JSON file to load.')

    def handle(self, *args, **options):
        url = options['url']
        self.stdout.write(self.style.NOTICE(f'Downloading data from: {url}'))

        try:
            response = requests.get(url)
            response.raise_for_status()
            place_data = response.json()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Failed to download or parse JSON: {e}'))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Invalid JSON format: {e}'))
            return

        title = place_data.get('title')
        if not title:
            self.stderr.write(self.style.ERROR('JSON is missing the "title" field. Aborting.'))
            return

        place, created = Place.objects.update_or_create(
            title=title,
            defaults={
                'description_short': place_data.get('description_short', ''),
                'description_long': place_data.get('description_long', ''),
                'latitude': place_data.get('coordinates', {}).get('lat'),
                'longitude': place_data.get('coordinates', {}).get('lng'),
            }
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} Place: {place.title}'))

        place.images.all().delete()

        image_urls = place_data.get('imgs', [])

        for index, img_url in enumerate(image_urls):
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()

                img_name = img_url.split('/')[-1]

                image = Image.objects.create(
                    place=place,
                    sort_order=index
                )

                image.file.save(img_name, ContentFile(img_response.content), save=True)
                self.stdout.write(self.style.SUCCESS(f'  - Image {index + 1} loaded: {img_name}'))

            except requests.RequestException as e:
                self.stderr.write(self.style.WARNING(f'  - Could not load image {img_url}: {e}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Import finished for {place.title}.'))