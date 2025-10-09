from django.contrib import admin
from .models import *

from django.utils.html import format_html, format_html_join



admin.site.register(ProductImage)
admin.site.register(productFeatures)
admin.site.register(CustomizationColorImage)
admin.site.register(CustomizationTextureImage)
admin.site.register(CustomizationFunctionImage)
admin.site.register(CustomizationPackagingImage)


class QuoteRequestAdmin(admin.ModelAdmin):
	list_display = ('name', 'company', 'email', 'created_at')
	readonly_fields = ('wishlist_data_pretty',)

	def wishlist_data_pretty(self, obj):
		wishlist = obj.wishlist_data or []
		if not wishlist:
			return "<i>No wishlist items</i>"
		rows = []
		for item in wishlist:
			# Colors: show selected color names, and custom color hex/pantone if present
			colors_list = [c.get('name', '') for c in item.get('selected_colors', [])]
			custom_color = item.get('custom_color')
			custom_color_str = ''
			if custom_color:
				hex_code = custom_color.get('hex', '')
				pantone = custom_color.get('pantone', '')
				if hex_code or pantone:
					custom_color_str = f"Custom Color: "
					if hex_code:
						custom_color_str += f"Hex: <span style='color:{hex_code};font-weight:bold'>{hex_code}</span> "
					if pantone:
						custom_color_str += f"Pantone: <span style='font-weight:bold'>{pantone}</span>"
			colors = ', '.join(colors_list)
			if custom_color_str:
				colors = (colors + '<br>' if colors else '') + custom_color_str
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
			'fields': ('name', 'company', 'email', 'phone', 'address', 'custom_packaging_image', 'spec_sheet_file', 'wishlist_data_pretty')
		}),
	)

admin.site.register(QuoteRequest, QuoteRequestAdmin)