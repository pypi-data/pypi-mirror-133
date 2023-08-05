from django import forms
from .config import get_bleach_default_options
from bleach import clean

class SanitizedCharField(forms.CharField):
    def __init__(self, f_name=None, f_error = None,
                allowed_tags=None, strip_comments=None, strip_tags=None,
                *args, **kwargs,
            ):
        self.f_name = f_name
        self.f_error = f_error
        self.bleach_kwargs = get_bleach_default_options()
        if allowed_tags:
            self.bleach_kwargs["tags"] = allowed_tags
        if strip_comments:
            self.bleach_kwargs["strip_comments"] = strip_comments
        if strip_tags:
            self.bleach_kwargs["strip"] = strip_tags
        super(SanitizedCharField, self).__init__(*args, **kwargs)

    def get_error_message(self):
        if self.f_error:
            return self.f_error
        elif self.f_name:
            return f"Please enter valid {' '.join(self.f_name.split('_'))}."
        return "Please enter valid text for this field."

    def clean(self, value):
        data = super(SanitizedCharField, self).clean(value)
        if data is None:
            return data
        cleaned_data = clean(data, **self.bleach_kwargs)
        if not cleaned_data and self.required:
            raise forms.ValidationError(self.get_error_message())
        return cleaned_data

class SanitizedTextField(forms.CharField):
    def __init__(self, f_name=None, f_error = None,
                allowed_tags=None, strip_comments=None, strip_tags=None,
                *args, **kwargs,
            ):
        self.f_name = f_name
        self.f_error = f_error
        self.bleach_kwargs = get_bleach_default_options()
        if allowed_tags:
            self.bleach_kwargs["tags"] = allowed_tags
        if strip_comments:
            self.bleach_kwargs["strip_comments"] = strip_comments
        if strip_tags:
            self.bleach_kwargs["strip"] = strip_tags
        super(SanitizedTextField, self).__init__(*args, **kwargs)

    def get_error_message(self):
        if self.f_error:
            return self.f_error
        elif self.f_name:
            return f"Please enter valid {' '.join(self.f_name.split('_'))}."
        return "Please enter valid text for this field."

    def clean(self, value):
        data = super(SanitizedTextField, self).clean(value)
        if data is None:
            return data
        cleaned_data = clean(data, **self.bleach_kwargs)
        if not cleaned_data and self.required:
            raise forms.ValidationError(self.get_error_message())
        return cleaned_data