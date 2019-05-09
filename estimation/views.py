import json
from http import HTTPStatus

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render

from estimation.helpers import Estimation
from estimation.models import Holiday


def index(request):
    return render(request, 'index.html')


def estimate(request):
    if request.method == "POST":

        estimation = Estimation(json.loads(request.body).get("date"),
                                          json.loads(request.body).get("estimation_type"))
        allowed, estimated, reason = estimation.estimate()
        response = {"delivery": estimation.delivery,
                    "return": estimation.pick_up
                    }
        if allowed:
            return JsonResponse(data=response.get(json.loads(request.body).get("estimation_type"))(),
                                status=HTTPStatus.OK)
        estimated = estimated.first().date.strftime("%A") if isinstance(estimated, QuerySet) else estimated

        return JsonResponse(data={"message": f"can't order on {estimated}, because {reason}"}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
