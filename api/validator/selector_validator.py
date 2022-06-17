from ..enums.error_code import ErrorCode


class SelectorValidator:

    def __init__(self, model_class):
        self.model_class = model_class

    def validate(self, selector):
        errors = []
        # Modelで定義したカラムの一覧
        fields = [field.column for field in self.model_class._meta.fields]
        fields = self.__add_filter_field(fields)
        pop_key_list = []
        for key, value in selector.items():
            if key not in fields:
                pop_key_list.append(key)
                continue
            if not self.__validate_value(value):
                errors.append({'code': ErrorCode.UNSPECIFIED_VALUE.name, 'detail': {'key': key, 'value': value}})
        [selector.pop(pop_key) for pop_key in pop_key_list]
        return errors

    def __validate_value(self, value):
        if type(value) is str and value == '':
            return False
        if type(value) is list and len(value) == 0:
            return False
        return True

    def __add_filter_field(self, fields):
        new_fields = []
        # TODO: 型ごとに使えるフィルタを絞る
        for field in fields:
            new_fields.append(field)
            new_fields.append(field + '__exact')
            new_fields.append(field + '__icontains')
            new_fields.append(field + '__istartswith')
            new_fields.append(field + '__iendswith')
            new_fields.append(field + '__gt')
            new_fields.append(field + '__gte')
            new_fields.append(field + '__lt')
            new_fields.append(field + '__lte')
            new_fields.append(field + '__in')
            new_fields.append(field + '__range')
        return new_fields
