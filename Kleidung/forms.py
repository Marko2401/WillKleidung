from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Listing, ListingImage, Message, Review, UserProfile


class UserRegistrationForm(UserCreationForm):
    """Registrierungsformular für neue Benutzer"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-Mail Adresse'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Vorname'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nachname'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Benutzername'
        })
    )
    password1 = forms.CharField(
        label="Passwort",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Passwort'
        })
    )
    password2 = forms.CharField(
        label="Passwort bestätigen",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Passwort wiederholen'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Diese Email-Adresse wird bereits verwendet.')
        return email


class UserProfileForm(forms.ModelForm):
    """Formular für Benutzerprofile"""
    class Meta:
        model = UserProfile
        fields = ['biography', 'profile_picture', 'location', 'phone']
        widgets = {
            'biography': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Erzähle etwas über dich...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stadt/Ort'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefonnummer (optional)'
            }),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ListingForm(forms.ModelForm):
    """Formular zum Erstellen/Bearbeiten von Angeboten"""
    
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'size', 'price', 'brand', 'color', 'material', 'condition', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Artikel-Titel (z.B. Blauer Pullover von H&M)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Beschreibe den Zustand, die Herkunft und besondere Merkmale...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Preis in €',
                'step': '0.01',
                'min': '0.01'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marke (z.B. H&M, Zara, Vintage)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Farbe (z.B. Blau, Schwarz-weiß gestreift)'
            }),
            'material': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Material (z.B. 100% Baumwolle, Baumwolle-Mix)'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stadt/Ort für Haushalt'
            }),
        }


class ListingImageForm(forms.ModelForm):
    """Formular für Bilder zu Angeboten"""
    class Meta:
        model = ListingImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class MessageForm(forms.ModelForm):
    """Formular für Nachrichten"""
    class Meta:
        model = Message
        fields = ['subject', 'text']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Betreff (optional)',
                'maxlength': 200
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deine Nachricht...'
            }),
        }


class ReviewForm(forms.ModelForm):
    """Formular für Bewertungen"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optionaler Kommentar zu dieser Bewertung...'
            }),
        }


class SearchForm(forms.Form):
    """Suchformular für Angebote"""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nach Kleidung suchen...'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min. Preis',
            'step': '0.01',
            'min': '0'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max. Preis',
            'step': '0.01',
            'min': '0'
        })
    )
    condition = forms.ChoiceField(
        required=False,
        choices=[('', 'Alle Zustände')] + Listing.CONDITION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ort/Stadt'
        })
    )
    sort_by = forms.ChoiceField(
        initial='-created_at',
        choices=[
            ('-created_at', 'Neueste zuerst'),
            ('price', 'Preis: Aufsteigend'),
            ('-price', 'Preis: Absteigend'),
            ('-views', 'Beliebteste'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    

