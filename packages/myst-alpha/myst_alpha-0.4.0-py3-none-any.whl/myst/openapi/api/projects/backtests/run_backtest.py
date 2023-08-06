from myst.client import Client
from myst.openapi.models.backtest_job_get import BacktestJobGet


def request_sync(client: Client, project_uuid: str, uuid: str) -> BacktestJobGet:
    """Gets a backtest by its unique identifier."""

    return client.request(
        method="post", path=f"/projects/{project_uuid}/backtests/{uuid}:run", response_class=BacktestJobGet
    )
