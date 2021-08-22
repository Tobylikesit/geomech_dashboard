
import streamlit as st
import pandas as pd
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import numpy as np
import time
from math import ceil

st.set_page_config(
     page_title="Geomechanics Dashboard",
     page_icon="🟢",
     layout="wide",
     initial_sidebar_state="expanded",
 )


def load_data():
    file = st.sidebar.file_uploader("Upload your file",type=["xls","xlsx","xlsm","xlsb","odf","ods","odt"])
    # if file!=None:st.balloons()
    return file



@st.cache(suppress_st_warning=True)
def get_data(xl, dir_col):
    my_prog = st.progress(0)
    # Sample Shales data:
    # xl = None
    xl = pd.ExcelFile(xl)
    sheets = list(xl.sheet_names)
    shale = xl.parse(sheets[0],na_values=0).dropna(axis=1,how="all",inplace=False).dropna(axis=0,how="all",inplace=False)
    shale[shale.depth == '*if Per A, maybe 10 m shallower'] = np.nan

    shale.depth = shale.depth.astype(float) #//1
    for n,i in enumerate(sheets[1:]):
        d = xl.parse(i,na_values=0).dropna(axis=1,how="all",inplace=False).dropna(axis=0,how="all",inplace=False)
        d = d.astype({"depth":float})
        # d[d.depth == '*if Per A, maybe 10 m shallower'] = np.nan
        # d.depth = d.depth.astype(float) #//1
        # d.set_index(["well","depth"], inplace = True) #,"form","facies",pd.Index(range(len(d))), verify_integrity = True
        # print(i,":\n",d.head(5))
        # if i=="Tensile":
        #     for j in shale.dir.unique():
        #         dc = d.copy()
        #         dc["dir"] = j
        #         shale = shale.merge(dc, on=list(shale.columns[shale.columns.isin(dc.columns)]), how="outer", )
        #         dc = None
        print(i)
        my_prog.progress(ceil(100/len(sheets)*(n+2)))
        shale = shale.merge(d, on=list(shale.columns[shale.columns.isin(d.columns)]), how="outer", )
    col_bys = ['depth','well']
    if dir_col:
        col_bys.append('dir')

    grsh = shale.groupby(by=col_bys, dropna=False, as_index=False).mean()
    grdepthsh = grsh.copy()
    grdepthsh.depth = 0.5*(np.array(grdepthsh.depth-grdepthsh.depth//1)>=0.5)+grdepthsh.depth//1

    grdepthsh = grdepthsh.groupby(by=col_bys, dropna=False, as_index=False).mean()
    filename = F"output_shales {time.strftime('%d.%m.%Y %H.%M.%S')}.xlsx"
    with pd.ExcelWriter(filename) as writer:  
        shale.to_excel(writer, sheet_name='SH')
        grsh.to_excel(writer, sheet_name='GR_SH')
        grdepthsh.to_excel(writer, sheet_name='GR_SH_DEPTH')
        my_prog = None
    return pd.DataFrame(grdepthsh)
    # Sample data for sands:
    
    
def poly_reg(x, y, order = 2, Plot = True):
    # Deleting null values
    cond = x.isnull() | y.isnull()
    x,y = np.array(x[~cond]), np.array(y[~cond])
    # find coeffs:
    coeffs = np.polyfit(x, y, order)
    # predict data:
    p = np.poly1d(coeffs)
    # plot if needed:
    if Plot:
        t = np.linspace(x.min(), x.max(), 100)
        plt.scatter(x, y, label = 'orig')
        # print(p(t))
        plt.plot(t, p(t), ':', c = 'r' , label = 'reg')
        plt.legend()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(plt.show())
    return(coeffs)


# Main:

try:
    with st.echo(code_location='below'):
        # Data Reading
        file = load_data()
        
        
        if file == None:
            # ds = st.sidebar.radio(
            # "Or choose dataset:",
            # ('None','Shales.xlsx','Sands.xlsx'),)
            
            # if ds == 'None':
            st.info('No data was chosen, app is terminated...')
            st.stop()
            # df = get_data(ds)
        else:
            # xl = pd.ExcelFile(file)
            # all_sheets = xl.sheet_names
            # sheet = st.sidebar.selectbox(
            # 'Sheet:',
            # all_sheets,index=0)
            # cols = st.sidebar.slider('Columns:', 0, 25, 14)
            dir_col = st.checkbox("Consider direction", True)
            
            df = get_data(file, dir_col)
            # df = pd.read_excel(file, usecols=range(cols))
            
        # Columns
        if 'depth' not in df.columns:
            # st.stop()
            depth_col_name = st.selectbox(
            'Choose column with depth names:',
            list(df.columns),index=0)
            df.rename(columns = {depth_col_name: 'depth'}, inplace = True)
        if 'well' not in df.columns:
            well_col_name = st.selectbox(
            'Choose column with well names:',
            list(df.columns),)
            df.rename(columns = {well_col_name: 'well'}, inplace = True)
        
        # Well selector
        
        wellnonan = [x for x in np.array(df.well.unique()) if x is not np.nan]
        wells = st.multiselect("Choose wells", wellnonan, wellnonan)
        if not wells:
            st.error("Please select at least one well.")
            st.stop()
        else:
            data = df[df.well.isin(wells)]
            # AXES
            
            xaxvalues = [x for x in np.array(df.columns.unique()) if x not in ['well','depth']]
            
            X_AXIS = st.sidebar.selectbox(
            'X-axis column:',
            xaxvalues,index=9%len(xaxvalues))
            
            yaxvalues = [x for x in np.array(df.columns.unique()) if x not in ['well','depth',X_AXIS]]
            
            Y_AXIS = st.sidebar.selectbox(
            'Y-axis column:',
            yaxvalues,index=12%len(yaxvalues))
            st.write("#",X_AXIS,'vs',Y_AXIS)
            
                
            if X_AXIS in ['depth','well',Y_AXIS] or Y_AXIS in ['depth','well']:
                st.sidebar.warning("Dublicate column found, please change axes. \
                        (If you have well or depth selected as one of the\
                         axes please change it to data column with integers or floats.)")
            # Visualisation
            if st.checkbox("Show all columns"):
                st.write(data)
            else:
                if X_AXIS in ['depth','well',Y_AXIS] or Y_AXIS in ['depth','well']:
                    st.warning("Dublicate column found, please change axes. \
                        (If you have well or depth selected as one of the axes please change it to data column with integers or floats.)")
                    st.stop()
                else:
                    st.write(data[['depth','well',X_AXIS,Y_AXIS]])

            # data = data.T.reset_index()
            # data = pd.melt(data, id_vars=["index"]).rename(
            #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            # )
            chart = (
                alt.Chart(data)
                .mark_circle(size=60)
                .encode(
                    x=X_AXIS,
                    y=Y_AXIS,
                    color="well",
                    tooltip=[i for i in data.columns]
                ).interactive()
            )
            st.altair_chart(chart, use_container_width=True)
            
            
            # Regression
            try:
                with st.spinner('Please wait...'):
                    time.sleep(2)
                order = st.slider('Regression order:', 0, 3, 1)
                st.write('Regression coeffs:',poly_reg(data[X_AXIS],data[Y_AXIS],order=order))
                st.write('\n')
            except:
                st.warning("Please try using numerical data for regression!")
except Exception as e:
    print(e)
finally:
    file.close()
    st.stop()
