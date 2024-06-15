from datetime import datetime as dt
from pathlib import Path

import click

from llm_engineering.interfaces.orchestrator.pipelines import (
    digital_data_etl,
    feature_engineering,
    generate_instruct_datasets
)


@click.command(
    help="""
LLM Engineering project CLI v0.0.1. 

Main entry point for the pipeline execution. 
This entrypoint is where everything comes together.

Run the ZenML LLM Engineering project pipelines with various options.

Run a pipeline with the required parameters. This executes
all steps in the pipeline in the correct order using the orchestrator
stack component that is configured in your active ZenML stack.

Examples:

  \b
  # Run the pipeline with default options
  python run.py
               
  \b
  # Run the pipeline without cache
  python run.py --no-cache
  
  \b
  # Run only the ETL pipeline
  python run.py --only-etl

"""
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable caching for the pipeline run.",
)
@click.option(
    "--run-etl",
    is_flag=True,
    default=False,
    help="Whether to run the ETL pipeline.",
)
@click.option(
    "--run-feature-engineering",
    is_flag=True,
    default=False,
    help="Whether to run the FE pipeline.",
)
@click.option(
    "--run-create-dataset",
    is_flag=True,
    default=False,
    help="Whether to run the create dataset pipeline.",
)
def main(
    no_cache: bool = False,
    run_etl: bool = False,
    run_feature_engineering: bool = False,
    run_create_dataset: bool = False,
) -> None:
    assert (
        run_etl or run_feature_engineering or run_create_dataset
    ), "Please specify a pipeline to run."

    pipeline_args = {
        "enable_cache": not no_cache,
    }
    root_dir = Path(__file__).resolve().parent.parent.parent.parent

    if run_etl:
        run_args_etl = {}
        pipeline_args["config_path"] = (
            root_dir
            / "configs"
            / "digital_data_etl_paul_iusztin.yaml"
        )
        pipeline_args["run_name"] = (
            f"digital_data_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )
        digital_data_etl.with_options(**pipeline_args)(**run_args_etl)

    if run_feature_engineering:
        run_args_fe = {}
        pipeline_args["config_path"] = (
            root_dir
            / "configs"
            / "feature_engineering.yaml"
        )
        pipeline_args["run_name"] = (
            f"feature_engineering_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )
        feature_engineering.with_options(**pipeline_args)(**run_args_fe)

    if run_create_dataset:
        run_args_cd = {}
        pipeline_args["config_path"] = (
            root_dir 
            / "configs" 
            / "generate_instruct_datasets.yaml"
        )
        pipeline_args["run_name"] = (
            f"generate_instruct_datasets_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        )
        generate_instruct_datasets.with_options(**pipeline_args)(**run_args_cd)


if __name__ == "__main__":
    main()