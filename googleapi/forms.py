from django import forms


class OauthForm(forms.Form):
    # token_field= forms.CharField()
    json_uploader=forms.FileField()
