from django import forms

from .models import ServiceRequest


MAX_IMAGE_BYTES = 5 * 1024 * 1024


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model  = ServiceRequest
        fields = ('category', 'location', 'description', 'image', 'priority')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue...'}),
            'location':    forms.TextInput(attrs={'placeholder': 'e.g. Tom Mboya St, Nairobi'}),
        }
        labels = {
            'category':    'Issue category',
            'description': 'Describe the issue',
            'image':       'Photo (optional, max 5 MB)',
        }

    def clean_location(self):
        location = self.cleaned_data['location'].strip()
        if len(location) < 3:
            raise forms.ValidationError("Please provide a specific location.")
        return location

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if len(description) < 10:
            raise forms.ValidationError("Please describe the issue in at least 10 characters.")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > MAX_IMAGE_BYTES:
            raise forms.ValidationError("Image must be under 5 MB.")
        return image
