import itertools
import pathlib
from multiprocessing import Pool
from pathlib import Path

import PyPDF2
import click
import pandas as pd
# camelot-py
from camelot import read_pdf
from camelot.core import TableList, Table
from pandas import DataFrame


def _raw_read_tables(page: int) -> TableList:
    """
    Extract all tables from a given page of the pdf
    :param page: page to load tables from
    :return: list of all found tables
    """
    return read_pdf('Modulkatalog_2023_Wintersemester.pdf', pages=str(page))


def _get_last_page_number(pdf_file: Path) -> int:
    """
    Get the last page index of the pdf file
    :param pdf_file: path to pdf file to get last page index from
    :return: last page number (1-indexed)
    """

    with open(pdf_file, 'rb') as f:
        return PyPDF2.PdfFileReader(f).getNumPages()


def _get_raw_tables(pdf_file: Path, start_page: int = 0, end_page: int = None) \
    -> list[Table]:
    """
    Load all tables from the pdf file

    :param pdf_file: path to pdf file to get tables from
    :param start_page: page to start reading from (0-indexed)
    :param end_page: page to stop reading at
    :return: list of all tables in order of appearance in the document
    """

    if end_page is None:
        end_page = _get_last_page_number(pdf_file)

    with Pool(8) as p:
        raw_tables: list[list[TableList]] = p.map(_raw_read_tables, range(start_page, end_page))

    # flatten array before returning. See: https://note.nkmk.me/en/python-list-flatten/
    return list(itertools.chain.from_iterable(raw_tables))


def _join_split_tables(list_of_tables: list[Table], first_key_name: str, last_key_name: str) -> list[DataFrame]:
    """
    Join tables that are split across multiple pages

    Function asserts table is structured as follows:

    +----------------+-------------+
    | first_key_name | first value |
    +----------------+-------------+
    | ...            | ...         |
    +----------------+-------------+
    | last_key_name  | last value  |
    +----------------+-------------+


    :param first_key_name: name of first key in table. This will indicate the start of a new table
    :param last_key_name: name of last key in. This will indicate the end of a table
    :param list_of_tables: list of tables to join
    :return: list of no longer split tables
    """

    result: list[DataFrame] = []

    current_table: DataFrame | None = None
    for table in list_of_tables:

        # clean up messy key columns
        table_df: DataFrame = table.df
        table_df[0] = table_df[0].str.replace("\n *", '', regex=True).str.strip().to_frame()
        table_df[1] = table_df[1].str.replace("\n", '', regex=True).str.strip().to_frame()

        for index, row in table_df.iterrows():
            if row[0] == first_key_name:
                if current_table is not None:
                    result.append(current_table)

                # create new table with first row being the current row
                current_table = pd.DataFrame(columns=table_df.columns, data=[row])
            elif row[0] == '':
                if current_table is not None:
                    current_table.iloc[-1, -1] = str(current_table.iloc[-1, -1]) + " " + str(row[1])
                else:
                    result[-1].iloc[-1, -1] = str(result[-1].iloc[-1, -1]) + " " + str(row[1])
            else:
                current_table = pd.concat([current_table, row.to_frame().T], ignore_index=True)

    if current_table is not None:
        result.append(current_table)
    return result


def _to_database_representation(joined_tables: list[DataFrame]) -> DataFrame:
    res = pd.DataFrame()
    for joined_table in joined_tables:
        column_names = joined_table.T.iloc[0]
        joined_table = joined_table.T[1:]
        joined_table.columns = column_names

        print(joined_table)

        res = pd.concat([res, joined_table], ignore_index=True)

    return res


@click.command()
@click.option('--import_path', '-i',
              type=click.Path(exists=True, readable=True, dir_okay=False, path_type=pathlib.Path))
def data_loader(import_path: Path):
    raw_tables = _get_raw_tables(Path('Modulkatalog_2023_Wintersemester.pdf'), start_page=2)
    joined_tables = _join_split_tables(raw_tables, 'Modulbezeichnung:', 'Literatur:')

    table_representation = _to_database_representation(joined_tables)
    table_representation.to_csv("out.csv", index=False)
