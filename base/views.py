import io
import requests
from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from Administration.models import *

@csrf_exempt
def SendQuote(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
    try:
        import json, base64
        from django.core.files.base import ContentFile
        # Get data from multipart/form-data
        name = request.POST.get('name')
        company = request.POST.get('company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        wishlist_raw = request.POST.get('wishlist', '[]')
        try:
            wishlist = json.loads(wishlist_raw)
        except Exception:
            wishlist = []

        # Prepare uploads
        custom_color_image = None
        custom_packaging_image = None
        spec_sheet_file = None

        # Find uploads in wishlist items (first found)
        for item in wishlist:
            # Custom color image (base64)
            custom_color = item.get('custom_color')
            if custom_color and custom_color.get('image'):
                img_data = custom_color['image']
                if img_data.startswith('data:'):
                    fmt, b64 = img_data.split(';base64,')
                    ext = fmt.split('/')[-1]
                    custom_color_image = ContentFile(base64.b64decode(b64), name=f'custom_color.{ext}')
                break
        for item in wishlist:
            # Custom packaging image (base64)
            custom_pack = item.get('custom_packaging')
            if custom_pack and custom_pack.get('data'):
                img_data = custom_pack['data']
                if img_data.startswith('data:'):
                    fmt, b64 = img_data.split(';base64,')
                    ext = fmt.split('/')[-1]
                    custom_packaging_image = ContentFile(base64.b64decode(b64), name=f'custom_packaging.{ext}')
                break
        for item in wishlist:
            # Spec sheet file (base64)
            spec_file = item.get('custom_spec_sheet')
            if spec_file and spec_file.get('data'):
                file_data = spec_file['data']
                if file_data.startswith('data:'):
                    fmt, b64 = file_data.split(';base64,')
                    ext = fmt.split('/')[-1]
                    spec_sheet_file = ContentFile(base64.b64decode(b64), name=f'spec_sheet.{ext}')
                break

        quote_obj = QuoteRequest.objects.create(
            name=name,
            company=company,
            email=email,
            phone=phone,
            address=address,
            wishlist_data=wishlist,
            custom_packaging_image=custom_packaging_image,
            spec_sheet_file=spec_sheet_file
        )

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph('<b>Quote Request</b>', styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f'<b>Name:</b> {name}', styles['Normal']))
        elements.append(Paragraph(f'<b>Company:</b> {company}', styles['Normal']))
        elements.append(Paragraph(f'<b>Email:</b> {email}', styles['Normal']))
        elements.append(Paragraph(f'<b>Phone:</b> {phone}', styles['Normal']))
        elements.append(Paragraph(f'<b>Address:</b> {address}', styles['Normal']))
        elements.append(Spacer(1, 18))
        elements.append(Paragraph('<b>Wishlist</b>', styles['Heading2']))
        elements.append(Spacer(1, 8))

        # Table header (removed Perfume)
        table_data = [[
            'Image',
            'Product Name',
            'Color(s)',
            'Packaging',
            'Function Option',
            'Product Link'
        ]]

        for item in wishlist:
            img_flowable = ''
            img_url = item.get('product_main_image_url')
            if img_url:
                try:
                    img_resp = requests.get(img_url, timeout=5)
                    if img_resp.status_code == 200:
                        img_bytes = io.BytesIO(img_resp.content)
                        img_flowable = Image(img_bytes, width=40, height=40)
                except Exception:
                    img_flowable = ''

            pname = item.get('product_name', '-')
            colors_html = ''
            for c in item.get('selected_colors', []):
                hex_code = c.get('hex_code', '#eee')
                color_name = c.get('name', '')
                colors_html += f'<font color="{hex_code}">&#9679;</font><br/><font size=8>{color_name}</font><br/>'
            packs = ', '.join([p.get('name','') for p in item.get('selected_packs',[])])
            functions = ', '.join([f.get('name','') for f in item.get('selected_functions',[])])
            product_link = item.get('product_link', '-')
            if product_link and product_link != '-':
                product_link_para = Paragraph(f'<link href="{product_link}">{product_link}</link>', styles['Normal'])
            else:
                product_link_para = Paragraph('-', styles['Normal'])
            table_data.append([
                img_flowable if img_flowable else '',
                Paragraph(pname, styles['Normal']),
                Paragraph(colors_html or '-', styles['Normal']),
                Paragraph(packs or '-', styles['Normal']),
                Paragraph(functions or '-', styles['Normal']),
                product_link_para,
            ])

        wishlist_table = Table(table_data, colWidths=[45, 80, 70, 70, 90, 120])
        wishlist_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#374151')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
            ('FONTSIZE', (0,1), (-1,-1), 9),
        ]))
        elements.append(wishlist_table)
        elements.append(Spacer(1, 18))
        quote_link = f"{request.build_absolute_uri('/admin/base/quoterequest/')}{quote_obj.id}/change/"
        # Build admin PDF (with quote record link)
        elements_admin = list(elements)
        elements_admin.append(Paragraph(f'<b>Quote Request Record:</b> <link href="{quote_link}">{quote_link}</link>', styles['Normal']))
        doc.build(elements_admin)
        pdf_data_admin = buffer.getvalue()

        # Build user PDF (without quote record link)
        buffer_user = io.BytesIO()
        doc_user = SimpleDocTemplate(buffer_user, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        doc_user.build(elements)
        pdf_data_user = buffer_user.getvalue()

        subject = f"Quote Request from {name} ({company})"
        body = f"Name: {name}\nCompany: {company}\nEmail: {email}\nPhone: {phone}\nAddress: {address}\n\nSee attached PDF for wishlist."
        # Send to admin
        admin_email_msg = EmailMessage(
            subject,
            body,
            'no-replay@beyondcosmetics.us',
            ['sales@beyondcosmetics.us'],
            reply_to=[email] if email else None
        )
        admin_email_msg.attach('quote.pdf', pdf_data_admin, 'application/pdf')
        admin_email_msg.send(fail_silently=False)

        # Send confirmation to user
        if email:
            user_subject = "Your Quote Request has been received"
            user_body = f"Dear {name},\n\nThank you for your quote request. We have received your information and will get back to you soon.\n\nPlease find attached a copy of your quote request for your records.\n\nBest regards,\nBEYOND Team"
            user_email_msg = EmailMessage(
                user_subject,
                user_body,
                'noreply@example.com',
                [email],
                reply_to=['sales@beyondcosmetics.us']
            )
            user_email_msg.attach('quote.pdf', pdf_data_user, 'application/pdf')
            user_email_msg.send(fail_silently=False)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def Home(request):
    # Get all MainCategory objects and their related Category objects
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    # Structure: [{'main': MainCategory, 'subs': [Category, ...]}, ...]
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    # Pass main_categories for Explore section
    return render(request, 'index.html', {
        'nav_structure': nav_structure,
        'main_categories': main_categories,
    })

def About(request):
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    return render(request, 'about.html', {'nav_structure': nav_structure,})


def Shop(request):
    catagories = MainCategory.objects.all()
    products = Product.objects.filter(is_active=True)
    catagories_heor = catagories.order_by('-id')[:5]
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    context = {
        'catagories': catagories,
        'products': page_obj.object_list,
        'catagories_heor': catagories_heor,
        'page_obj': page_obj,
        'paginator': paginator,
        'nav_structure': nav_structure,
    }
    return render(request, 'shop.html', context)

def Contact(request):
    from django.core.mail import send_mail, BadHeaderError
    from django.conf import settings
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    message_sent = False
    error_message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        company = request.POST.get('company')
        if name and email and message:
            subject = f"Contact Form Submission from {name}"
            body = f"Name: {name} \nEmail: {email} \nCompany: {company} \n\nMessage:\n{message}"
            try:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, ["sales@beyondcosmetics.us"], fail_silently=False)
                message_sent = True
            except BadHeaderError:
                error_message = "Invalid header found."
            except Exception as e:
                error_message = str(e)
        else:
            error_message = "Please fill out all fields."
    return render(request, 'contact.html', {'message_sent': message_sent, 'error_message': error_message, 'nav_structure': nav_structure,})

def Services(request):
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    return render(request, 'services.html', {'nav_structure': nav_structure})

def ProductDetail(request, product_id):
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
        'nav_structure': nav_structure,
    }
    return render(request, 'product.html', context)


def Wishlist(request):
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    return render(request, 'wishlist.html', {'nav_structure': nav_structure,})


def CatagoryPage(request, category_id):
    category = Category.objects.get(id=category_id)
    products = category.products.filter(is_active=True)

    # Get the first Customization object for this category (if any)
    customization = category.customizations.first()
    main_categories = MainCategory.objects.prefetch_related('subcategories').all()
    nav_structure = []
    for main_cat in main_categories:
        subs = main_cat.subcategories.all()
        nav_structure.append({'main': main_cat, 'subs': subs})
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 30)
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'customization': customization,
        'nav_structure': nav_structure,
    }
    return render(request, 'catagory.html', context)