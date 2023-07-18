import pandas as pd
import tabula
import streamlit as st

def extract_table_from_pdf(file):
    tables = tabula.read_pdf(file, lattice=True, pages='all')
    return pd.concat(tables)

def extract_inventory_from_excel(file):
    return pd.read_excel(file, sheet_name=None)

def main():
    st.title('PDFとExcelからのデータ抽出')

    uploaded_pdfs = [st.file_uploader(f"PDFファイル{i+1}をアップロードしてください", type="pdf") for i in range(3)]
    uploaded_excel = st.file_uploader("Excelファイルをアップロードしてください", type="xlsx")

    if uploaded_excel and any(uploaded_pdfs):
        dfs = [extract_table_from_pdf(pdf) for pdf in uploaded_pdfs if pdf is not None]
        df = pd.concat(dfs)

        inventory_sheets = extract_inventory_from_excel(uploaded_excel)

        df_sum = df[['Unnamed: 1', 'Unnamed: 2']].groupby('Unnamed: 1', as_index=False).sum()

        d = {}
        dd = {}
        for i in range(len(df_sum)):
            d[df_sum['Unnamed: 1'].iloc[i]] = df_sum['Unnamed: 2'].iloc[i]
            dd[df_sum['Unnamed: 1'].iloc[i]] = False

        for sheet_name, inventory in inventory_sheets.items():
            result_rows = []
            for i in range(len(inventory)):
                key = inventory.iloc[i,2]
                value = ""
                if key in d and key != "nan":
                    value = d[key]
                    dd[key] = True
                result_rows.append([key, value])
            st.subheader(sheet_name)
            st.write(pd.DataFrame(result_rows, columns=['商品コード', '数量']))

        st.subheader("在庫表になかった商品コードと合計数量")
        missing_items = [[k, d[k]] for k, v in dd.items() if not v]
        st.write(pd.DataFrame(missing_items, columns=['商品コード', '数量']))

if __name__ == "__main__":
    main()
