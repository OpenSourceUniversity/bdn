from ajax_select import register, LookupChannel
from .models import Skill


@register('skills')
class SkillLookup(LookupChannel):

    model = Skill

    def get_query(self, query, request):
        return self.model.objects.filter(name__icontains=query)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
