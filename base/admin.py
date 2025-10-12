from django.contrib import admin
from .models import *

from django.utils.html import format_html, format_html_join



admin.site.register(NewsArticle)
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
			# Build color HTML entries (thumbnail + admin link)
			color_entries = []
			for c in item.get('selected_colors', []):
				c_name = c.get('name', '')
				c_img = c.get('image')
				c_admin = c.get('admin')
				if c_img:
					entry = f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px;'>"
					entry += f"<img src='{c_img}' style='width:40px;height:40px;object-fit:cover;border-radius:50%;border:1px solid #e5e7eb;' />"
					entry += f"<div style='font-size:13px;color:#111;'> {c_name}"
					if c_admin:
						entry += f" &nbsp;<a href='{c_admin}' target='_blank' style='font-size:12px;'>[view]</a>"
					entry += "</div></div>"
				else:
					entry = f"<div style='font-size:13px;margin-bottom:6px;'>{c_name}"
					if c_admin:
						entry += f" &nbsp;<a href='{c_admin}' target='_blank' style='font-size:12px;'>[view]</a>"
					entry += "</div>"
				color_entries.append(entry)
			colors_html = ''.join(color_entries)

			# Packaging entries
			pack_entries = []
			for p in item.get('selected_packs', []):
				p_name = p.get('name', '')
				p_img = p.get('image')
				p_admin = p.get('admin')
				if p_img:
					pentry = f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px;'>"
					pentry += f"<img src='{p_img}' style='width:48px;height:32px;object-fit:cover;border-radius:6px;border:1px solid #e5e7eb;' />"
					pentry += f"<div style='font-size:13px;color:#111;'>{p_name}"
					if p_admin:
						pentry += f" &nbsp;<a href='{p_admin}' target='_blank' style='font-size:12px;'>[view]</a>"
					pentry += "</div></div>"
				else:
					pentry = f"<div style='font-size:13px;margin-bottom:6px;'>{p_name}"
					if p_admin:
						pentry += f" &nbsp;<a href='{p_admin}' target='_blank' style='font-size:12px;'>[view]</a>"
					pentry += "</div>"
				pack_entries.append(pentry)
			packs_html = ''.join(pack_entries)

			# Selected features (functions)
			features = ', '.join([f.get('name', '') for f in item.get('selected_functions', [])]) or ''

			# Custom color/pack strings
			custom_color = item.get('custom_color')
			custom_color_str = ''
			if custom_color:
				hex_code = custom_color.get('hex', '')
				pantone = custom_color.get('pantone', '')
				if hex_code or pantone:
					custom_color_str = '<div style="font-size:13px;color:#374151;">Custom Color:'
					if hex_code:
						custom_color_str += f" <span style='font-weight:bold;color:{hex_code};'>{hex_code}</span>"
					if pantone:
						custom_color_str += f" <span style='font-weight:bold'>{pantone}</span>"
					custom_color_str += '</div>'

			custom_pack = item.get('custom_packaging')
			custom_pack_str = ''
			if custom_pack and custom_pack.get('name'):
				custom_pack_str = f"<div style='font-size:13px;'>Custom Packaging: <b>{custom_pack.get('name')}</b></div>"

			rows.append(
				f"<tr>"
				f"<td style='vertical-align:top;padding:8px;border-bottom:1px solid #e5e7eb;'><b>{item.get('product_name','-')}</b><br><a href='{item.get('product_link','')}' target='_blank' style='font-size:12px;'>Open product</a></td>"
				f"<td style='vertical-align:top;padding:8px;border-bottom:1px solid #e5e7eb;'>{colors_html}{custom_color_str}</td>"
				f"<td style='vertical-align:top;padding:8px;border-bottom:1px solid #e5e7eb;'>{packs_html}{custom_pack_str}</td>"
				f"<td style='vertical-align:top;padding:8px;border-bottom:1px solid #e5e7eb;'>{item.get('uploaded_file_name','')}</td>"
				f"<td style='vertical-align:top;padding:8px;border-bottom:1px solid #e5e7eb;'>{features}</td>"
				f"<td style='vertical-align:top;padding:8px;border-bottom:1px solid #e5e7eb;'>{item.get('customization_note','')}</td>"
				f"</tr>"
			)
			table = """
			<table style='border-collapse:collapse;width:100%;'>
				<tr><th style='text-align:left;padding:8px;'>Product</th><th style='text-align:left;padding:8px;'>Colors</th><th style='text-align:left;padding:8px;'>Packaging</th><th style='text-align:left;padding:8px;'>Uploaded File</th><th style='text-align:left;padding:8px;'>Features</th><th style='text-align:left;padding:8px;'>Note</th></tr>
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