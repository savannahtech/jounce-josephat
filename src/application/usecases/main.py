import base64
import io

import matplotlib.pyplot as plt
import plotly.graph_objs as go
from injector import inject, singleton

from src.application.ports.uow import IUnitOfWork
from src.application.ports.usecases import IUseCases
from src.infrastructure.utils.constants import NUMBER_OF_DATA_POINTS, SEED_VALUE
from src.infrastructure.utils.helpers import generate_data


@singleton
class MetricUseCases(IUseCases):

    @inject
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def generate_llm_data(self):
        with self.uow:
            llms = self.uow.repository.get_all_llms()
            metrics = self.uow.repository.get_all_metrics()
            data = generate_data(
                seed=SEED_VALUE,
                num_points=NUMBER_OF_DATA_POINTS,
                models=llms,
                metrics=metrics,
            )
            self.uow.repository.bulk_create_record(data)

    def fetch_metric_by_name(self, name):
        with self.uow:
            return self.uow.repository.get_metric_by_name(name)

    def fetch_metric_rankings_by_metric_id(self, metric_id):
        with self.uow:
            return self.uow.repository.get_llm_metric_rankings_by_metric_id(metric_id) # noqa

    def rank_llms_by_metrics(self):
        all_results = []

        with self.uow:
            metrics = self.uow.repository.get_all_metrics()
            for metric in metrics:
                results = self.uow.repository.get_llm_metric_rankings_by_metric_id(
                    metric.id
                )
                for result in results:
                    result["metric"] = metric
                    all_results.append(result)

        ranked_llms = {}
        for result in all_results:
            llm = result["llm"]
            metric = result["metric"]
            mean_value = result["mean_value"]

            if llm not in ranked_llms:
                ranked_llms[llm] = {}
            ranked_llms[llm][metric] = mean_value

        ranked_list = []
        for llm, metrics in ranked_llms.items():
            avg_score = sum(metrics.values()) / len(metrics)
            ranked_list.append({"llm": llm, "mean_value": avg_score})

        ranked_list = sorted(ranked_list, key=lambda x: x["mean_value"], reverse=True) # noqa
        return ranked_list

    def create_line_graph(self, data):
        # In a non-GUI environment, it will throw RuntimeError:
        #  main thread is not in the main loop.
        # Simply switch to backends that do not
        # employ a graphical user interface, such as Agg, Cairo, PS, PDF, or SVG. # noqa
        # https://stackoverflow.com/questions/52839758/matplotlib-and-runtimeerror-main-thread-is-not-in-main-loop
        plt.switch_backend("agg")

        # Extract data
        llms = [d["llm"] for d in data]
        mean_values = [d["mean_value"] for d in data]

        # Create line graph with a larger figure size
        _, ax = plt.subplots(figsize=(10, 6))
        ax.plot(llms, mean_values, marker="o", color="b")
        ax.set_xlabel("LLM Model")
        ax.set_ylabel("Mean Value")
        ax.set_title("Line Graph: LLM Performance by Mean Value")
        # Set the x-ticks and rotate the labels
        ax.set_xticks(range(len(llms)))
        ax.set_xticklabels(llms, rotation=65, ha="right")
        # Automatically adjust subplot parameters
        # to give room for the x-axis labels
        plt.tight_layout()
        # Convert plot to PNG image
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode("utf-8")
        plt.close()
        return "data:image/png;base64,{}".format(graph_url)

    def create_bar_graph(self, data):
        # Extract data
        llms = [d["llm"] for d in data]
        mean_values = [d["mean_value"] for d in data]
        # Create bar graph
        fig = go.Figure([go.Bar(x=llms, y=mean_values)])
        fig.update_layout(
            title="Bar Graph: LLM Performance by Mean Value",
            xaxis_title="LLM Model",
            yaxis_title="Mean Value",
        )
        # Convert Plotly figure to HTML
        graph_html = fig.to_html(full_html=False)
        return graph_html
