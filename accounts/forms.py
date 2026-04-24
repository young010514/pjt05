from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms import ModelForm

from community.utils import load_assets

from .models import CustomUser


class SignUpForm(UserCreationForm):
    nickname = forms.CharField(max_length=50, label="닉네임")
    profile_image = forms.ImageField(required=False, label="프로필 이미지")
    interest_stocks = forms.MultipleChoiceField(
        required=False,
        label="관심 종목",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "password1",
            "password2",
            "nickname",
            "profile_image",
            "interest_stocks",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "아이디"
        self.fields["password1"].label = "비밀번호"
        self.fields["password2"].label = "비밀번호 확인"
        self.fields["interest_stocks"].choices = [
            (asset["id"], asset["name"])
            for asset in load_assets()
            if asset.get("id") and asset.get("name")
        ]

        for field_name in ("username", "password1", "password2", "nickname"):
            self.fields[field_name].widget.attrs["class"] = "form-input"

        self.fields["profile_image"].widget.attrs["class"] = "form-input form-input-file"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nickname = self.cleaned_data["nickname"]
        user.profile_image = self.cleaned_data.get("profile_image")
        user.interest_stocks = self.cleaned_data.get("interest_stocks", [])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="아이디")
    password = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": "아이디 또는 비밀번호가 올바르지 않습니다.",
        "inactive": "비활성화된 계정입니다.",
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-input"
        self.fields["password"].widget.attrs["class"] = "form-input"


class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_incorrect": "현재 비밀번호가 올바르지 않습니다.",
        "password_mismatch": "새 비밀번호와 비밀번호 확인이 일치하지 않습니다.",
    }

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields["old_password"].label = "현재 비밀번호"
        self.fields["new_password1"].label = "새 비밀번호"
        self.fields["new_password2"].label = "새 비밀번호 확인"

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-input"


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("nickname", "profile_image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nickname"].label = "닉네임"
        self.fields["profile_image"].label = "프로필 이미지"
        self.fields["nickname"].widget.attrs["class"] = "form-input"
        self.fields["profile_image"].widget.attrs["class"] = "form-input"
