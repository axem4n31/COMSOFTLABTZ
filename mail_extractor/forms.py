from django.forms import ModelForm

from mail_extractor.models import Mail


class MailForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"
