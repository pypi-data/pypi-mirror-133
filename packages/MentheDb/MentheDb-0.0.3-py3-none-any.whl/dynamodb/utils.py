class StringExpressionsGen:

    @staticmethod
    def gen_update_str_expression(field_values: dict):
        init_str = "set "
        set_attr_values = {}
        for i, (k, v) in enumerate(field_values.items()):
            if i == len(field_values) - 1:
                init_str += '%s=:%s' % (k, k[:3])
            else:
                init_str += '%s=:%s, ' % (k, k[:3])
            set_attr_values.setdefault(':%s' % (k[:3]), v)

        return init_str, set_attr_values
