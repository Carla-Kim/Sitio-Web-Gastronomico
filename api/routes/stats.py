from flask import Blueprint, jsonify
from ..services import stats
from ..utils.errors import ReturnErrors

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats', methods=['GET'])
def obtener_stats():
    try:
        results = stats.obtener_stats()

    except Exception as e:
        print(f"No fue posible obtener las estadísticas. Error: {e}")
        return jsonify(ReturnErrors(500)), 500

    return jsonify(results), 200
