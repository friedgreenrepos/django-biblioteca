from django import template
from django.utils.safestring import mark_safe
from django.forms import widgets

register = template.Library()

@register.filter(name='render')
def render(field):
    out = []
    required_class = ''
    required_mark = ''
    out.append('<div id="field-{0}" class="form-group">'.format(field.id_for_label))
    if field.field.required:
        required_class = 'required-field '
        #required_mark = '*' # asterisco viene messo via css
    if isinstance(field.field.widget, widgets.CheckboxInput):
        out.append('<label class="{required_class} custom-control custom-checkbox">{field} <span class="custom-control-indicator"></span> <span class="custom-control-description">{label} {required_mark}</span></label>'.format(**{
            'field': field.as_widget(attrs={'class': "custom-control-input"}),
            'label': field.label,
            'required_class': required_class,
            'required_mark': required_mark,
        }))
    elif ('readonly' in field.field.widget.attrs) and isinstance(field.field.widget, widgets.Select):
        out.append('<label for="{id}" class="{required_class}">{label} {required_mark}</label>{field}'.format(**{
            'id': field.id_for_label,
            'label': field.label,
            'field': field.as_widget(attrs={'disabled': 'disabled'}),
            'required_class': required_class,
            'required_mark': required_mark,
        }))
        out.append(field.as_hidden())
    elif isinstance(field.field.widget, widgets.FileInput):
        out.append('<label for="{id_for_label}" class="{required_class}">{label} {required_mark}'.format(**{
            'id_for_label': field.id_for_label,
            'label': field.label,
            'required_class': required_class,
            'required_mark': required_mark,
        }))
        out.append(field.as_widget())
        if field.initial:
            out.append('<a href="{}" class="btn btn-default"><i class="fa fa-download"></i>Scarica</a>'.format(field.initial.url))
        out.append('</label>')
    elif isinstance(field.field.widget, widgets.HiddenInput):
        out.append('{}'.format(field.as_widget()))
    else:
        out.append('<label for="{id}" class="{required_class}">{label} {required_mark}</label>{field}'.format(**{
            'id': field.id_for_label,
            'label': field.label,
            'field': field.as_widget(),
            'required_class': required_class,
            'required_mark': required_mark,
        }))
    if field.help_text:
        out.append('<div class="small">{0}</div>'.format(field.help_text))
    if field.errors:
        out.append('<div class="text-danger"><ul>')
        for error in field.errors:
            out.append('<li>%s</li>' % error)
        out.append('</ul></div>')
    out.append('</div>')
    return mark_safe(''.join(out))
