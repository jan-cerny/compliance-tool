import compliance.products

def find_ds():
    product = compliance.products.detect_product()
    return "/usr/share/xml/scap/ssg/content/ssg-" + product + "-ds.xml"
