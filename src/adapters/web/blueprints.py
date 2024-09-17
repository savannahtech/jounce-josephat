from flask import Blueprint, render_template, request
from flask_injector import inject

from src.application.ports.usecases import IUseCases

visualize_blueprint = Blueprint(
    "visualize", __name__, url_prefix="/", static_folder="../static"
)


@visualize_blueprint.route("/visualize", methods=["GET", "POST"])
@inject
def visualize(usecases: IUseCases):
    metric_name = "TTFT"
    if request.method == "POST":
        metric_name = request.form.get("metric_name")

    metric = usecases.fetch_metric_by_name(metric_name)
    data = usecases.fetch_metric_rankings_by_metric_id(metric.id)
    line_graph = usecases.create_line_graph(data)
    bar_graph = usecases.create_bar_graph(data)
    return render_template("visualize.html", line_graph=line_graph, bar_graph=bar_graph) # noqa


@visualize_blueprint.route("/visualize/all")
@inject
def visualize_all(usecases: IUseCases):
    data = usecases.rank_llms_by_metrics()
    line_graph = usecases.create_line_graph(data)
    bar_graph = usecases.create_bar_graph(data)
    return render_template(
        "visualize_all.html", line_graph=line_graph, bar_graph=bar_graph
    )
