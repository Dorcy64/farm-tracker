from flask import jsonify
import json


def strip_tags_from_request(category_in):
    output = []
    if category_in is not None and category_in != "" and len(category_in) > 3:
        new_cat = json.loads(category_in)
        for key in new_cat:
            for value in key.values():
                output.append(value)

        return output

    return None


def render_json(status, *args, **kwargs):
    """
    Return a JSON response.
    Example usage:
      render_json(404, {'error': 'Discount code not found.'})
      render_json(200, {'data': coupon.to_json()})
    :param status: HTTP status code
    :type status: int
    :param args:
    :param kwargs:
    :return: Flask response
    """
    response = jsonify(*args, **kwargs)
    response.status_code = status

    return response
