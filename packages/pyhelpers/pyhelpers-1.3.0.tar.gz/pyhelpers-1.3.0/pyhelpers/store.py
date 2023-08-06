"""
Saving and loading file-like objects.
"""

import json
import os
import pathlib
import pickle
import subprocess
import zipfile

import pandas as pd

from .ops import confirmed


def _get_specific_filepath_info(path_to_file, verbose=False, verbose_end=" ... ", ret_info=False):
    """
    Get information about the path of a file.

    :param path_to_file: path where a file is saved
    :type path_to_file: str or pathlib.Path
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param verbose_end: a string passed to ``end`` for ``print``, defaults to ``" ... "``
    :type verbose_end: str
    :param ret_info: whether to return the file path information, defaults to ``False``
    :type ret_info: bool
    :return: a relative path and a filename (if ``ret_info=True``)
    :rtype: tuple

    **Examples**::

        from pyhelpers.dir import cd
        from pyhelpers.store import _get_specific_filepath_info

        file_path = cd()
        try:
            _get_specific_filepath_info(file_path, verbose=True)
        except AssertionError as e:
            print(e)
        # The input for `path_to_file` may not be a file path.

        file_path = cd("test_store.py")
        _get_specific_filepath_info(file_path, verbose=True)
        print("Pass.")
        # Saving "test_store.py" ... Pass.

        file_path = cd("tests", "test_store.py")
        _get_specific_filepath_info(file_path, verbose=True)
        print("Pass.")
        # Updating "test_store.py" at "tests\\" ... Pass.

    :meta private:
    """

    abs_path_to_file = pathlib.Path(path_to_file).absolute()
    assert not abs_path_to_file.is_dir(), "The input for `path_to_file` may not be a file path."

    filename = pathlib.Path(abs_path_to_file).name if abs_path_to_file.suffix else ""

    try:
        rel_path = pathlib.Path(os.path.relpath(abs_path_to_file.parent))

        if rel_path == rel_path.parent:
            rel_path = abs_path_to_file.parent
            msg_fmt = "{} \"{}\""
        else:
            msg_fmt = "{} \"{}\" {} \"{}\\\""
            # The specified path exists?
            os.makedirs(abs_path_to_file.parent, exist_ok=True)

    except ValueError:
        if verbose == 2:
            warn_msg = "Warning: \"{}\" is outside the current working directory".format(
                str(abs_path_to_file.parent))
            print(warn_msg)

        rel_path = abs_path_to_file.parent
        msg_fmt = "{} \"{}\""

    if verbose:
        if os.path.isfile(abs_path_to_file):
            status_msg, prep = "Updating", "at"
        else:
            status_msg, prep = "Saving", "to"

        if verbose_end:
            verbose_end_ = verbose_end
        else:
            verbose_end_ = "\n"

        if rel_path == rel_path.parent:
            print(msg_fmt.format(status_msg, filename), end=verbose_end_)
        else:
            print(msg_fmt.format(status_msg, filename, prep, rel_path), end=verbose_end_)

    if ret_info:
        return rel_path, filename


""" == Save data ============================================================================= """


def save(data, path_to_file, warning=False, **kwargs):
    """
    Save data to a file of specific format.

    :param data: data that could be saved to
        a `CSV`_, `Microsoft Excel`_, `Feather`_, `JSON`_ or `pickle`_ file
    :type data: any
    :param path_to_file: path where a file is saved
    :type path_to_file: str
    :param warning: whether to show a warning messages, defaults to ``False``
    :type warning: bool
    :param kwargs: [optional] parameters of :py:func:`pyhelpers.store.save_spreadsheet`,
        :py:func:`pyhelpers.store.save_feather`, :py:func:`pyhelpers.store.save_json` or
        :py:func:`pyhelpers.store.save_pickle`

    .. _`CSV`: https://en.wikipedia.org/wiki/Comma-separated_values
    .. _`Microsoft Excel`: https://en.wikipedia.org/wiki/Microsoft_Excel
    .. _`Feather`: https://arrow.apache.org/docs/python/feather.html
    .. _`JSON`: https://www.json.org/json-en.html
    .. _`Pickle`: https://docs.python.org/3/library/pickle.html

    **Examples**::

        >>> from pyhelpers.store import save
        >>> from pyhelpers.dir import cd
        >>> import pandas

        >>> data_dir = cd("tests\\data")

        >>> dat_list = [(530034, 180381),
        ...             (406689, 286822),
        ...             (383819, 398052),
        ...             (582044, 152953)]

        >>> idx = ['London', 'Birmingham', 'Manchester', 'Leeds']
        >>> col = ['Easting', 'Northing']

        >>> dat = pandas.DataFrame(dat_list, idx, col)
        >>> dat
                    Easting  Northing
        London       530034    180381
        Birmingham   406689    286822
        Manchester   383819    398052
        Leeds        582044    152953

        >>> dat_file_path = cd(data_dir, "dat.txt")
        >>> save(dat, dat_file_path, verbose=True)
        Saving "dat.txt" to "tests\\data\\" ... Done.

        >>> dat_file_path = cd(data_dir, "dat.csv")
        >>> save(dat, dat_file_path, verbose=True)
        Saving "dat.csv" to "tests\\data\\" ... Done.

        >>> dat_file_path = cd(data_dir, "dat.xlsx")
        >>> save(dat, dat_file_path, verbose=True)
        Saving "dat.xlsx" to "tests\\data\\" ... Done.

        >>> dat_file_path = cd(data_dir, "dat.pickle")
        >>> save(dat, dat_file_path, verbose=True)
        Saving "dat.pickle" to "tests\\data\\" ... Done.

        >>> dat_file_path = cd(data_dir, "dat.feather")
        >>> # `save(data_[, ...])` may produce an error due to the index of `dat`
        >>> save(dat.reset_index(), dat_file_path, verbose=True)
        Saving "dat.feather" to "tests\\data\\" ... Done.
    """

    # Make a copy the original data
    data_ = data.copy()
    if isinstance(data, pd.DataFrame) and data.index.nlevels > 1:
        data_.reset_index(inplace=True)

    # Save the data according to the file extension
    if path_to_file.endswith((".csv", ".xlsx", ".xls", ".txt")):
        save_spreadsheet(data_, path_to_file, **kwargs)

    elif path_to_file.endswith(".feather"):
        save_feather(data_, path_to_file, **kwargs)

    elif path_to_file.endswith(".json"):
        save_json(data_, path_to_file, **kwargs)

    elif path_to_file.endswith(".pickle"):
        save_pickle(data_, path_to_file, **kwargs)

    else:
        if warning:
            print("Note that the current file extension is not recognisable by this \"save()\".")

        if confirmed("To save \"{}\" as a .pickle file? ".format(os.path.basename(path_to_file))):
            save_pickle(data_, path_to_file, **kwargs)


# Pickle files

def save_pickle(pickle_data, path_to_pickle, mode='wb', verbose=False, **kwargs):
    """
    Save data to a `pickle <https://docs.python.org/3/library/pickle.html>`_ file.

    :param pickle_data: data that could be dumped by the built-in module `pickle.dump`_
    :type pickle_data: any
    :param path_to_pickle: path where a pickle file is saved
    :type path_to_pickle: str
    :param mode: mode to `open`_ file, defaults to ``'wb'``
    :type mode: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `pickle.dump`_

    .. _`open`: https://docs.python.org/3/library/functions.html#open
    .. _`pickle.dump`: https://docs.python.org/3/library/pickle.html#pickle.dump

    **Example**::

        >>> from pyhelpers.store import save_pickle
        >>> from pyhelpers.dir import cd

        >>> pickle_dat = 1
        >>> pickle_path = cd("tests\\data", "dat.pickle")

        >>> save_pickle(pickle_dat, pickle_path, verbose=True)
        Saving "dat.pickle" to "tests\\data\\" ... Done.
    """

    _get_specific_filepath_info(path_to_pickle, verbose=verbose, ret_info=False)

    try:
        pickle_out = open(path_to_pickle, mode=mode)
        pickle.dump(pickle_data, pickle_out, **kwargs)
        pickle_out.close()
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e))


# Joblib

def save_joblib(joblib_data, path_to_joblib, verbose=False, **kwargs):
    """
    Save data to a `joblib <https://pypi.org/project/joblib/>`_ file.

    :param joblib_data: data that could be dumped by `joblib.dump`_
    :type joblib_data: any
    :param path_to_joblib: path where a pickle file is saved
    :type path_to_joblib: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `joblib.dump`_

    .. _`joblib.dump`: https://joblib.readthedocs.io/en/latest/generated/joblib.dump.html

    **Example**::

        >>> from pyhelpers.store import save_joblib
        >>> from pyhelpers.dir import cd
        >>> import numpy

        >>> joblib_dat = numpy.random.rand(100, 100)
        >>> joblib_path = cd("tests\\data", "dat.joblib")

        >>> save_joblib(joblib_dat, joblib_path, verbose=True)
        Saving "dat.joblib" to "tests\\data\\" ... Done.
    """

    _get_specific_filepath_info(path_to_joblib, verbose=verbose, ret_info=False)

    try:
        import joblib

        joblib.dump(value=joblib_data, filename=path_to_joblib, **kwargs)
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e))


# Spreadsheets

def save_spreadsheet(spreadsheet_data, path_to_spreadsheet, index=False, engine=None, delimiter=',',
                     verbose=False, **kwargs):
    """
    Save data to a `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ or
    an `Microsoft Excel <https://en.wikipedia.org/wiki/Microsoft_Excel>`_ file.

    The file extension can be `".txt"`, `".csv"`, `".xlsx"` or `".xls"`;
    engines can include: `xlsxwriter`_ (for .xlsx) and `openpyxl`_ (for .xlsx/.xlsm).

    :param spreadsheet_data: data that could be saved as a spreadsheet
        (e.g. with a file extension ".xlsx" or ".csv")
    :type spreadsheet_data: pandas.DataFrame
    :param path_to_spreadsheet: path where a spreadsheet is saved
    :type path_to_spreadsheet: str or None
    :param index: whether to include the index as a column, defaults to ``False``
    :type index: bool
    :param engine: options include ``'openpyxl'`` for latest Excel file formats,
        ``'xlrd'`` for .xls ``'odf'`` for OpenDocument file formats (.odf, .ods, .odt), and
        ``'pyxlsb'`` for Binary Excel files; defaults to ``None``
    :type engine: str or None
    :param delimiter: separator for saving a `".xlsx"` (or `".xls"`) file as a `".csv"` file,
        defaults to ``','``
    :type delimiter: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `pandas.DataFrame.to_excel`_ or `pandas.DataFrame.to_csv`_

    .. _`xlsxwriter`: https://pypi.org/project/XlsxWriter/
    .. _`openpyxl`: https://pypi.org/project/openpyxl/
    .. _`pandas.DataFrame.to_excel`:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
    .. _`pandas.DataFrame.to_csv`:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html

    **Examples**::

        >>> from pyhelpers.store import save_spreadsheet
        >>> import pandas
        >>> from pyhelpers.dir import cd

        >>> spreadsheet_dat = pandas.DataFrame({'Col1': 1, 'Col2': 2}, index=['data'])
        >>> spreadsheet_dat
              Col1  Col2
        data     1     2

        >>> spreadsheet_path = cd("tests\\data", "dat.csv")
        >>> save_spreadsheet(spreadsheet_dat, spreadsheet_path, verbose=True)
        Saving "dat.csv" to "tests\\data\\" ... Done.

        >>> spreadsheet_path = cd("tests\\data", "dat.xls")
        >>> save_spreadsheet(spreadsheet_dat, spreadsheet_path, verbose=True)
        Saving "dat.xls" to "tests\\data\\" ... Done.

        >>> spreadsheet_path = cd("tests\\data", "dat.xlsx")
        >>> save_spreadsheet(spreadsheet_dat, spreadsheet_path, verbose=True)
        Saving "dat.xlsx" to "tests\\data\\" ... Done.
    """

    _, spreadsheet_filename = _get_specific_filepath_info(
        path_to_file=path_to_spreadsheet, verbose=verbose, ret_info=True)

    try:  # to save the data
        if spreadsheet_filename.endswith(".xlsx"):  # a .xlsx file
            spreadsheet_data.to_excel(
                excel_writer=path_to_spreadsheet, index=index, engine=engine, **kwargs)

        elif spreadsheet_filename.endswith(".xls"):  # a .xls file
            if engine is None or engine == 'xlwt':
                engine = 'openpyxl'
            spreadsheet_data.to_excel(
                excel_writer=path_to_spreadsheet, index=index, engine=engine, **kwargs)

        elif spreadsheet_filename.endswith((".csv", ".txt")):  # a .csv file
            spreadsheet_data.to_csv(
                path_or_buf=path_to_spreadsheet, index=index, sep=delimiter, **kwargs)

        else:
            raise AssertionError('File extension must be ".txt", ".csv", ".xlsx" or ".xls"')

        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e.args[0])) if verbose else ""


def save_multiple_spreadsheets(spreadsheets_data, sheet_names, path_to_spreadsheet, mode='w',
                               index=False, confirmation_required=True, verbose=False, **kwargs):
    """
    Save data to a multi-sheet `Microsoft Excel`_ file.

    The file extension can be `".xlsx"` or `".xls"`.

    :param spreadsheets_data: a sequence of pandas.DataFrame
    :type spreadsheets_data: list or tuple or iterable
    :param sheet_names: all sheet names of an Excel workbook
    :type sheet_names: list or tuple or iterable
    :param path_to_spreadsheet: path where a spreadsheet is saved
    :type path_to_spreadsheet: str
    :param mode: mode to write to an Excel file; ``'w'`` (default) for 'write' and ``'a'`` for 'append'
    :type mode: str
    :param index: whether to include the index as a column, defaults to ``False``
    :type index: bool
    :param confirmation_required: whether to prompt a message for confirmation to proceed,
        defaults to ``True``
    :type confirmation_required: bool
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `pandas.ExcelWriter`_

    .. _`Microsoft Excel`: https://en.wikipedia.org/wiki/Microsoft_Excel
    .. _pandas.ExcelWriter:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html

    **Examples**::

        >>> from pyhelpers.store import save_multiple_spreadsheets
        >>> import numpy
        >>> import pandas
        >>> from pyhelpers.dir import cd

        >>> xy_array = numpy.array([(530034, 180381),   # London
        ...                         (406689, 286822),   # Birmingham
        ...                         (383819, 398052),   # Manchester
        ...                         (582044, 152953)])  # Leeds
        >>> idx = ['London', 'Birmingham', 'Manchester', 'Leeds']
        >>> col = ['Easting', 'Northing']

        >>> dat1 = pandas.DataFrame(xy_array, idx, col)
        >>> dat1
                    Easting  Northing
        London       530034    180381
        Birmingham   406689    286822
        Manchester   383819    398052
        Leeds        582044    152953

        >>> dat2 = dat1.T
        >>> dat2
                  London  Birmingham  Manchester   Leeds
        Easting   530034      406689      383819  582044
        Northing  180381      286822      398052  152953

        >>> ss_dat = [dat1, dat2]  # spreadsheets_data = ss_dat
        >>> s_names = ['TestSheet1', 'TestSheet2']  # sheet_names = s_names
        >>> ss_path = cd("tests\\data", "dat.xlsx")  # path_to_spreadsheet = ss_path

        >>> save_multiple_spreadsheets(ss_dat, s_names, ss_path, index=True, verbose=True)
        Saving "dat.xlsx" to "tests\\data\\" ...
            'TestSheet1' ... Done.
            'TestSheet2' ... Done.

        >>> save_multiple_spreadsheets(ss_dat, s_names, ss_path, mode='a', index=True, verbose=True)
        Updating "dat.xlsx" at "tests\\data\\" ...
            'TestSheet1' ... This sheet already exists; [pass]|new|replace: new
                saved as 'TestSheet11' ... Done.
            'TestSheet2' ... This sheet already exists; [pass]|new|replace: new
                saved as 'TestSheet21' ... Done.

        >>> save_multiple_spreadsheets(ss_dat, s_names, ss_path, mode='a', index=True,
        ...                            confirmation_required=False, verbose=True)
        Updating "dat.xlsx" at "tests\\dataz\" ...
            'TestSheet1' ... Failed. Sheet 'TestSheet1' already exists and if_sheet_exists is ...
            'TestSheet2' ... Failed. Sheet 'TestSheet2' already exists and if_sheet_exists is ...

        >>> save_multiple_spreadsheets(ss_dat, s_names, ss_path, mode='a', index=True,
        ...                            confirmation_required=False, verbose=True,
        ...                            if_sheet_exists='replace')
        Updating "dat.xlsx" at "tests\\data\\" ...
            'TestSheet1' ... Done.
            'TestSheet2' ... Done.
    """

    assert path_to_spreadsheet.endswith(".xlsx") or path_to_spreadsheet.endswith(".xls")

    _get_specific_filepath_info(path_to_spreadsheet, verbose=verbose, ret_info=False)

    if os.path.isfile(path_to_spreadsheet) and mode == 'a':
        excel_file = pd.ExcelFile(path_or_buffer=path_to_spreadsheet)
        cur_sheet_names = excel_file.sheet_names
        excel_file.close()
    else:
        cur_sheet_names = []

    engine = 'openpyxl' if mode == 'a' else None
    excel_writer = pd.ExcelWriter(path=path_to_spreadsheet, engine=engine, mode=mode, **kwargs)

    def _write_excel():
        try:
            sheet_data.to_excel(excel_writer, sheet_name=sheet_name, index=index)

            try:
                sheet_name_ = excel_writer.sheets[sheet_name].get_name()
            except AttributeError:
                sheet_name_ = excel_writer.sheets[sheet_name].title

            if sheet_name_ in sheet_names:
                msg_ = "Done."
            else:
                msg_ = "saved as '{}' ... Done. ".format(sheet_name_)

            print(msg_) if verbose else ""

        except Exception as e:
            print("Failed. {}".format(e))

    print("") if verbose else ""
    for sheet_data, sheet_name in zip(spreadsheets_data, sheet_names):
        # sheet_data, sheet_name = spreadsheets_data[0], sheet_names[0]
        print("\t'{}'".format(sheet_name), end=" ... ") if verbose else ""

        if (sheet_name in cur_sheet_names) and confirmation_required:
            if_sheet_exists = input(f"This sheet already exists; [pass]|new|replace: ")
            if if_sheet_exists != 'pass':
                excel_writer.if_sheet_exists = if_sheet_exists
                print("\t\t", end="")
                # suffix_msg = "(Note that a suffix has been added to the sheet name.)"
                _write_excel()
        else:
            _write_excel()

    excel_writer.close()


# JSON files

def save_json(json_data, path_to_json, method=None, verbose=False, **kwargs):
    """
    Save data to a `JSON <https://www.json.org/json-en.html>`_ file.

    :param json_data: data that could be dumped by as a JSON file
    :type json_data: any json data
    :param path_to_json: path where a json file is saved
    :type path_to_json: str
    :param method: an open-source module used for JSON serialization, options include
        ``None`` (default, for the built-in `json module`_), ``'orjson'`` (for `orjson`_) and
        ``'rapidjson'`` (for `python-rapidjson`_)
    :type method: str or None
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `json.dump`_ (if ``method=None``),
        `orjson.dumps`_ (if ``method='orjson'``), or `rapidjson.dump`_ (if ``method='rapidjson'``)

    .. _`json module`: https://docs.python.org/3/library/json.html
    .. _`orjson`: https://pypi.org/project/orjson/
    .. _`python-rapidjson`: https://pypi.org/project/python-rapidjson
    .. _`json.dump`: https://docs.python.org/3/library/json.html#json.dump
    .. _`orjson.dumps`: https://github.com/ijl/orjson#serialize
    .. _`rapidjson.dump`: https://python-rapidjson.readthedocs.io/en/latest/dump.html

    **Example**::

        >>> from pyhelpers.store import save_json
        >>> from pyhelpers.dir import cd

        >>> json_dat = {'a': 1, 'b': 2, 'c': 3}
        >>> json_path = cd("tests\\data", "dat.json")

        >>> save_json(json_dat, json_path, indent=4, verbose=True)
        Saving "dat.json" to "tests\\data\\" ... Done.
    """

    _get_specific_filepath_info(path_to_json, verbose=verbose, ret_info=False)

    try:
        if method == 'orjson':
            import orjson

            json_out = open(path_to_json, mode='wb')
            json_out.write(orjson.dumps(json_data, **kwargs))

        else:
            json_out = open(path_to_json, mode='w')

            if method == 'rapidjson':
                import rapidjson

                rapidjson.dump(json_data, json_out, **kwargs)

            else:
                json.dump(json_data, json_out, **kwargs)

        json_out.close()
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e))


# Feather files

def save_feather(feather_data, path_to_feather, verbose=False):
    """
    Save data frame to a `Feather <https://arrow.apache.org/docs/python/feather.html>`_ file.

    :param feather_data: a data frame to be saved as a feather-formatted file
    :type feather_data: pandas.DataFrame
    :param path_to_feather: path where a feather file is saved
    :type path_to_feather: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int

    **Example**::

        >>> from pyhelpers.store import save_feather
        >>> import pandas
        >>> from pyhelpers.dir import cd

        >>> feather_dat = pandas.DataFrame({'Col1': 1, 'Col2': 2}, index=[0])
        >>> feather_dat
           Col1  Col2
        0     1     2

        >>> feather_path = cd("tests\\data", "dat.feather")

        >>> save_feather(feather_dat, feather_path, verbose=True)
        Saving "dat.feather" to "tests\\data\\" ... Done.
    """

    assert isinstance(feather_data, pd.DataFrame)

    _get_specific_filepath_info(path_to_feather, verbose=verbose, ret_info=False)

    try:
        feather_data.to_feather(path_to_feather)
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e)) if verbose else ""


# Images

def save_fig(path_to_fig_file, dpi=None, verbose=False, conv_svg_to_emf=False, **kwargs):
    """
    Save a figure object to a file of a supported file format.

    This function relies on `matplotlib.pyplot.savefig`_ (and `Inkscape`_).

    :param path_to_fig_file: path where a figure file is saved
    :type path_to_fig_file: str
    :param dpi: the resolution in dots per inch; if ``None`` (default), use ``rcParams['savefig.dpi']``
    :type dpi: int, None
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param conv_svg_to_emf: whether to convert a .svg file to a .emf file, defaults to ``False``
    :type conv_svg_to_emf: bool
    :param kwargs: [optional] parameters of `matplotlib.pyplot.savefig`_

    .. _`matplotlib.pyplot.savefig`:
        https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.savefig.html
    .. _`Inkscape`: https://inkscape.org

    **Examples**::

        >>> from pyhelpers.store import save_fig
        >>> import matplotlib.pyplot as plt
        >>> from pyhelpers.dir import cd

        >>> x, y = (1, 1), (2, 2)

        >>> plt.figure()
        >>> plt.plot([x[0], y[0]], [x[1], y[1]])
        >>> plt.show()

    The above exmaple is illustrated in :numref:`fig-1`:

    .. figure:: ../_images/fig.*
        :name: fig-1
        :align: center
        :width: 76%

        An example figure created for :py:func:`save_fig()<pyhelpers.store.save_fig>`.

    .. code-block:: python

        >>> img_dir = cd("tests\\images")

        >>> png_file_path = cd(img_dir, "fig.png")
        >>> save_fig(png_file_path, dpi=300, verbose=True)
        Saving "fig.png" to "tests\\images\\" ... Done.

        >>> svg_file_path = cd(img_dir, "fig.svg")
        >>> save_fig(svg_file_path, dpi=300, verbose=True, conv_svg_to_emf=True)
        Saving "fig.svg" to "tests\\images\\" ... Done.
        Saving the .svg file as "tests\\images\\fig.emf" ... Done.
    """

    _get_specific_filepath_info(path_to_fig_file, verbose=verbose, ret_info=False)

    file_ext = pathlib.Path(path_to_fig_file).suffix

    try:
        import matplotlib.pyplot

        matplotlib.pyplot.savefig(path_to_fig_file, dpi=dpi, **kwargs)
        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}.".format(e)) if verbose else ""

    if file_ext == ".svg" and conv_svg_to_emf:
        save_svg_as_emf(path_to_fig_file, path_to_fig_file.replace(file_ext, ".emf"), verbose=verbose)


def save_svg_as_emf(path_to_svg, path_to_emf, verbose=False, inkscape_exe=None, **kwargs):
    """
    Save a `SVG <https://en.wikipedia.org/wiki/Scalable_Vector_Graphics>`_ file (.svg) as
    a `EMF <https://en.wikipedia.org/wiki/Windows_Metafile#EMF>`_ file (.emf).

    :param path_to_svg: path where a .svg file is saved
    :type path_to_svg: str
    :param path_to_emf: path where a .emf file is saved
    :type path_to_emf: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param inkscape_exe: absolute path to 'inkscape.exe', defaults to ``None``
        (on Windows, use the default installation path -
        ``"C:\\Program Files\\Inkscape\\inkscape.exe"``)
    :type inkscape_exe: str or None
    :param kwargs: [optional] parameters of `subprocess.call`_

    .. _`subprocess.call`:
        https://docs.python.org/3/library/subprocess.html#subprocess.call

    **Example**::

        >>> from pyhelpers.store import save_svg_as_emf
        >>> import matplotlib.pyplot as plt
        >>> from pyhelpers.dir import cd

        >>> x, y = (1, 1), (2, 2)

        >>> plt.figure()
        >>> plt.plot([x[0], y[0]], [x[1], y[1]])
        >>> plt.show()

    The above exmaple is illustrated in :numref:`fig-2`:

    .. figure:: ../_images/fig.*
        :name: fig-2
        :align: center
        :width: 76%

        An example figure created for :py:func:`save_svg_as_emf()<pyhelpers.store.save_svg_as_emf>`.

    .. code-block:: python

        >>> img_dir = cd("tests\\images")
        >>> svg_file_path = cd(img_dir, "fig.svg")

        >>> plt.savefig(svg_file_path)

        >>> emf_file_path = cd(img_dir, "fig.emf")

        >>> save_svg_as_emf(svg_file_path, emf_file_path, verbose=True)
        Saving the .svg file as "tests\\images\\fig.emf" ... Done.
    """

    abs_svg_path, abs_emf_path = pathlib.Path(path_to_svg), pathlib.Path(path_to_emf)
    assert abs_svg_path.suffix == ".svg"

    if inkscape_exe is None:
        inkscape_exe = "C:\\Program Files\\Inkscape\\inkscape.exe"

    if os.path.isfile(inkscape_exe):
        if verbose:
            if abs_emf_path.exists():
                print("Updating \"{}\" at \"{}\\\"".format(
                    abs_emf_path.name, os.path.relpath(abs_emf_path.parent)),
                    end=" ... ")
            else:
                print("Saving the .svg file as \"{}\"".format(os.path.relpath(abs_emf_path)),
                      end=" ... ")

        try:
            abs_emf_path.parent.mkdir(exist_ok=True)
            subprocess.call([inkscape_exe, '-z', path_to_svg, '-M', path_to_emf], **kwargs)
            print("Done.") if verbose else ""

        except Exception as e:
            print("Failed. {}".format(e))

    else:
        print("\"Inkscape\" (https://inkscape.org) is required to convert a .svg file to a .emf. file "
              "It is not found on this device.") if verbose else ""


# Web page

def save_web_page_as_pdf(url_to_web_page, path_to_pdf, page_size='A4', zoom=1.0, encoding='UTF-8',
                         verbose=False, wkhtmltopdf_exe=None, **kwargs):
    """
    Save a web page as a `PDF <https://en.wikipedia.org/wiki/PDF>`_ file
    by `wkhtmltopdf <https://wkhtmltopdf.org/>`_.

    :param url_to_web_page: URL of a web page
    :type url_to_web_page: str
    :param path_to_pdf: path where a .pdf is saved
    :type path_to_pdf: str
    :param page_size: page size, defaults to ``'A4'``
    :type page_size: str
    :param zoom: a parameter to zoom in/out, defaults to ``1.0``
    :type zoom: float
    :param encoding: encoding format defaults to ``'UTF-8'``
    :type encoding: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool
    :param wkhtmltopdf_exe: absolute path to 'wkhtmltopdf.exe', defaults to ``None``
        (on Windows, use the default installation path -
        ``"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"``)
    :type wkhtmltopdf_exe: str or None
    :param kwargs: [optional] parameters of `pdfkit.from_url <https://pypi.org/project/pdfkit/>`_

    **Example**::

        >>> from pyhelpers.store import save_web_page_as_pdf
        >>> from pyhelpers.dir import cd

        >>> url_to_a_web_page = 'https://github.com/mikeqfu/pyhelpers'
        >>> path_to_pdf_file = cd("tests\\data", "pyhelpers.pdf")

        >>> save_web_page_as_pdf(url_to_a_web_page, path_to_pdf_file, verbose=True)
        Saving "pyhelpers.pdf" to "tests\\data\\" ...
        Loading pages (1/6)
        Counting pages (2/6)
        Resolving links (4/6)
        Loading headers and footers (5/6)
        Printing pages (6/6)
        Done
    """

    if wkhtmltopdf_exe is None:
        wkhtmltopdf_exe = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

    import pdfkit

    if os.path.isfile(wkhtmltopdf_exe):
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_exe)
    else:
        try:
            config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf.exe")
        except (FileNotFoundError, OSError):
            print("\"wkhtmltopdf\" (https://wkhtmltopdf.org/) is required to run this function. "
                  "It is not found on this device.")
            return None

    try:
        _get_specific_filepath_info(
            path_to_file=path_to_pdf, verbose=verbose, verbose_end=" ... \n", ret_info=False)

        # print("Saving the web page \"{}\" as PDF".format(url_to_web_page)) if verbose else ""
        pdf_options = {'page-size': page_size,
                       # 'margin-top': '0',
                       # 'margin-right': '0',
                       # 'margin-left': '0',
                       # 'margin-bottom': '0',
                       'zoom': str(float(zoom)),
                       'encoding': encoding}

        os.makedirs(os.path.dirname(path_to_pdf), exist_ok=True)

        if os.path.isfile(path_to_pdf):
            os.remove(path_to_pdf)

        status = pdfkit.from_url(
            url_to_web_page, path_to_pdf, configuration=config, options=pdf_options, **kwargs)

        if verbose and not status:
            print("Failed. Check if the URL is available.")

    except Exception as e:
        if verbose:
            print("Failed. {}".format(e), end="")


""" == Load data ============================================================================= """


def load_pickle(path_to_pickle, mode='rb', verbose=False, **kwargs):
    """
    Load data from a `pickle`_ file.

    :param path_to_pickle: path where a pickle file is saved
    :type path_to_pickle: str
    :param mode: mode to `open`_ file, defaults to ``'rb'``
    :type mode: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `pickle.load`_
    :return: data retrieved from the specified path ``path_to_pickle``
    :rtype: any

    .. _`pickle`: https://docs.python.org/3/library/pickle.html
    .. _`open`: https://docs.python.org/3/library/functions.html#open
    .. _`pickle.load`: https://docs.python.org/3/library/pickle.html#pickle.load

    Example::

        >>> from pyhelpers.store import load_pickle
        >>> from pyhelpers.dir import cd

        >>> pickle_path = cd("tests\\data", "dat.pickle")

        >>> pickle_dat = load_pickle(pickle_path, verbose=True)
        Loading "tests\\data\\dat.pickle" ... Done.

        >>> print(pickle_dat)
        1
    """

    if verbose:
        print("Loading \"{}\"".format(os.path.relpath(path_to_pickle)), end=" ... ")

    try:
        pickle_in = open(path_to_pickle, mode=mode)
        pickle_data = pickle.load(pickle_in, **kwargs)
        pickle_in.close()
        print("Done.") if verbose else ""
        return pickle_data

    except Exception as e:
        print("Failed. {}".format(e))


def load_joblib(path_to_joblib, verbose=False, **kwargs):
    """
    Load data from a `joblib`_ file.

    :param path_to_joblib: path where a joblib file is saved
    :type path_to_joblib: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `joblib.load`_
    :return: data retrieved from the specified path ``path_to_joblib``
    :rtype: any

    .. _`joblib`: https://pypi.org/project/joblib/
    .. _`joblib.load`: https://joblib.readthedocs.io/en/latest/generated/joblib.load.html

    Example::

        >>> from pyhelpers.store import load_joblib
        >>> from pyhelpers.dir import cd

        >>> joblib_path = cd("tests\\data", "dat.joblib")

        >>> joblib_dat = load_joblib(joblib_path, verbose=True)
        Loading "tests\\data\\dat.joblib" ... Done.

        >>> joblib_dat
        array([[0.39217296, 0.04115659, 0.92330057, ..., 0.14532720, 0.49324968,
                0.03881915],
               [0.90634699, 0.25862333, 0.26697948, ..., 0.29660476, 0.68259263,
                0.84159475],
               [0.31764887, 0.75153717, 0.24380341, ..., 0.48122767, 0.10094099,
                0.29790084],
               ...,
               [0.52814915, 0.71957599, 0.08243408, ..., 0.87212171, 0.57398544,
                0.97802605],
               [0.48905238, 0.58182107, 0.73918226, ..., 0.16899552, 0.68858890,
                0.56816121],
               [0.14348573, 0.77819159, 0.31177084, ..., 0.85290419, 0.73422955,
                0.63899742]])
    """

    if verbose:
        print("Loading \"{}\"".format(os.path.relpath(path_to_joblib)), end=" ... ")

    try:
        import joblib

        joblib_data = joblib.load(filename=path_to_joblib, **kwargs)
        print("Done.") if verbose else ""

        return joblib_data

    except Exception as e:
        print("Failed. {}".format(e))


def load_multiple_spreadsheets(path_to_spreadsheet, as_dict=True, verbose=False, **kwargs):
    """
    Load multiple sheets of an `Microsoft Excel`_ file.

    :param path_to_spreadsheet: path where a spreadsheet is saved
    :type path_to_spreadsheet: str
    :param as_dict: whether to return the retrieved data as a dictionary type, defaults to ``True``
    :type as_dict: bool
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `pandas.ExcelFile.parse`_
    :return: all worksheet in an Excel workbook from the specified file path ``path_to_spreadsheet``
    :rtype: list or dict

    .. _`Microsoft Excel`: https://en.wikipedia.org/wiki/Microsoft_Excel
    .. _`pandas.ExcelFile.parse`:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelFile.parse.html

    **Examples**::

        >>> from pyhelpers.store import load_multiple_spreadsheets
        >>> from pyhelpers.dir import cd

        >>> dat_dir = cd("tests\\data")
        >>> path_to_xlsx = cd(dat_dir, "dat.xlsx")

        >>> wb_data = load_multiple_spreadsheets(path_to_xlsx, verbose=True, index_col=0)
        Loading "tests\\data\\dat.xlsx" ...
            'TestSheet1'. ... Done.
            'TestSheet2'. ... Done.
            'TestSheet11'. ... Done.
            'TestSheet21'. ... Done.
        >>> list(wb_data.keys())
        ['TestSheet1', 'TestSheet2', 'TestSheet11', 'TestSheet21']

        >>> wb_data = load_multiple_spreadsheets(path_to_xlsx, as_dict=False, index_col=0)
        >>> type(wb_data)
        list
        >>> len(wb_data)
        4
        >>> wb_data[0]
                    Easting  Northing
        London       530034    180381
        Birmingham   406689    286822
        Manchester   383819    398052
        Leeds        582044    152953
    """

    excel_file_reader = pd.ExcelFile(path_to_spreadsheet)

    sheet_names = excel_file_reader.sheet_names
    workbook_dat = []

    if verbose:
        print("Loading \"{}\" ... ".format(os.path.relpath(path_to_spreadsheet)))

    for sheet_name in sheet_names:
        print("\t'{}'.".format(sheet_name), end=" ... ") if verbose else ""

        try:
            sheet_dat = excel_file_reader.parse(sheet_name, **kwargs)
            print("Done.") if verbose else ""

        except Exception as e:
            sheet_dat = None
            print("Failed. {}.".format(e)) if verbose else ""

        workbook_dat.append(sheet_dat)

    excel_file_reader.close()

    if as_dict:
        workbook_data = dict(zip(sheet_names, workbook_dat))
    else:
        workbook_data = workbook_dat

    return workbook_data


def load_json(path_to_json, method=None, verbose=False, **kwargs):
    """
    Load data from a `JSON`_ file.

    :param path_to_json: path where a json file is saved
    :type path_to_json: str
    :param method: an open-source Python package for JSON serialization, options include
        ``None`` (default, for the built-in `json module`_), ``'orjson'`` (for `orjson`_) and
        ``'rapidjson'`` (for `python-rapidjson`_)
    :type method: str or None
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `open`_ (if ``method='orjson'``),
        `rapidjson.load`_ (if ``method='rapidjson'``) or `json.load`_ (if ``method=None``)
    :return: data retrieved from the specified path ``path_to_json``
    :rtype: dict

    .. _`JSON`: https://www.json.org/json-en.html
    .. _`json module`: https://docs.python.org/3/library/json.html
    .. _`orjson`: https://pypi.org/project/orjson/
    .. _`python-rapidjson`: https://pypi.org/project/python-rapidjson
    .. _`open`: https://docs.python.org/3/library/functions.html#open
    .. _`rapidjson.load`: https://docs.python.org/3/library/functions.html#open
    .. _`json.load`: https://docs.python.org/3/library/json.html#json.load

    **Example**::

        >>> from pyhelpers.store import load_json
        >>> from pyhelpers.dir import cd

        >>> json_path = cd("tests\\data", "dat.json")

        >>> json_dat = load_json(json_path, verbose=True)
        Loading "tests\\data\\dat.json" ... Done.

        >>> print(json_dat)
        {'a': 1, 'b': 2, 'c': 3}
    """

    if verbose:
        print("Loading \"{}\"".format(os.path.relpath(path_to_json)), end=" ... ")

    try:
        if method == 'orjson':
            import orjson

            json_in = open(path_to_json, mode='rb', **kwargs)
            json_data = orjson.loads(json_in.read())

        else:
            json_in = open(path_to_json, mode='r')

            if method == 'rapidjson':
                import rapidjson

                json_data = rapidjson.load(json_in, **kwargs)

            else:
                json_data = json.load(json_in, **kwargs)

        json_in.close()

        print("Done.") if verbose else ""

        return json_data

    except Exception as e:
        print("Failed. {}".format(e))


def load_feather(path_to_feather, verbose=False, **kwargs):
    """
    Load data frame from a `Feather`_ file.

    :param path_to_feather: path where a feather file is saved
    :type path_to_feather: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `pandas.read_feather`_

        * columns: (sequence, None) a sequence of column names, if ``None``, all columns
        * use_threads: (bool) whether to parallelize reading using multiple threads, defaults to ``True``

    :return: data retrieved from the specified path ``path_to_feather``
    :rtype: pandas.DataFrame

    .. _`Feather`: https://arrow.apache.org/docs/python/feather.html
    .. _`pandas.read_feather`:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_feather.html

    **Example**::

        >>> from pyhelpers.store import load_feather
        >>> from pyhelpers.dir import cd

        >>> feather_path = cd("tests\\data", "dat.feather")

        >>> feather_dat = load_feather(feather_path, verbose=True)
        Loading "tests\\data\\dat.feather" ... Done.
        >>> feather_dat
           Col1  Col2
        0     1     2
    """

    if verbose:
        print("Loading \"{}\"".format(os.path.relpath(path_to_feather)), end=" ... ")

    try:
        feather_data = pd.read_feather(path_to_feather, **kwargs)
        print("Done.") if verbose else ""
        return feather_data

    except Exception as e:
        print("Failed. {}".format(e))


""" == Uncompress data ======================================================================= """


def unzip(path_to_zip_file, out_dir=None, verbose=False, **kwargs):
    """
    Extract data from a `zipped (compressed)
    <https://support.microsoft.com/en-gb/help/14200/windows-compress-uncompress-zip-files>`_ file.

    :param path_to_zip_file: path where a Zip file is saved
    :type path_to_zip_file: str
    :param out_dir: path to a directory where the extracted data is saved, defaults to ``None``
    :type out_dir: str or None
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param kwargs: [optional] parameters of `zipfile.ZipFile.extractall`_

    .. _`zipfile.ZipFile.extractall`:
        https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.extractall

    **Examples**::

        >>> from pyhelpers.store import unzip
        >>> from pyhelpers.dir import cd, delete_dir

        >>> zip_file_path = cd("tests\\data", "zipped.zip")

        >>> unzip(path_to_zip_file=zip_file_path, verbose=True)
        Extracting "tests\\data\\zipped.zip" to "tests\\data\\zipped\\" ... Done.

        >>> output_dir = cd("tests\\data\\zipped_alt")
        >>> unzip(path_to_zip_file=zip_file_path, out_dir=output_dir, verbose=True)
        Extracting "tests\\data\\zipped.zip" to "tests\\data\\zipped_alt\\" ... Done.

        >>> # Delete the directories "tests\\data\\zipped\\" and "tests\\data\\zipped_alt\\"
        >>> delete_dir(cd("tests\\data\\zipped"), verbose=True)
        The directory "tests\\data\\zipped\\" is not empty.
        Confirmed to delete it? [No]|Yes: yes
        Deleting "tests\\data\\zipped\\" ... Done.
        >>> delete_dir(output_dir, verbose=True)
        The directory "tests\\data\\zipped_alt\\" is not empty.
        Confirmed to delete it
        ? [No]|Yes: yes
        Deleting "tests\\data\\zipped_alt\\" ... Done.
    """

    if out_dir is None:
        out_dir = os.path.splitext(path_to_zip_file)[0]

    if not os.path.exists(out_dir):
        os.makedirs(name=out_dir)

    if verbose:
        rel_path = os.path.relpath(path=path_to_zip_file)
        out_dir_ = os.path.relpath(path=out_dir) + ("\\" if not out_dir.endswith("\\") else "")
        print("Extracting \"{}\" to \"{}\"".format(rel_path, out_dir_), end=" ... ")

    try:
        with zipfile.ZipFile(file=path_to_zip_file) as zf:
            zf.extractall(path=out_dir, **kwargs)
        zf.close()

        print("Done.") if verbose else ""

    except Exception as e:
        print("Failed. {}".format(e))


def seven_zip(path_to_zip_file, out_dir=None, mode='aoa', verbose=False, seven_zip_exe=None,
              **kwargs):
    """
    Use `7-Zip <https://www.7-zip.org/>`_ to extract data from a compressed file.

    :param path_to_zip_file: path where a compressed file is saved
    :type path_to_zip_file: str
    :param out_dir: path to a directory where the extracted data is saved, defaults to ``None``
    :type out_dir: str or None
    :param mode: defaults to ``'aoa'``
    :type mode: str
    :param verbose: whether to print relevant information in console, defaults to ``False``
    :type verbose: bool or int
    :param seven_zip_exe: absolute path to '7z.exe', defaults to ``None``
        (on Windows, the default installation path - ``"C:\\Program Files\\7-Zip\\7z.exe"``)
    :type seven_zip_exe: str or None
    :param kwargs: [optional] parameters of `subprocess.call`_

    .. _`subprocess.call`: https://docs.python.org/3/library/subprocess.html#subprocess.call

    **Examples**::

        >>> from pyhelpers.store import seven_zip
        >>> from pyhelpers.dir import cd, delete_dir

        >>> zip_file_path = cd("tests\\data", "zipped.zip")

        >>> seven_zip(path_to_zip_file=zip_file_path, verbose=True)
        7-Zip 20.00 alpha (x64) : Copyright (c) 1999-2020 Igor Pavlov : 2020-02-06

        Scanning the drive for archives:
        1 file, 158 bytes (1 KiB)

        Extracting archive: \\tests\\data\\zipped.zip
        --
        Path = \\tests\\data\\zipped.zip
        Type = zip
        Physical Size = 158

        Everything is Ok

        Size:       4
        Compressed: 158

        File extracted successfully.

        >>> output_dir = cd("tests\\data\\zipped_alt")
        >>> seven_zip(path_to_zip_file=zip_file_path, out_dir=output_dir, verbose=True)
        7-Zip 20.00 alpha (x64) : Copyright (c) 1999-2020 Igor Pavlov : 2020-02-06

        Scanning the drive for archives:
        1 file, 158 bytes (1 KiB)

        Extracting archive: \\tests\\data\\zipped.zip
        --
        Path = \\tests\\data\\zipped.zip
        Type = zip
        Physical Size = 158

        Everything is Ok

        Size:       4
        Compressed: 158

        File extracted successfully.

        >>> # Extract a .7z file
        >>> zip_file_path = cd("tests\\data", "zipped.7z")
        >>> seven_zip(path_to_zip_file=zip_file_path, out_dir=output_dir, verbose=True)
        7-Zip 20.00 alpha (x64) : Copyright (c) 1999-2020 Igor Pavlov : 2020-02-06

        Scanning the drive for archives:
        1 file, 138 bytes (1 KiB)

        Extracting archive: .\\tests\\data\\zipped.7z
        --
        Path = .\\tests\\data\\zipped.7z
        Type = 7z
        Physical Size = 138
        Headers Size = 130
        Method = LZMA2:12
        Solid = -
        Blocks = 1

        Everything is Ok

        Size:       4

        Compressed: 138

        File extracted successfully.

        >>> # Delete the directories "tests\\data\\zipped\\" and "tests\\data\\zipped_alt\\"
        >>> delete_dir(cd("tests\\data\\zipped"), verbose=True)
        The directory "tests\\data\\zipped\\" is not empty.
        Confirmed to delete it? [No]|Yes: yes
        Deleting "tests\\data\\zipped\\" ... Done.
        >>> delete_dir(output_dir, verbose=True)
        The directory "tests\\data\\zipped_alt\\" is not empty.
        Confirmed to delete it
        ? [No]|Yes: >? yes
        Deleting "tests\\data\\zipped_alt\\" ... Done.
    """

    if seven_zip_exe is None:
        seven_zip_exe = "C:\\Program Files\\7-Zip\\7z.exe"
        if not os.path.isfile(seven_zip_exe):
            seven_zip_exe = "7z.exe"

    if out_dir is None:
        out_dir = os.path.splitext(path_to_zip_file)[0]

    try:
        subprocess.call(
            '"{}" x "{}" -o"{}" -{}'.format(seven_zip_exe, path_to_zip_file, out_dir, mode), **kwargs)
        print("\nFile extracted successfully.")

    except Exception as e:
        print("\nFailed to extract \"{}\". {}.".format(path_to_zip_file, e))
        if verbose:
            print("\"7-Zip\" (https://www.7-zip.org/) is required to run this function. "
                  "It may not be available on this device.")
