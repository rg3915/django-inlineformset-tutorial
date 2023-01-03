from django.db import models
from django.urls import reverse


class Provider(models.Model):
    name = models.CharField('nome', max_length=30, unique=True)

    class Meta:
        verbose_name = 'fornecedor'
        verbose_name_plural = 'fornecedores'

    def __repr__(self):
        return f'Provider({self.name})'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField('título', max_length=20, unique=True)
    price = models.DecimalField('preço', max_digits=7, decimal_places=2)
    manufacturing_date = models.DateField('data de fabricação', null=True, blank=True)  # noqa E501
    due_date = models.DateField('data de vencimento', null=True, blank=True)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("admin:product_product_change", args=(self.id,))
