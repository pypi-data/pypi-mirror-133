from django.template.defaultfilters import slugify

# Utilities start here


# Returns the path to a specific work order image 
def get_image_filename(instance, filename):
    title = instance.work_order
    slug = slugify(title)
    return "media/work_order_images/%s-%s" % (slug, filename)