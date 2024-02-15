from .models import Profile
from django import forms
from PIL import Image

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'banner', 'bio']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            # Check if the uploaded file is an image
            try:
                img = Image.open(image)
                img.verify()  # This will throw an error if the file is not an image
            except Exception as e:
                raise forms.ValidationError("Invalid image file.")

            # Check if the image format is allowed
            allowed_formats = ('JPEG', 'PNG')
            if img.format not in allowed_formats:
                raise forms.ValidationError("Unsupported image format. Only JPEG and PNG are allowed.")

        return image