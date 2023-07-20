import pandas as pd
import camelot  # tabulaの代わりにcamelotをインポートします
import streamlit as st
import base64

def extract_table_from_pdf(file):
    tables = camelot.read_pdf(file, stream=True, pages='all')  # read_pdfの呼び出しをcamelotのものに書き換えます
    return pd.concat([table.df for table in tables])

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
            result_df = pd.DataFrame(result_rows, columns=['商品コード', '数量'])
            st.write(result_df)

            # ダウンロードボタンを追加
            csv = result_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="result.csv">Download csv file</a>', unsafe_allow_html=True)

        st.subheader("在庫表になかった商品コードと合計数量")
        missing_items = [[k, d[k]] for k, v in dd.items() if not v]
        missing_items_df = pd.DataFrame(missing_items, columns=['商品コード', '数量'])
        st.write(missing_items_df)

        # ダウンロードボタンを追加
        csv = missing_items_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="missing_items.csv">Download csv file</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
