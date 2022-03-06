from market import login_manager, app
from market.models import User
from urllib.parse import urlparse, urljoin
from flask import request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def utility_processor():
    def add_comma_to_money(amt):
        amt = str(amt)
        integer, decimal = amt.split(".")
        length = len(integer)
        if length > 3:
            y = []
            parts = length // 3
            for x in range(parts):
                if x == 0:
                    y.append(integer[-3:])
                else:
                    y.insert(0, integer[-3 * (x + 1): -3 * x])

            left = length % 3
            if left != 0:
                y.insert(0, integer[:left])

            return ",".join(y) + "." + decimal

        return amt
    return dict(add_comma_to_money=add_comma_to_money)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
