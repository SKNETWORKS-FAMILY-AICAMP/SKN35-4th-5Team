from django import forms

from products.samples import product_choices, resolve_product_choice


class ProductChoiceMixin:
    """제품 선택지: 내 제품 + 아직 불러오지 않은 3차 예시 제품 (3차 화면처럼 바로 고를 수 있게).

    예시 제품을 고르면 검증 시점에 내 제품으로 복사하고, cleaned_data["product"] 는 항상 Product 다.
    폼에 선언된 product 필드는 여기서 ChoiceField 로 바꿔 끼운다.
    """

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        label = self.fields["product"].label if "product" in self.fields else "제품"
        self.fields["product"] = forms.ChoiceField(
            label=label,
            choices=product_choices(user),
            help_text="예시 제품을 고르면 내 제품에 추가된 뒤 검토합니다.",
        )

    def clean_product(self):
        product = resolve_product_choice(self.user, self.cleaned_data["product"])
        if product is None:
            raise forms.ValidationError("제품을 다시 선택해 주세요.")
        return product


class ReviewForm(ProductChoiceMixin, forms.Form):
    product = forms.ChoiceField(label="제품")
    copy_text = forms.CharField(label="광고 문구", max_length=5000, widget=forms.Textarea(attrs={"rows": 4}))


class GenerateForm(ProductChoiceMixin, forms.Form):
    # 선택지는 AI 서버 GenerateRequest의 Literal 값과 같아야 한다.
    CHANNELS = ["상세페이지", "SNS", "배너", "검색광고", "라이브커머스"]
    LENGTHS = ["한 줄", "짧은 문단", "상세 설명"]

    product = forms.ChoiceField(label="제품")
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
