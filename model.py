import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import yaml
    import logging

    from typing import Self, Literal

    from pydantic import BaseModel, Field, AliasChoices
    return AliasChoices, BaseModel, Field, Literal, Self, yaml


@app.cell
def _():
    blueprint_yaml = """
    Main:
        Top level 1: 0.5
        Top level 2: 0.5

    Top level 1:
        _aggregate: mean
        Sub level 1.1: 0.3
        Sub level 1.2: 0.7

    Sub level 1.1:
        _fillna: null
        Indicator 1.1.A: 0.2
        Indicator 1.1.B: 0.8

    Sub level 1.2:
        Indicator 1.2.A: 1.0

    Top level 2:
        Indicator 2.A: 1.0
    """
    return (blueprint_yaml,)


@app.cell
def _(blueprint_yaml, yaml):
    blueprint = yaml.safe_load(blueprint_yaml)
    blueprint
    return (blueprint,)


@app.cell
def _():
    # Assume indicator scores have been built.
    indicators = {
        "Indicator 1.1.A": 1,
        "Indicator 1.1.B": 2,
        "Indicator 1.2.A": 3,
        "Indicator 2.A": None,
    }
    return (indicators,)


@app.cell
def _(AliasChoices, BaseModel, Field, Literal, Self):
    class ModelItem(BaseModel):
        """Class for items in the risk model."""

        name: str
        weight: int | float = 1

        value: float | None = None
        score: float | None = None

        fillna: int | float | None = Field(
            alias=AliasChoices("_fillna", "_fill_na"), default=None
        )
        aggregate: Literal["mean", "sum"] | None = Field(
            alias=AliasChoices("_agg", "_aggregate"), default=None
        )

        children: list[Self] | None = None

        @staticmethod
        def _mean(scores: list) -> float:
            """Compute mean of scores, ignoring missing values."""
            # Ignore missing values.
            filtered = [_ for _ in scores if _ is not None]
            if not filtered:
                return None
            return sum(filtered) / len(filtered)

        @staticmethod
        def _sum(scores: list) -> float:
            """Compute sum of scores, ignoring missing values."""
            filtered = [_ for _ in scores if _ is not None]
            return sum(filtered)

        def resolve(self) -> float:
            """Recursively compute scores for all items in the model.

            Returns
            -------
            float
                The score for the root node of the model.
            """
            # Process any child items.
            if self.children:
                child_scores = [child.resolve() for child in self.children]

                if self.aggregate == "mean":
                    self.score = self._mean(child_scores)
                else:
                    self.score = self._sum(child_scores)
                return self.score

            # Compute own weighted score.
            else:
                # Handle missing value.
                if self.value is None:
                    if self.fillna is None:
                        self.score = None
                    else:
                        self.score = self.weight * self.fillna

                # Process normal values.
                else:
                    self.score = self.weight * self.value

                return self.score
    return (ModelItem,)


@app.cell
def _(ModelItem, blueprint, indicators):
    def build_tree(name, weight=1, aggregate: str = "sum", fillna: int | float | None = 0):
        """Build items in the model node tree.

        Parameters
        ----------
        aggregate: {"sum", "mean"}
            Aggregation method to combine scores from children.
            Can be overridden with `aggregate` in the model blueprint.
        fill_na: float or None
            Fill value for missing values, None to disable filling.
        """
        if name in blueprint:
            print(f"Processing item: {name}")

            children = []
            self_aggregate = aggregate
            self_fillna = fillna
            for child, setting in blueprint[name].items():
                if child == "_aggregate":
                    self_aggregate = setting
                elif child == "_fillna":
                    self_fillna = setting
                else:
                    print(f"- Processing child: {child}")
                    children.append(build_tree(name=child, weight=setting, aggregate=aggregate, fillna=fillna))
        
            return ModelItem(name=name, weight=weight, children=children, _aggregate=self_aggregate, _fillna=self_fillna)

        elif name in indicators:
            print(f"Processing indicator: {name}")
            return ModelItem(name=name, weight=weight, value=indicators[name])

        else:
            raise RuntimeError(f"Item {name} was not found in the model blueprint or indicators!")
    return (build_tree,)


@app.cell
def _(build_tree):
    # Build the model tree, starting at "Main".
    risk_model = build_tree("Main")
    risk_model.model_dump()
    return (risk_model,)


@app.cell
def _(risk_model):
    risk_model.resolve()
    return


@app.cell
def _(risk_model):
    risk_model.model_dump()
    return


if __name__ == "__main__":
    app.run()
