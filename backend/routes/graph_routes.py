from flask import Blueprint, request, jsonify
from algorithms.connected_components import connected_components
from algorithms.strongly_connected_components import strongly_connected_components

graph_bp = Blueprint("graph", __name__)

@graph_bp.route("/cc", methods=["POST"])
def cc_route():
    data = request.json

    result, steps = connected_components(data["graph"])

    return jsonify({
        "success": True,
        "algorithm": "cc",
        "result": result,
        "visualization": {
            "steps": steps
        }
    })


@graph_bp.route("/scc", methods=["POST"])
def scc_route():
    data = request.json

    result = strongly_connected_components(data["graph"])

    return jsonify({
        "success": True,
        "algorithm": "scc",
        "result": result
    })
