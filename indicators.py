import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import yaml
    from typing import Literal
    from pydantic import BaseModel
    return BaseModel, Literal, yaml


@app.cell
def _():
    blueprint_yaml = """
    indicators:

    - name: CopyIndicator
      type: copy
      normalize: percentiles
      desc: Copy indicator example.
      args:
        columns: ColumnA

    - name: RecodeMissingIndicator
      type: recode
      normalize: scale_weights
      desc: Recode indicator with missing values.
      args:
        columns: ColumnC
        weights:
          Ja: 1
          Nee: 2
          $MISSING$: 3

    - name: PercentageIndicator
      type: percentage
      normalize: verify
      args:
        numerator: ColumnA
        denominator: ColumnA + ColumnB
    """
    return (blueprint_yaml,)


@app.cell
def _(BaseModel, Literal):
    operator = Literal["copy", "recode", "percentage"]
    normalization = Literal["verify", "percentiles", "scale_weights"]


    class Indicator(BaseModel):
        name: str
        type: operator
        normalize: normalization
        desc: str | None = None
        args: dict


    class IndicatorBlueprint(BaseModel):
        indicators: list[Indicator]
    return (IndicatorBlueprint,)


@app.cell
def _(IndicatorBlueprint, blueprint_yaml, yaml):
    blueprint = IndicatorBlueprint.model_validate(yaml.safe_load(blueprint_yaml))
    blueprint.model_dump()
    return (blueprint,)


@app.cell
def _(BaseModel):
    class BaseOperator:
        """Operator base class."""

        class ArgModel(BaseModel):
            """Model for operator arguments."""

            columns: str

        def __init__(self, args):
            self.args = self.ArgModel.model_validate(args)


    class CopyOperator(BaseOperator):
        """Class for copying a single numeric column."""


    class RecodeOperator(BaseOperator):
        """Operator for recoding categorical values."""

        class ArgModel(BaseModel):
            columns: str
            weights: dict[str, float | int]


    class PercentageOperator(BaseOperator):
        """Operator for computing percentages."""

        class ArgModel(BaseModel):
            numerator: str
            denominator: str
    return PercentageOperator, RecodeOperator


@app.cell
def _(blueprint):
    op_config = blueprint.indicators[1]
    op_config.model_dump()
    return (op_config,)


@app.cell
def _(RecodeOperator, op_config):
    rec_op = RecodeOperator(op_config.args)
    rec_op.args
    return


@app.cell
def _(PercentageOperator, blueprint):
    pct_op = PercentageOperator(blueprint.indicators[2].args)
    pct_op.args.model_dump()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
