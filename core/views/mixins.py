class FilteredQuerysetMixin:
    filter_class = None

    def get_filter_obj(self, initial=None):
        if initial is None:
            initial = self.request.GET
        if self.filter_class is not None:
            return self.filter_class(initial, queryset=self.get_queryset())
        else:
            return None

    def get_context_data(self, **kwargs):
        filters = self.get_filter_obj()
        if filters is not None:
            kwargs['object_list'] = filters.qs
            kwargs['filter'] = filters
        return super().get_context_data(**kwargs)
