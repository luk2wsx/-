import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

st.title("📈 員工學習效率分析 Dashboard")

# 📁 檔案上傳功能
uploaded_file = st.file_uploader(
    "📁 請上傳您的 Excel 檔案",
    type=['xlsx', 'xls'],
    help="支援 .xlsx 和 .xls 格式的 Excel 檔案"
)

if uploaded_file is not None:
    try:
        # 讀取上傳的檔案
        df = pd.read_excel(uploaded_file)
        df['歸屬日期'] = pd.to_datetime(df['歸屬日期'])
        
        st.success(f"✅ 檔案上傳成功！共讀取到 {len(df)} 筆資料")
        
        # 顯示資料預覽
        with st.expander("📊 資料預覽"):
            st.dataframe(df.head())
            st.write(f"**資料欄位：** {list(df.columns)}")
        
        # 👤 選擇員工(可複選)
        workers = st.multiselect(
            "👤 選擇員工(可複選)",
            options=df['姓名'].unique(),
            default=[df['姓名'].unique()[0]]
        )

        # 🏭 選擇工站
        station = st.selectbox(
            "🏭 選擇工站",
            options=df['工站'].unique(),
            index=0
        )

        # 🗓️ 分析日期區間
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "開始日期",
                value=df['歸屬日期'].min().date(),
                min_value=df['歸屬日期'].min().date(),
                max_value=df['歸屬日期'].max().date()
            )
        with col2:
            end_date = st.date_input(
                "結束日期",
                value=df['歸屬日期'].max().date(),
                min_value=df['歸屬日期'].min().date(),
                max_value=df['歸屬日期'].max().date()
            )

        # 🔎 資料篩選
        if not workers:
            st.warning("⚠️ 請至少選擇一位員工")
        else:
            df_filtered = df[
                (df['姓名'].isin(workers)) &
                (df['工站'] == station) &
                (df['歸屬日期'] >= pd.to_datetime(start_date)) &
                (df['歸屬日期'] <= pd.to_datetime(end_date))
            ].sort_values('歸屬日期')

            # 📊 統計
            if df_filtered.empty:
                st.warning("⚠️ 無符合條件的資料")
            else:
                avg_eff = round(df_filtered['分數'].mean(), 2)
                avg_time = round(df_filtered['人員作業時間'].mean(), 2)
                st.markdown(f"📌 **平均效率：{avg_eff}%｜平均每日作業時間：{avg_time} 小時**")

                # 📈 學習曲線圖
                fig_curve = go.Figure()
                for emp in workers:
                    emp_data = df_filtered[df_filtered['姓名'] == emp]
                    if emp_data.empty:
                        continue
                    emp_data = emp_data.copy()
                    emp_data['作業次數'] = range(1, len(emp_data)+1)
                    X = emp_data['作業次數'].values.reshape(-1, 1)
                    y = emp_data['分數'].values
                    model = LinearRegression().fit(X, y)
                    y_pred = model.predict(X)
                    fig_curve.add_trace(go.Scatter(x=X.flatten(), y=y, mode='lines+markers', name=f'{emp} 效率'))
                    fig_curve.add_trace(go.Scatter(x=X.flatten(), y=y_pred, mode='lines', name=f'{emp} 趨勢線', line=dict(dash='dash')))
                fig_curve.update_layout(title='👥 員工學習效率曲線', xaxis_title='作業次數', yaxis_title='效率(%)')
                st.plotly_chart(fig_curve, use_container_width=True)
                
                                 # 📋 詳細資料表格
                 with st.expander("📋 詳細資料"):
                     st.dataframe(df_filtered)
                     
     except Exception as e:
         st.error(f"❌ 檔案讀取錯誤：{str(e)}")
         st.info("💡 請確認您的 Excel 檔案包含以下必要欄位：姓名、工站、歸屬日期、分數、人員作業時間")
 else:
     st.info("📁 請上傳您的 Excel 檔案開始分析")
     
     # 顯示範例資料格式
     with st.expander("📋 資料格式說明"):
         st.markdown("""
         **您的 Excel 檔案應包含以下欄位：**
         - **姓名**：員工姓名
         - **工站**：工作站名稱
         - **歸屬日期**：日期格式 (YYYY-MM-DD)
         - **分數**：效率分數 (數值)
         - **人員作業時間**：作業時間 (數值)
         
         **範例資料格式：**
         | 姓名 | 工站 | 歸屬日期 | 分數 | 人員作業時間 |
         |------|------|----------|------|--------------|
         | 張三 | A站 | 2024-01-01 | 85 | 8.5 |
         | 李四 | B站 | 2024-01-01 | 92 | 7.8 |
         """)

# 🖥️ 本地執行設定（僅用於本地測試）
if __name__ == '__main__':
    # 本地執行時可以加入額外設定
    pass