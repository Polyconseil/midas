import json
import pytest

from django.utils import timezone
from midas import admin  # noqa: F401
from midas import models

from django.contrib.gis.geos import GEOSGeometry


@pytest.mark.django_db
def test_admin(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_service_area(client):
    response = client.get("/service_area/foo/bar/")
    assert response.status_code == 404
    models.Area.objects.create(
        id="13B8C961-61FD-4CCE-8113-81AF1DE90942",
        provider="27E84290-06B4-4C5D-88F2-60E6DCB09712",
        begin_date=timezone.now(),
        polygon=GEOSGeometry(
            json.dumps(
                {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [2.293117046356201, 48.85829170715186],
                            [2.294490337371826, 48.857416413913725],
                            [2.295863628387451, 48.8583905296204],
                            [2.294447422027588, 48.85913875055143],
                            [2.293117046356201, 48.85829170715186],
                        ]
                    ],
                }
            )
        ),
    )
    response = client.get(
        "/service_area/27e84290-06b4-4c5d-88f2-60e6dcb09712/13b8c961-61fd-4cce-8113-81af1de90942/"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_device(client):
    response = client.put(
        "/vehicle/27e84290-06b4-4c5d-88f2-60e6dcb09712/13b8c961-61fd-4cce-8113-81af1de90942/",
        data={"identification_number": "foo", "model": "bar"},
        content_type="application/json",
    )
    assert response.status_code == 201
    response = client.post(
        "/vehicle/27e84290-06b4-4c5d-88f2-60e6dcb09712/13b8c961-61fd-4cce-8113-81af1de90942/",
        data={
            "status": "available",
            "position": {
                "type": "Point",
                "coordinates": [2.293117046356201, 48.85829170715186],
            },
        },
        content_type="application/json",
    )
    assert response.status_code == 200
    response = client.get("/vehicle/")
    assert response.status_code == 200
    assert response.data == [
        {
            "id": "13b8c961-61fd-4cce-8113-81af1de90942",
            "provider": "27e84290-06b4-4c5d-88f2-60e6dcb09712",
            "identification_number": "foo",
            "model": "bar",
            "status": "available",
            "position": '{ "type": "Point", "coordinates": [ 2.293117046356201, 48.858291707151857 ] }',
            "properties": {},
        }
    ]
