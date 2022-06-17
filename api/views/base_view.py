from rest_framework.response import Response

from ..validator.selector_validator import SelectorValidator

class BaseView:

    def get_selector(self, request, model_class):
        selector = {}
        if 'selector' not in request.data.keys():
            return selector
        selector = request.data['selector']
        selector_validator = SelectorValidator(model_class)
        errors = selector_validator.validate(selector)
        return selector, errors