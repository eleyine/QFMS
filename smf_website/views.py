from django.views import generic
# from event.assets import Person, Sponsor, Workshop, Prize
from event.models.main import Event
from event.models.page import Section, SECTION_CLASSES
from collections import defaultdict

class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        event = Event.objects.first()
        page = event.pages.first()
        context['event'] = event
        context['page'] = page
        context['sections'] = page.get_sections()
        
        # Add in a QuerySet of all persons
        # context['judges'] = Person.objects.filter(category='J').all()
        # context['mentors'] = Person.objects.filter(category='M').all()

        # context['workshops'] = Workshop.objects.all()
        # context['prizes'] = Prize.objects.all()
        
        # # Add sponsors
        # context['sponsors'] = defaultdict(list)
        # for sponsor in Sponsor.objects.all():
        #     category = sponsor.get_category_display().lower().replace(' ', '_')
        #     context['sponsors'][category].append(sponsor)
        return context