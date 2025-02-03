from ast import literal_eval
from logging import Logger
from os import makedirs

import pandas as pd
from django.conf import settings
from django.db.models import Model
from django.utils.timezone import now
from django_admin_bulk_io.utils.constants import FILE_NAME_TEMPLATE


def log_messages(error: str, logger: Logger) -> None:
    """
    This method logs the errors.
    :param errors: list of errors
    """
    logger(error)


def generate_csv_from_data(data: list):
    """
    generate csv from data dict
    :param data: list
    :return: str
    """
    return pd.DataFrame(data).to_csv(index=False)


def get_model_fields_info(model: Model) -> tuple[list[str], list[str]]:
    """
    This method returns required & optional fields for given model.
    :param model: model instance
    :return: tuple of required and optional fields list
    """
    required = set()
    optional = set()
    for field in model._meta.get_fields():
        try:
            if field.field.blank is False and field.field.null is False:
                required.add(field.field)
            else:
                optional.add(field.field)
        except AttributeError:
            if field.blank is False and field.null is False:
                required.add(field)
            else:
                optional.add(field)
    if model._meta.many_to_many:
        for field in model._meta.many_to_many:
            if field.blank is False and field.null is False:
                required.add(field)
            else:
                optional.add(field)
    return list(required), list(optional)


def generate_csv_filename() -> str:
    """
    generate csv filename with timestamp
    :return: str
    """

    return f"bulk_io_{now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"


def generate_csv_from_serialized_data(data: dict) -> str:
    """
    use pandas to generate csv from queryset
    :param data: dict
    :return: str
    """
    df = pd.DataFrame.from_records(data=data)
    return df.to_csv(index=False)


def save_csv_file_in_base_dir(csv_str: str, info: tuple) -> None:
    """
    save csv string in base dir handle exceptions
    :param csv_str: str
    :param app_label: str
    :param model_name: str
    :return: None
    """
    filename = generate_csv_filename()
    file_path = FILE_NAME_TEMPLATE % (settings.BASE_DIR, *info)
    try:
        makedirs(file_path)
    except FileExistsError:
        pass
    full_path = f"{file_path}{filename}"

    def create_file():
        with open(full_path, "w") as f:
            f.write(csv_str)

    create_file()


def clean_csv_data(csv_str: str, required: list, optional: list, model: Model):
    """
    clean `CSV` data
    """
    df = pd.read_csv(csv_str)
    # Drop duplicates
    df.drop_duplicates(inplace=True)
    if model._meta.pk.name in df.columns:
        # drop primary key column
        df.drop(columns=[model._meta.pk.name], inplace=True)
    for field in df.columns:
        # iterate field of dataframe
        if field not in [field.name for field in required + optional]:
            # if field not in required & optional then drop column with field
            df.drop(columns=[field], inplace=True)
    for field in required + optional:
        # iterate required & optional fields
        if field.name in df.columns:
            # if field in dataframe
            if field.many_to_many:
                # if field is many to many then literal_eval
                df[field.name] = df[field.name].apply(lambda x: literal_eval(x))
    for field in optional:
        # iterate options fields
        if field.name in df.columns:
            # if field in dataframe and is nan then drop
            if df[field.name].isna().any():
                df.drop(columns=[field.name], inplace=True)
    return df


def validate_data_from_csv_file(model: Model, csv_str: str) -> dict:
    """
    import & clean csv file data for optional field and returns dict of data

    :param model: Model
    :param csv_file: str
    :return: dict
    """
    required, optional = get_model_fields_info(model=model)
    df = clean_csv_data(
        csv_str=csv_str, required=required, optional=optional, model=model
    )
    return df.to_dict(orient="records")


def filter_data_from_csv(model: Model, csv_str: str) -> dict:
    """
    import & clean csv file data and returns dict of data
    :param model: Model
    :param csv_file: str
    :param fields: list
    :return: dict
    """
    required, optional = get_model_fields_info(model=model)
    df = clean_csv_data(
        csv_str=csv_str, required=required, optional=optional, model=model
    )
    for field in required:
        if field.name in df.columns:
            df.dropna(subset=[field.name], inplace=True)
    return df.to_dict(orient="records")
