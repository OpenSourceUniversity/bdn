from haystack import indexes
from .models import Profile


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    full_name = indexes.CharField(model_attr='full_name', null=True)
    full_name_auto = indexes.EdgeNgramField(
        model_attr='full_name', null=True)

    academy_name = indexes.CharField(model_attr='academy_name', null=True)
    academy_name_auto = indexes.EdgeNgramField(
        model_attr='academy_name', null=True)

    company_name = indexes.CharField(model_attr='company_name', null=True)
    company_name_auto = indexes.EdgeNgramField(
        model_attr='company_name', null=True)

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
