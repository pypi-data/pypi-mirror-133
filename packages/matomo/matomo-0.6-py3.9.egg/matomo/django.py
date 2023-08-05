import collections

from django.conf import settings

import matomo


MATOMO_SITE_ID = getattr(settings, "MATOMO_SITE_ID", 0)
MATOMO_TRACKING_API_URL = getattr(settings, "MATOMO_TRACKING_API_URL", "")


class DjangoRequest(collections.UserDict):
    pass


def get_tracker(request):
    trequest = DjangoRequest()
    trequest.update(request.META)
    trequest["HTTPS"] = request.scheme == "https"
    trequest["REQUEST_URI"] = request.path
    trequest["PATH_INFO"] = request.path_info
    # Doesn't exist in Django and will be set to path info
    trequest["SCRIPT_NAME"] = ""

    if MATOMO_SITE_ID and MATOMO_TRACKING_API_URL:
        return matomo.Matomo(trequest, MATOMO_SITE_ID, MATOMO_TRACKING_API_URL)
    else:
        print("MATOMO_SITE_ID or MATOMO_TRACKING_API_URL not set.")
        return None


class MatomoMixin:
    matomo = None

    def dispatch(self, request, *args, **kwargs):
        self.matomo = get_tracker(request)
        response = super().dispatch(request, *args, **kwargs)
        # TODO: Handle cookies
        return response
