from flask_restx import Namespace, Resource
from flask_cors import cross_origin
from src.core.awards import AwardsCore

import traceback

# Namespaces
awards_ns = Namespace("awards", description="Prêmios")


@awards_ns.route("/longest-fastest-consecutive-awards")
class ListRegionResource(Resource):

    @awards_ns.doc(description="Intervalo de prêmios")
    @cross_origin()
    def get(self):
        """Intervalo de prêmios"""

        try:
            return AwardsCore().get_longest_fastest_consecutive_awards()
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            return 400, {}
