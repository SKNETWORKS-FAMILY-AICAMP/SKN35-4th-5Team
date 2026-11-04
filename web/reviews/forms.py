from django import forms


class ProductChoiceMixin:
    """로그인한 사용자의 제품만 선택지로 보여준다."""

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = user.products.all()
        self.fields["product"].empty_label = "제품을 선택하세요"


class ReviewForm(ProductChoiceMixin, forms.Form):
    product = forms.ModelChoiceField(queryset=None, label="제품")
    copy_text = forms.CharField(label="광고 문구", max_length=5000, widget=forms.Textarea(attrs={"rows": 4}))


class GenerateForm(ProductChoiceMixin, forms.Form):
    # 선택지는 AI 서버 GenerateRequest의 Literal 값과 같아야 한다.
    CHANNELS = ["상세페이지", "SNS", "배너", "검색광고", "라이브커머스"]
    LENGTHS = ["한 줄", "짧은 문단", "상세 설명"]

    product = forms.ModelChoiceField(queryset=None, label="제품")
    instruction = forms.CharField(label="요청 사항", max_length=5000, widget=forms.Textarea(attrs={"rows": 3}))
    channel = forms.ChoiceField(label="채널", choices=[(c, c) for c in CHANNELS])
    tone = forms.CharField(label="어조", max_length=100, initial="고급스러운")
    length = forms.ChoiceField(label="길이", choices=[(c, c) for c in LENGTHS])
    keywords = forms.CharField(label="키워드", required=False, help_text="쉼표로 구분, 최대 10개")

    def clean_keywords(self):
        keywords = [k.strip() for k in self.cleaned_data["keywords"].split(",") if k.strip()]
        if len(keywords) > 10:
            raise forms.ValidationError("키워드는 최대 10개까지 입력할 수 있습니다.")
        return keywords
