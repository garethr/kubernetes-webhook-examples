import base64
import copy
import http
import json
import random
import logging

import jsonpatch
from flask import Flask, jsonify, request

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route("/validate", methods=["POST"])
def validate():
    app.logger.info('on validate')
    allowed = True
    try:
        for container_spec in request.json["request"]["object"]["spec"]["containers"]:
            if "env" in container_spec:
                allowed = False
    except KeyError as e:
        app.logger.warning('Validate got KeyError %s', str(e))

    return jsonify(
        {
            "response": {
                "allowed": allowed,
                "uid": request.json["request"]["uid"],
                "status": {"message": "env keys are prohibited"},
            }
        }
    )


@app.route("/mutate", methods=["POST"])
def mutate():
    app.logger.info('on mutate')
    spec = request.json["request"]["object"]
    app.logger.info('mutating spec %s', str(spec))
    modified_spec = copy.deepcopy(spec)

    try:
        modified_spec["metadata"]["labels"]["example.com/new-label"] = str(
            random.randint(1, 1000)
        )
    except KeyError as e:
        app.logger.warning('Mutate got KeyError %s', str(e))

    patch = jsonpatch.JsonPatch.from_diff(spec, modified_spec)
    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "allowed": True,
            "uid": request.json["request"]["uid"],
            "patch": base64.b64encode(str(patch).encode()).decode(),
            "patchType": "JSONPatch",
        }
    }
    app.logger.info('Mutate returning response %s', str(jsonify(response)))
    return jsonify(response)


@app.route("/health", methods=["GET"])
def health():
    app.logger.info('/health')
    return ("", http.HTTPStatus.NO_CONTENT)


# if __name__ == "app": # gunicorn
#     app.run(host="0.0.0.0", debug=True, port=8000)  # pragma: no cover

if __name__ == "__main__": # development
    app.run(host="0.0.0.0", debug=True)  # pragma: no cover
