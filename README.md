# geomech_dashboard
Built with streamlit and pandas for my bp internship project analysis.

Excel file requirements
1. Excel should contain multiple datasheets.
2. Each sheet should contain 'depth' and 'well' columns.
3. Order of sheets merging with complete file is the same as sheets order in original excel file.
4. Since join and merge methods are used related columns in different sheets should have the same name.
5. Avoid having extra data(/charts) below or in the side of your table in excel file.
6. Load_data method uses data window resampling with 1 unit scale (1234.5,1234.9 are combined into one 1234.0)

