from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Functions)
admin.site.register(ColorShade)
admin.site.register(PackagingOption)
admin.site.register(FragranceOption)
admin.site.register(productFeatures)

admin.site.register(CustomizationColorImage)
admin.site.register(CustomizationTextureImage)
admin.site.register(CustomizationFunctionImage)
admin.site.register(CustomizationPackagingImage)
admin.site.register(Customization)
admin.site.register(HowItworks)

from django.utils.html import format_html, format_html_join

class QuoteRequestAdmin(admin.ModelAdmin):
	list_display = ('name', 'company', 'email', 'created_at')
	readonly_fields = ('wishlist_data_pretty',)

	def wishlist_data_pretty(self, obj):
		wishlist = obj.wishlist_data or []
		if not wishlist:
			return "<i>No wishlist items</i>"
		rows = []
		for item in wishlist:
			colors = ', '.join([c.get('name', '') for c in item.get('selected_colors', [])])
			packs = ', '.join([p.get('name', '') for p in item.get('selected_packs', [])])
			rows.append(
				f"<tr>"
				f"<td><b>{item.get('product_name', '-')}</b></td>"
				f"<td>{colors}</td>"
				f"<td>{packs}</td>"
				f"<td>{item.get('uploaded_file_name', '')}</td>"
				f"</tr>"
			)
		table = """
		<table style='border-collapse:collapse;'>
			<tr><th>Product</th><th>Colors</th><th>Packaging</th><th>Uploaded File</th></tr>
			{rows}
		</table>
		""".replace('{rows}', ''.join(rows))
		return format_html(table)
	wishlist_data_pretty.short_description = "Wishlist Details"

	fieldsets = (
		(None, {
			'fields': ('name', 'company', 'email', 'phone', 'address', 'uploaded_file', 'wishlist_data_pretty')
		}),
	)

admin.site.register(QuoteRequest, QuoteRequestAdmin)