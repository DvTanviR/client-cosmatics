from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Model for storing quote requests
class QuoteRequest(models.Model):
	name = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=20)
	address = models.CharField(max_length=255)
	wishlist_data = models.JSONField(help_text='Serialized wishlist items from user')
	# Multiple uploaded files for custom color, packaging, and spec sheet
	# custom_color_image = models.ImageField(upload_to='quote_uploads/custom_colors/', blank=True, null=True, help_text='User uploaded custom color image')
	custom_packaging_image = models.ImageField(upload_to='quote_uploads/custom_packaging/', blank=True, null=True, help_text='User uploaded custom packaging image')
	spec_sheet_file = models.FileField(upload_to='quote_uploads/spec_sheets/', blank=True, null=True, help_text='User uploaded spec/artwork/details file')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Quote from {self.name} ({self.company})"


class QuoteAttachment(models.Model):
	"""Attach one file per wishlist item or quote-level uploads.

	This stores spec sheets, custom packaging images, or custom color images
	associated with a QuoteRequest and optionally a product id.
	"""
	ATTACHMENT_TYPES = [
		('spec_sheet', 'Spec Sheet'),
		('custom_packaging', 'Custom Packaging'),
		('custom_color', 'Custom Color'),
		('other', 'Other'),
	]

	quote = models.ForeignKey(QuoteRequest, related_name='attachments', on_delete=models.CASCADE)
	product_id = models.CharField(max_length=100, blank=True, null=True, help_text='Product id from wishlist item (if any)')
	wishlist_item_id = models.CharField(max_length=100, blank=True, null=True, help_text='Unique wishlist item id (from localStorage)')
	attachment_type = models.CharField(max_length=30, choices=ATTACHMENT_TYPES, default='other')
	file = models.FileField(upload_to='quote_uploads/attachments/')
	original_name = models.CharField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Attachment {self.original_name or self.file.name} for Quote {self.quote.id}"



class CustomizationColorImage(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='customizations/colors/')
	def __str__(self):
		return self.name

class CustomizationTextureImage(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='customizations/textures/')
	def __str__(self):
		return self.name

class CustomizationFunctionImage(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='customizations/functions/')
	def __str__(self):
		return self.name

class CustomizationPackagingImage(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='customizations/packaging/')
	def __str__(self):
		return self.name


# ColorShade model for product color/shade options
class ColorShade(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to='products/colors/', blank=True, null=True)

	def __str__(self):
		return self.name
	

class ProductImage(models.Model):
	image = models.ImageField(upload_to='products/gallery/')
	alt_text = models.CharField(max_length=255, blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.alt_text or f"Image {self.id}"
	


	
class productFeatures(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name




class NewsArticle(models.Model):
	title = models.CharField(max_length=200)
	cover_image = models.ImageField(upload_to='news/covers/')
	content = CKEditor5Field('Content', config_name='default')
	published_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


