from django import forms
__all__ = ['BootstrapForm']


class BootstrapForm(forms.Form):
    ''' A simple Form to apply bootstrap classes to widgets.
    '''
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            name = field.widget.__class__.__name__.lower()
            if not name.startswith("radio") and not name.startswith("checkbox") and not name == 'fileinput':
                try:
                    classes = field.widget.attrs['class'].split(' ')
                    classes.append('form-control')
                    field.widget.attrs['class'] = ' '.join(set(classes))
                except KeyError:
                    field.widget.attrs['class'] = 'form-control'
