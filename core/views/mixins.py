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


class BreadcrumbsMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.set_breadcrumbs()
        return context

    def set_breadcrumbs(self):
        pass


class BasePageMixin:
    titolo = ""
    sottotitolo = ""

    def get_titolo_pagina(self):
        return self.titolo

    def get_sottotitolo_pagina(self, **context):
        return self.sottotitolo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = self.get_titolo_pagina()
        context['sottotitolo'] = self.get_sottotitolo_pagina(**context)
        return context


class ListMixin:
    count_context_name = 'objects_count'

    def get_objects_count(self, object_list=None, **kwargs):
        if object_list is not None:
            count = object_list.count()
        else:
            count = self.object_list.count()
        return count

    def get_objects_count_display(self, **kwargs):
        return '[{}]'.format(self.get_objects_count(**kwargs))

    def get_context_data(self, object_list=None, **context):
        context = super().get_context_data(object_list=object_list, **context)
        context[self.count_context_name] = self.get_objects_count_display(object_list=object_list)
        return context


class PageMixin(BreadcrumbsMixin, BasePageMixin):

    def set_breadcrumbs(self):
        super().set_breadcrumbs()
        self.request.breadcrumbs.add(self.get_titolo_pagina())


class PageListMixin(PageMixin, ListMixin):

    def get_sottotitolo_pagina(self, **context):
        if self.count_context_name in context:
            return context[self.count_context_name]
        return super().get_sottotitolo_pagina(**context)
