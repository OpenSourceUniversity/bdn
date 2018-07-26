from haystack import indexes
from .models import Job


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Job

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
