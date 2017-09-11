from django import template
from django.template.loader import get_template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def uikit_form(form, *args, **kwargs):
    # from blog.form import RegisterForm
    # form = RegisterForm()
    rendered_fields = []
    for field in form:
        rendered_fields.append(render_field(field))

    return mark_safe(render_error(form) + '\n'.join(rendered_fields))


def render_field(field):
    # widget = field.field.widget
    # initial_attrs = widget.attrs.copy()
    # classes = widget.attrs.get('class', '')
    # print(widget)
    # print(initial_attrs)
    # print(classes)
    # print(field)
    # print(field.label_tag())

    return wrap_form_row(field.label_tag(attrs={'class': 'uk-form-label'}) + wrap_form_controls(field.as_widget()))


def render_error(form):
    form_errors = get_fields_errors(form) + form.non_field_errors()
    template = get_template('blog/form_errors.html')
    return template.render({'errors': form_errors})


def get_fields_errors(form):
    form_errors = []
    for field in form:
        if not field.is_hidden and field.errors:
            form_errors += field.errors
    return form_errors


def wrap_form_controls(html):
    return '<div class="uk-form-controls">{}</div>'.format(html)


def wrap_form_row(html):
    return '<div class="uk-form-row">{}</div>'.format(html)


def text_value(value):
    """
    Force a value to text, render None as an empty string
    """
    if value is None:
        return ''
    return force_text(value)


def split_css_classes(css_classes):
    """
    Turn string into a list of CSS classes
    """
    classes_list = text_value(css_classes).split(' ')
    return [c for c in classes_list if c]


def add_css_class(css_classes, css_class, prepend=False):
    """
    Add a CSS class to a string of CSS classes
    """
    classes_list = split_css_classes(css_classes)
    classes_to_add = [c for c in split_css_classes(css_class)
                      if c not in classes_list]
    if prepend:
        classes_list = classes_to_add + classes_list
    else:
        classes_list += classes_to_add
    return ' '.join(classes_list)
