import json
from http import HTTPStatus

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from estimation.helpers import Estimation


@csrf_exempt
def estimate(request):
    try:
        date_time = json.loads(request.body)["dateTime"]
        estimation_type = json.loads(request.body)["estimationType"]

    except Exception as e:
        return JsonResponse(data={"message": f"supported request body is dateTime and estimationType",
                                  "error": f"{type(e)} {json.loads(request.body).keys()}"},
                            status=HTTPStatus.BAD_REQUEST)

    if request.method == "POST":

        estimation = Estimation(date_time,
                                estimation_type)
        pickup = True if estimation_type == "return" else None
        allowed, estimated, reason = estimation.estimate(pickup=pickup)
        response = {
            "delivery": estimation.delivery,
            "return": estimation.pick_up
        }
        if allowed:
            return JsonResponse(data=response.get(estimation_type)(),
                                status=HTTPStatus.OK)

        estimated = estimated.first().date.strftime("%A") if isinstance(estimated, QuerySet) else estimated.strftime(
            "%A")

        return JsonResponse(data={"message": f"can't estimate on {estimated}, because {reason}"},
                            status=HTTPStatus.BAD_REQUEST)

    else:
        return JsonResponse(data={"message": "method not allowed"}, status=HTTPStatus.METHOD_NOT_ALLOWED)
