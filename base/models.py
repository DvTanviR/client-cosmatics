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
	uploaded_file = models.FileField(upload_to='quote_uploads/', blank=True, null=True, help_text='User uploaded spec/artwork/details file')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Quote from {self.name} ({self.company})"



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

# Customization and related image models
class Customization(models.Model):
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='customizations')
	color_images = models.ManyToManyField('CustomizationColorImage', blank=True, related_name='customizations')
	texture_images = models.ManyToManyField('CustomizationTextureImage', blank=True, related_name='customizations')
	function_images = models.ManyToManyField('CustomizationFunctionImage', blank=True, related_name='customizations')
	packaging_images = models.ManyToManyField('CustomizationPackagingImage', blank=True, related_name='customizations')
	def __str__(self):
		return f"({self.category.name})"


class HowItworks(models.Model):
	catagory = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='how_it_works')
	title = models.CharField(max_length=200)
	description = models.TextField()
	image = models.ImageField(upload_to='how_it_works/', blank=True, null=True)

	def __str__(self):
		return self.title




# Certification model for product certifications (e.g., Vegan, Cruelty-Free)
class Functions(models.Model):
	name = models.CharField(max_length=100, unique=True)

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


# PackagingOption model for product packaging choices
class PackagingOption(models.Model):
	name = models.CharField(max_length=100, unique=True)
	image = models.ImageField(upload_to='products/packaging/', blank=True, null=True)

	def __str__(self):
		return self.name

# FragranceOption model for product fragrance choices
class FragranceOption(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	image = models.ImageField(upload_to='categories/')

	def __str__(self):
		return self.name
	
class productFeatures(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY_CHOICES = [
		('makeup', 'Makeup'),
		('skincare', 'Skincare'),
	]

	name = models.CharField(max_length=200)
	category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
	# type = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
	description = CKEditor5Field(blank=True)
	features = models.ManyToManyField('productFeatures', blank=True, related_name='products', help_text='Key features or benefits')
	images = models.ManyToManyField('ProductImage', blank=True, related_name='products')
	# ingredients = models.TextField(blank=True, help_text='List of ingredients')
	# min_order_quantity = models.PositiveIntegerField(default=100)
	packaging_options = models.ManyToManyField('PackagingOption', blank=True, related_name='products', help_text='Bottle, jar, tube, etc.')
	color_options = models.ManyToManyField('ColorShade', blank=True, related_name='products', help_text='Available shades/colors')
	# fragrance_options = models.ManyToManyField('FragranceOption', blank=True, related_name='products', help_text='Available fragrances/scents')
	# logo_printing = models.BooleanField(default=True, help_text='Allow custom logo printing')
	# custom_label = models.BooleanField(default=True, help_text='Allow custom label design')
	# box_packaging = models.BooleanField(default=True, help_text='Allow custom box packaging')
	# function_options = models.ManyToManyField('Functions', blank=True, related_name='products', help_text='E.g. Vegan, Cruelty-Free, etc.')
	# sample_available = models.BooleanField(default=True)
	# lead_time_days = models.PositiveIntegerField(default=30, help_text='Production lead time in days')
	# price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Base price per unit')
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	# updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name






