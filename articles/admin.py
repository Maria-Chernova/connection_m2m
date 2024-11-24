
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1  # Количество пустых форм для добавления новых тегов

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.formset = ScopeInlineFormset
        return formset

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tags = [form.cleaned_data for form in self.forms if form.cleaned_data.get('is_main')]
        if len(main_tags) > 1:
            raise ValidationError('Только один тег может быть основным для статьи.')
        return super().clean()

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass