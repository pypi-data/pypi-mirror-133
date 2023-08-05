from .ua_util import UAS

__name_mapping = {

}

def get_single_name(tp):
    if not tp:
        return "None"
    name = __name_mapping.get(tp)
    if name:
        return name
    if not isinstance(tp, object):
        tp = type(tp)
    name = '%s' % str(tp)[8:-2].split('.')[-1]
    __name_mapping[tp] = name
    return name