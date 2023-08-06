import pandas as pd

STRING_VALUE_LENGTH = 75


def pystr(df: pd.DataFrame) -> None:

    print(f"Pandas DataFrame {df.shape[0]} obs. of {df.shape[1]} variables")
    n_values = 50 if df.shape[0] > 50 else df.shape[0]

    for col_name in df.columns:

        str_dtype = _parse_dtypes(df, col_name)

        if "float" in str_dtype:
            rounded_vals_str = [round(x, 1) if x > 1 else round(x, 2) for x in df[col_name].values[:n_values]]
            values_str = ", ".join([str(x) for x in [rounded_vals_str]])
        if "str" in str_dtype:
            values_str = ", ".join([f"\042{x}\042" for x in df[col_name].values[:n_values]])
        else:
            values_str = ", ".join([str(x) for x in df[col_name].values[:n_values]])

        if len(values_str) > STRING_VALUE_LENGTH:
            values_str = f"{values_str[:STRING_VALUE_LENGTH]}..."

        print(f"$ {_parse_string(col_name)}: {str_dtype} {values_str}")


def _parse_string(string_name: str, string_size: int = 18) -> str:

    if len(string_name) > string_size:
        return f"{string_name[:string_size-2]}.."

    if len(string_name) < string_size:
        return string_name.ljust(string_size)

    return string_name


def _contains(string: str, string_list: list) -> bool:

    return any([x in string for x in string_list])


SAMPLE_SIZE = 30
PRIMITIVE_TYPES = ["int", "float", "bool"]


def _parse_dtypes(df: pd.DataFrame, col_name: str) -> str:

    data_type = str(df.dtypes[col_name])

    if _contains(data_type, PRIMITIVE_TYPES):
        return _parse_string(data_type, 12)

    classes = list(dict.fromkeys([str(type(x)) for x in df[col_name].sample(SAMPLE_SIZE).dropna()]))

    if len(classes) == 0:
        return _parse_string("Null", 12)
    if len(classes) == 1:
        return _parse_string(classes[0].replace("<class '", "").replace("'>", ""), 12)

    return _parse_string(f"{len(classes)} types", 12)
