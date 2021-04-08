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

@app.route("/mutate", methods=["POST"])
def mutate():
    app.logger.debug('on mutate')
    original_object = request.json["request"]["object"]
    modified_object = copy.deepcopy(original_object)
    original_spec = original_object["spec"]
    spec = modified_object["spec"]

    app.logger.debug('mutating spec %s', str(spec))

    try:
        if 'dnsConfig' not in spec:
            spec['dnsConfig'] = {'searches': []}
            app.logger.debug('added dnsConfig %s', str(spec))

        dns_config = spec['dnsConfig']
        app.logger.debug('dns config %s', str(dns_config))

        if 'searches' not in dns_config:
            dns_config['searches'] = []

        searches = dns_config['searches']
        searches += ['ah.svc.cluster.local']

    except KeyError as e:
        app.logger.warning('Mutate got KeyError %s', str(e))

    patch = jsonpatch.JsonPatch.from_diff(original_object, modified_object)
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
    app.logger.debug('Mutate returning response %s', str(response))
    return jsonify(response)


@app.route("/health", methods=["GET"])
def health():
    return ("", http.HTTPStatus.NO_CONTENT)

if __name__ == "__main__": # development
    app.run(host="0.0.0.0", debug=True)  # pragma: no cover
