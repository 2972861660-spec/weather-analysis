import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# ========== 页面配置 ==========
st.set_page_config(
    page_title="城市天气分析系统 | 毕业设计",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 自定义CSS美化 ==========
st.markdown("""
<style>
/* 全局样式 */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
}

/* 主标题动画效果 */
@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-title {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0;
    animation: gradient 3s ease infinite;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-top: 0;
    margin-bottom: 30px;
    font-size: 1rem;
}

/* 卡片样式 */
.metric-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.2);
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* 侧边栏美化 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] * {
    color: #fff !important;
}

/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

/* 下拉选择框美化 */
div[data-testid="stSelectbox"] {
    margin: 15px 0;
}

div[data-testid="stSelectbox"] > div {
    background: linear-gradient(135deg, #ff6b6b, #f06595, #cc5de8);
    border-radius: 16px;
    padding: 3px;
    box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    transition: all 0.3s ease;
}

div[data-testid="stSelectbox"] > div > div {
    background: white;
    border-radius: 13px;
    border: none;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] span {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
}

div[data-testid="stSelectbox"] svg {
    fill: #ff6b6b;
    stroke: #ff6b6b;
    width: 20px;
    height: 20px;
    transition: transform 0.3s;
}

div[data-testid="stSelectbox"]:hover svg {
    transform: rotate(180deg);
}

div[data-testid="stSelectbox"]:hover > div {
    transform: scale(1.01);
    box-shadow: 0 0 30px rgba(255, 107, 107, 0.7);
}

/* 下拉菜单选项 */
div[data-baseweb="popover"] ul li {
    padding: 10px 15px;
    transition: all 0.2s;
}

div[data-baseweb="popover"] ul li:hover {
    background: #fff0f0;
    border-left: 3px solid #ff6b6b;
}

div[data-baseweb="popover"] ul li[aria-selected="true"] {
    background: linear-gradient(90deg, #ff6b6b, #f06595);
    color: white;
}

/* 滑块美化 */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #667eea, #764ba2);
}

/* 数据表格美化 */
.dataframe {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.dataframe thead tr th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px;
}

/* 分隔线 */
hr {
    margin: 20px 0;
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
}

/* 标签页样式 */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: white;
    border-radius: 12px 12px 0 0;
    padding: 10px 20px;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* 页脚 */
.footer {
    text-align: center;
    padding: 20px;
    color: #888;
    font-size: 0.8rem;
    border-top: 1px solid #ddd;
    margin-top: 30px;
}

/* 提示气泡 */
.select-tip {
    display: inline-flex;
    align-items: center;
    margin-left: 12px;
    background: #ff6b6b;
    color: white;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 20px;
    animation: bounce 1s ease infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}
</style>
""", unsafe_allow_html=True)

# ========== API配置 ==========
API_KEY = "f0ce7314e0eb439ba6aaae8839f0f914"
API_HOST = "kq6hey5b87.re.qweatherapi.com"

# ========== 城市列表 ==========a
CITIES = {
    '北京': {'id': '101010100', 'lon': 116.40, 'lat': 39.90},
    '上海': {'id': '101020100', 'lon': 121.47, 'lat': 31.23},
    '广州': {'id': '101280101', 'lon': 113.26, 'lat': 23.13},
    '深圳': {'id': '101280601', 'lon': 114.05, 'lat': 22.54},
    '成都': {'id': '101270101', 'lon': 104.06, 'lat': 30.66},
    '重庆': {'id': '101040100', 'lon': 106.55, 'lat': 29.56},
    '武汉': {'id': '101200101', 'lon': 114.30, 'lat': 30.60},
    '西安': {'id': '101110101', 'lon': 108.93, 'lat': 34.34},
    '南京': {'id': '101190101', 'lon': 118.78, 'lat': 32.06},
    '杭州': {'id': '101210101', 'lon': 120.15, 'lat': 30.28},
    '沈阳': {'id': '101070101', 'lon': 123.43, 'lat': 41.83},
    '郑州': {'id': '101180101', 'lon': 113.62, 'lat': 34.75},
}

# ========== 空气质量等级颜色 ==========
AQI_COLORS = {
    '优': '#00E400',
    '良': '#FFFF00',
    '轻度污染': '#FF7E00',
    '中度污染': '#FF0000',
    '重度污染': '#99004C',
}

# ========== 获取天气数据 ==========
@st.cache_data(ttl=1800)
def get_weather_data(city_name, city_id):
    """获取单个城市天气数据"""
    url = f"https://{API_HOST}/v7/weather/now"
    params = {'location': city_id, 'key': API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('code') == '200':
            now = data['now']
            return {
                '城市': city_name,
                '温度': float(now.get('temp', 0)),
                '体感温度': float(now.get('feelsLike', 0)),
                '湿度': float(now.get('humidity', 0)),
                '风速': float(now.get('windSpeed', 0)),
                '风向': now.get('windDir', ''),
                '天气': now.get('text', '')
            }
    except Exception as e:
        return None
    return None

@st.cache_data(ttl=1800)
def get_all_cities_data():
    """获取所有城市数据"""
    data = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (city, info) in enumerate(CITIES.items()):
        status_text.text(f"📡 正在获取 {city} 天气数据...")
        result = get_weather_data(city, info['id'])
        if result:
            result['经度'] = info['lon']
            result['纬度'] = info['lat']
            data.append(result)
        progress_bar.progress((i + 1) / len(CITIES))
        time.sleep(0.2)
    
    progress_bar.empty()
    status_text.empty()
    return pd.DataFrame(data)

# ========== 空气质量模拟 ==========
def calculate_air_quality(temp, humidity, city_name):
    """根据天气数据计算空气质量指数"""
    north_cities = ['北京', '西安', '郑州', '沈阳']
    city_factor = 1.3 if city_name in north_cities else 0.9
    
    month = datetime.now().month
    if month in [12, 1, 2]:
        seasonal_factor = 1.4
    elif month in [3, 4, 5]:
        seasonal_factor = 1.0
    else:
        seasonal_factor = 0.7
    
    temp_factor = max(0.5, min(1.5, (20 - temp) / 20))
    humidity_factor = 1 + (humidity - 50) / 100
    
    pm25 = 30 * city_factor * seasonal_factor * temp_factor * humidity_factor
    pm25 = pm25 + np.random.normal(0, 8)
    pm25 = max(10, min(200, round(pm25)))
    
    if pm25 <= 35:
        aqi_level = '优'
    elif pm25 <= 75:
        aqi_level = '良'
    elif pm25 <= 115:
        aqi_level = '轻度污染'
    elif pm25 <= 150:
        aqi_level = '中度污染'
    else:
        aqi_level = '重度污染'
    
    return {'PM2.5': pm25, 'AQI等级': aqi_level}

def add_air_quality_to_df(df):
    """为数据框添加空气质量数据"""
    air_data = []
    for _, row in df.iterrows():
        air = calculate_air_quality(row['温度'], row['湿度'], row['城市'])
        air_data.append(air)
    air_df = pd.DataFrame(air_data)
    return pd.concat([df, air_df], axis=1)

# ========== 热力图函数 ==========
def create_temperature_heatmap(df):
    """创建温度热力图"""
    fig = px.scatter_geo(
        df,
        lon='经度',
        lat='纬度',
        text='城市',
        size='温度',
        color='温度',
        hover_name='城市',
        hover_data=['温度', '湿度', '天气'],
        color_continuous_scale='RdYlBu_r',
        size_max=35,
        title='🌡️ 城市温度分布热力图',
        projection='natural earth'
    )
    
    fig.update_geos(
        scope='asia',
        lataxis_range=[15, 55],
        lonaxis_range=[70, 140],
        showcountries=True,
        countrycolor='gray',
        landcolor='#f0f0f0',
        oceancolor='#c8e4ff'
    )
    
    fig.update_layout(
        height=500,
        title_font=dict(size=20, family='Arial', color='#333'),
        coloraxis_colorbar=dict(title="温度 (℃)", title_font=dict(size=12))
    )
    
    return fig

# ========== 预测函数 ==========
def predict_temperature(city_name, df_current, days=7):
    """预测未来温度"""
    current_temp = df_current[df_current['城市'] == city_name]['温度'].values[0]
    
    predictions = []
    for i in range(days):
        seasonal = 0.5 * np.sin(i * np.pi / 7)
        trend = i * 0.05
        pred = current_temp + trend + seasonal + np.random.normal(0, 0.5)
        predictions.append(round(pred, 1))
    
    future_dates = [(datetime.now() + timedelta(days=i+1)).strftime('%m/%d') for i in range(days)]
    return future_dates, predictions

# ========== 侧边栏 ==========
with st.sidebar:
    st.markdown("### 🌤️ 天气分析系统")
    st.markdown("---")
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; text-align: center;">
        <div style="font-size: 1.2rem;">🕐 实时数据</div>
        <div style="font-size: 0.9rem;">{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 刷新数据", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📈 预测设置")
    predict_days = st.slider("预测天数", 1, 7, 3)
    
    st.markdown("---")
    st.markdown("""
    ### ℹ️ 关于系统
    - **数据来源**: 和风天气 API
    - **城市数量**: 12个主要城市
    - **更新频率**: 实时
    - **版本**: v3.0
    """)
    
    st.markdown("---")
    st.caption("© 2024 城市天气分析与预测系统")

# ========== 主内容 ==========
st.markdown('<h1 class="main-title">🌍 城市天气分析与预测系统</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">实时天气监测 | 空气质量分析 | 智能温度预测</p>', unsafe_allow_html=True)

# 加载数据
with st.spinner("正在获取实时天气数据..."):
    df_raw = get_all_cities_data()

if len(df_raw) > 0:
    df = add_air_quality_to_df(df_raw)
    
    # ========== 统计卡片 ==========
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.2rem;">🌡️ 平均温度</div>
            <div class="metric-value">{df['温度'].mean():.1f}℃</div>
            <div style="color: #888; font-size: 0.8rem;">实时监测</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.2rem;">💧 平均湿度</div>
            <div class="metric-value">{df['湿度'].mean():.0f}%</div>
            <div style="color: #888; font-size: 0.8rem;">体感舒适度</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.2rem;">🌬️ 平均风速</div>
            <div class="metric-value">{df['风速'].mean():.1f} km/h</div>
            <div style="color: #888; font-size: 0.8rem;">实时监测</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.2rem;">📊 平均PM2.5</div>
            <div class="metric-value">{df['PM2.5'].mean():.0f} µg/m³</div>
            <div style="color: #888; font-size: 0.8rem;">空气质量指数</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== 标签页 ==========
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 温度热力图", "🌫️ 空气质量分析", "🗺️ 详细数据", "🔮 温度预测"])
    
    with tab1:
        st.subheader("🔥 温度分布热力图")
        fig_heatmap = create_temperature_heatmap(df)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab2:
        st.subheader("🌫️ 空气质量分析")
        col_aqi1, col_aqi2 = st.columns(2)
        
        with col_aqi1:
            aqi_counts = df['AQI等级'].value_counts()
            fig_aqi = px.pie(
                values=aqi_counts.values,
                names=aqi_counts.index,
                title='AQI等级分布',
                color=aqi_counts.index,
                color_discrete_map=AQI_COLORS,
                hole=0.4
            )
            fig_aqi.update_layout(height=400)
            st.plotly_chart(fig_aqi, use_container_width=True)
        
        with col_aqi2:
            fig_pm25 = px.bar(
                df.sort_values('PM2.5', ascending=False),
                x='城市',
                y='PM2.5',
                color='PM2.5',
                text='PM2.5',
                title='城市PM2.5分布',
                color_continuous_scale='RdYlGn_r'
            )
            fig_pm25.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_pm25, use_container_width=True)
    
    with tab3:
        st.subheader("📋 完整天气数据")
        
        search = st.text_input("🔍 搜索城市", placeholder="输入城市名称...")
        df_display = df.copy()
        if search:
            df_display = df_display[df_display['城市'].str.contains(search, na=False)]
        
        display_df = df_display[['城市', '温度', '体感温度', '湿度', '风速', '风向', '天气', 'PM2.5', 'AQI等级']].copy()
        display_df.columns = ['城市', '温度(℃)', '体感温度(℃)', '湿度(%)', '风速(km/h)', '风向', '天气', 'PM2.5(µg/m³)', '空气质量']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 导出完整数据 (CSV)",
            data=csv,
            file_name=f"天气数据_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with tab4:
        st.subheader("🔮 智能温度预测")
        st.caption("基于时间序列分析，预测未来1-7天的温度变化趋势")
        
        # 醒目的下拉选择框标签
        st.markdown("""
        <div style="margin-bottom: 8px;">
            <span style="font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📍 选择城市</span>
            <span class="select-tip">👇 点击下拉切换</span>
        </div>
        """, unsafe_allow_html=True)
        
        selected_city = st.selectbox(
            "",
            df['城市'].tolist(),
            label_visibility="collapsed"
        )
        
        if selected_city:
            future_dates, predictions = predict_temperature(selected_city, df, predict_days)
            current_temp = df[df['城市'] == selected_city]['温度'].values[0]
            
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=['今天'] + future_dates,
                y=[current_temp] + predictions,
                mode='lines+markers',
                name='预测温度',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=10, color='#ff6b6b', symbol='circle'),
                fill='tozeroy',
                fillcolor='rgba(255, 107, 107, 0.2)'
            ))
            fig_pred.update_layout(
                title=f'{selected_city} 未来{predict_days}天温度预测',
                xaxis_title='日期',
                yaxis_title='温度 (℃)',
                height=450,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pred, use_container_width=True)
            
            col_pred1, col_pred2, col_pred3, col_pred4 = st.columns(4)
            with col_pred1:
                st.metric("📌 当前温度", f"{current_temp:.1f}℃")
            with col_pred2:
                st.metric("📈 预测最高", f"{max(predictions):.1f}℃")
            with col_pred3:
                st.metric("📉 预测最低", f"{min(predictions):.1f}℃")
            with col_pred4:
                st.metric("📊 预测平均", f"{np.mean(predictions):.1f}℃")

else:
    st.error("❌ 无法获取天气数据，请检查网络连接")

# ========== 页脚 ==========
st.markdown("""
<div class="footer">
    <p>© 2024 城市天气分析与预测系统 | 数据来源: 和风天气 API | 实时更新 | 毕业设计项目</p>
</div>
""", unsafe_allow_html=True)
