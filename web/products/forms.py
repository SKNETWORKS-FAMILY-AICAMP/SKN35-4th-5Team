from django import forms

from .models import Evidence, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["owner", "created_at", "updated_at"]
        widgets = {
            "key_ingredients": forms.Textarea(attrs={"rows": 2}),
            "ingredients": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("category") == Product.Category.FUNCTIONAL and not cleaned.get("functional_type"):
            self.add_error("functional_type", "기능성 화장품은 기능성 유형을 입력해 주세요.")
        return cleaned


EvidenceFormSet = forms.inlineformset_factory(
    Product,
    Evidence,
    fields=["test_type", "item", "value", "institute", "conditions"],
    extra=1,
    can_delete=True,
)
