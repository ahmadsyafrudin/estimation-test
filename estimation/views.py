import json
from http import HTTPStatus

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from estimation.helpers import Estimation


@csrf_exempt
def estimate(request):
    if request.method == "POST":

        estimation = Estimation(json.loads(request.body).get("dateTime"),
                                json.loads(request.body).get("estimationType"))
        pickup = True if json.loads(request.body).get("estimationType") == "return" else None
        allowed, estimated, reason = estimation.estimate(pickup=pickup)
        response = {"delivery": estimation.delivery,
                    "return": estimation.pick_up
                    }
        if allowed:
            return JsonResponse(data=response.get(json.loads(request.body).get("estimationType"))(),
                                status=HTTPStatus.OK)
        estimated = estimated.first().date.strftime("%A") if isinstance(estimated, QuerySet) else estimated.strftime(
            "%A")

        return JsonResponse(data={"message": f"can't order on {estimated}, because {reason}"},
                            status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse(data={"message": "method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)
