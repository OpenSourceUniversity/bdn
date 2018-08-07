from haystack import indexes
from bdn.course.models import Skill


class SkillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    name_auto = indexes.EdgeNgramField(model_attr='name')
    standardized = indexes.BooleanField(model_attr='standardized')

    def get_model(self):
        return Skill

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
