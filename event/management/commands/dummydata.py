from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from random import randint
from datetime import datetime
from collections import defaultdict

from event.models.main import Event
from event.models.page import Page, SECTION_CLASSES

from loremipsum import get_sentence, get_paragraph

def get_word():
    return get_sentence().split(' ')[0]

class Command(BaseCommand):
    # args = 'numRegistrations [--reset]'
    help = 'Create dummy event data using lorem ipsum generator'

    option_list = BaseCommand.option_list + (
        make_option('--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Delete all event data before generating new data.'),
        )

    def handle(self, *args, **options):

        if options['reset']:
            Event.objects.all().delete()

        event = Command.create_event()
        page = Command.create_page(event)
        Command.create_sections(page)

        self.stdout.write('Successfully generated dummy data')

    @staticmethod
    def create_event(**kwargs):
        event = Event.objects.create(
            is_active = True,
            start_date = datetime.strptime('Sep 24 2016 9:00AM', '%b %d %Y %I:%M%p'),
            end_date = datetime.strptime('Sep 25 2016 8:00PM', '%b %d %Y %I:%M%p'),
            title = 'Dummy event',
            city = 'Montreal',
            country = 'Canada',
            )
        return event

    @staticmethod
    def create_page(event, **kwargs):
        page = Page.objects.create(
            event = event,
            title = 'Dummy main page',
            )
        return page

    @staticmethod
    def random_section_data(page, section_type, **kwargs):
        section_templates = defaultdict(lambda: 'section.html')
        section_templates.update({
            'cover': 'header.html',
            'about': 'about.html',
            'perks': 'perks.html',
            
            'venue': 'venue.html'
        })
        data = {
            'page': page,
            'is_visible': True,
            'template': section_templates[section_type],

        }
        return data

    @staticmethod
    def create_sections(page, **kwargs):
        sections = []

        for section_class in SECTION_CLASSES:
            data = Command.random_section_data(page, section_class.SECTION_TYPE)
            section_class.objects.create(**data)


    @staticmethod
    def generate_registrations(n, **kwargs):
        charge_attempt = ChargeAttempt.objects.create(
                    email = 'default@charge.com',
                    charge_id = 'ch_xxx',
                    is_livemode = False,
                    is_paid = False,
                    status = 'None',
                    amount = 0,
                    source_id = 'tok_xxx',
                    is_captured = False,
                    failure_message = '',
                    failure_code = 'dummy_code'
                )
        for i in range(n):
            Registration.objects.create(**Command.generate_registration_data(**kwargs))

    @staticmethod
    def generate_challenges(n, **kwargs):
        for i in range(n):
            Challenge.objects.create(
                encrypted_message = get_sentence(),
                decrypted_message = get_sentence(),
            )

    @staticmethod
    def generate_registration_data(max_length=300):
        # add random hashtags
        data =  {
            'first_name':  get_word(), 
            'last_name':  get_word(), 
            'school': 'McGill University',
            'email': '@'.join([get_word(), get_word() + '.com']),
            'is_first_time_hacker': bool(randint(0, 1)),
            'is_returning': bool(randint(0, 1))
            }
        return data