from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag("payments/thankyou_display.html")
def payment_thankyou_display(request, payment):
    obj_header = None
    obj_display = None
        
    if not payment:
        obj = None
    else:
        obj = payment.invoice.get_object()

        #print 'obj', obj._meta.app_label

        if obj:
            from django.template.loader import render_to_string
            from django.template import RequestContext
            from django.template import TemplateDoesNotExist
            app_label = obj._meta.app_label
            template_name = "%s/payment_thankyou_display.html" % (app_label)
            try:
                obj_display = render_to_string(template_name, {'obj':obj,
                                                   'payment':payment},
                                                   context_instance=RequestContext(request))
            except TemplateDoesNotExist:
                pass
            
            template_name = "%s/payment_thankyou_header.html" % (app_label)
            try:
                obj_header = render_to_string(template_name, {'obj':obj,
                                                   'payment':payment},
                                                   context_instance=RequestContext(request))
            except TemplateDoesNotExist:
                pass         
    
    return {'request':request, 
            "payment" : payment,
            "obj": obj, 
            'obj_header': obj_header,
            'obj_display':obj_display}
    
@register.inclusion_tag('payments/stripe/js_stripe_key.html', takes_context=True)
def set_stripe_key(context):
    context["STRIPE_PUBLISHABLE_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
    return context