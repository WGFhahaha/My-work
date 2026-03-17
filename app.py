import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# 0. 页面全局配置
st.set_page_config(
    page_title="大湾区 vs 山东 区域科创数据对比",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 1. 内嵌脱敏/汇总数据
# 1.1 宏观投入产出数据
df_macro = pd.DataFrame({
    "指标": ["R&D经费支出(亿元)", "当年发明专利申请量(万件)", "当年发明专利授权量(万件)", "GDP(万亿元)"],
    "粤港澳大湾区": [4912.9, 38.0, 16.4, 14.8],
    "山东省": [2386.0, 14.8, 6.4, 9.86]
})

# 1.2 战新产业专利分布数据 (雷达图数据)
df_industry = pd.DataFrame({
    "产业赛道": ["半导体", "通信", "人工智能", "新材料", "高端装备", "新能源"],
    "大湾区申请量(万件)": [2.8, 2.7, 4.0, 2.6, 2.7, 2.3],
    "山东申请量(万件)": [0.31, 0.27, 1.13, 1.67, 1.59, 0.91]
})

# 1.3 科创企业梯队数据
df_enterprise = pd.DataFrame({
    "企业梯队": ["中国科创领袖(家)", "国家级制造业单项冠军(家)", "专精特新'小巨人'(家)"],
    "粤港澳大湾区": [22, 186, 1922],
    "山东省": [5, 237, 1163]
})

# 1.4 城市分布集中度 (气泡图数据)
df_city = pd.DataFrame({
    "城市": ["深圳", "广州", "东莞", "青岛", "济南", "烟台", "潍坊"],
    "区域": ["大湾区", "大湾区", "大湾区", "山东", "山东", "山东", "山东"],
    "小巨人数量(家)": [1029, 336, 150, 194, 163, 130, 108],  # 东莞数据为估算演示
    "单项冠军数量(家)": [95, 31, 15, 39, 23, 24, 27]
})


# 2. 侧边栏设计 (导航与个人信息)

col_img1, col_img2, col_img3 = st.sidebar.columns([1, 1.5, 1])
with col_img2:

    st.image("avatar.jpg", use_container_width=True)

st.sidebar.markdown("<h3 style='text-align: center;'>王高飞</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: gray;'>金融学硕士 | 24岁 </p>", unsafe_allow_html=True)
st.sidebar.markdown("📧 1260093494@qq.com")
st.sidebar.markdown("📞 15655482536")

st.sidebar.divider()

# 页面导航
page = st.sidebar.radio(
    "📂 个人作品集导航",
    ["📊 科创调研报告", "📝 核心项目经历"]
)

st.sidebar.divider()
st.sidebar.caption("")


# 3. 页面一：交互式数据看板 (Dashboard)

if page == "📊 科创调研报告":
    st.title("📊 大湾区 vs 山东 区域科创数据对比")
    st.markdown("基于专利与科创公开数据，客观呈现粤港澳大湾区与山东省在科技创新、产业分布及企业梯队上的特征与差异。")

    # --- 核心指标区 (KPI) ---
    st.subheader("一、 宏观研发对比 (2024年数据)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="大湾区 R&D经费", value="4912 亿元", delta="占全国14.7%")
    with col2:
        st.metric(label="山东省 R&D经费", value="2386 亿元", delta="全国第五", delta_color="off")
    with col3:
        st.metric(label="大湾区 发明专利申请", value="38.0 万件", delta="+13.2% 同比")
    with col4:
        st.metric(label="山东省 发明专利申请", value="14.8 万件", delta="+19.2% 同比 (高增长)")

    st.divider()

    # --- 交互图表区 ---

    st.subheader("二、 优势产业偏好")
    st.markdown("大湾区聚焦半导体与通信，山东则在新材料与高端装备领域领先。")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=df_industry["大湾区申请量(万件)"],
        theta=df_industry["产业赛道"],
        fill='toself',
        name='粤港澳大湾区',
        line_color='#FF773C'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=df_industry["山东申请量(万件)"],
        theta=df_industry["产业赛道"],
        fill='toself',
        name='山东省',
        line_color='#10C378'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True,
                            margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_radar, use_container_width=True)


    st.subheader("三、 科创企业梯队")


    df_melt = df_enterprise.melt(id_vars="企业梯队", var_name="区域", value_name="企业数量")
    # 为了展示效果，使用对数坐标轴，因为小巨人数量(1000+)和科创领袖(5)差距太大
    fig_bar = px.bar(df_melt, x="企业梯队", y="企业数量", color="区域",
                     barmode="group", text="企业数量", log_y=True,
                     color_discrete_map={"粤港澳大湾区": '#FF773C', "山东省": '#10C378'})
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(yaxis_title="企业数量 (对数轴)", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)



    st.subheader("四、 科创资源聚集度")
    st.markdown("大湾区科创资源极度向深圳集中，而山东则在青岛、济南、烟台、潍坊形成多点分散的矩阵。")
    fig_bubble = px.scatter(df_city, x="单项冠军数量(家)", y="小巨人数量(家)",
                            size="小巨人数量(家)", color="区域", text="城市",
                            size_max=50, color_discrete_map={"大湾区": '#FF773C', "山东": '#10C378'})
    fig_bubble.update_traces(textposition='top center')
    st.plotly_chart(fig_bubble, use_container_width=True)


   # 3. 底部直接放 PDF 下载链接区
    st.subheader("📎 获取完整版调研报告")
    st.caption("以下报告为本人在实习期间，独立进行底稿数据处理并撰写的区域科创分析报告。")

    col_pdf1, col_pdf2, col_empty = st.columns([1, 1, 1.5])
    with col_pdf1:
        try:
            with open("大湾区篇.pdf", "rb") as pdf_file1:
                st.download_button(label="📥 下载《大湾区篇》完整PDF", data=pdf_file1,
                                   file_name="粤港澳大湾区科创全景解析.pdf", mime="application/pdf", type="primary")
        except FileNotFoundError:
            st.button("📥 下载《大湾区篇》(请将 大湾区篇.pdf 放入同目录以激活)", disabled=True)

    with col_pdf2:
        try:
            with open("山东篇.pdf", "rb") as pdf_file2:
                st.download_button(label="📥 下载《山东篇》完整PDF", data=pdf_file2, file_name="山东省科创全景解析.pdf",
                                   mime="application/pdf", type="primary")
        except FileNotFoundError:
            st.button("📥 下载《山东篇》(请将 山东篇.pdf 放入同目录以激活)", disabled=True)



    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("以下报告为本人在实习期间，全程参与底稿数据处理并撰写部分内容的知识产权调研报告。")

    col_pdf3, col_empty2 = st.columns([1.5, 2.5])
    with col_pdf3:
        try:
            with open("2025年426知识产权调研报告.pdf", "rb") as pdf_file3:
                st.download_button(label="📥 下载《2025年426知识产权调研报告》", data=pdf_file3,
                                   file_name="2025年426知识产权调研报告.pdf", mime="application/pdf", type="primary")
        except FileNotFoundError:
            st.button("📥 下载《426知识产权报告》(请将PDF文件放入同目录激活)", disabled=True)






elif page == "📝 核心项目经历":
    st.title("📑 实证研究项目")

    # 论文基本信息卡片
    st.info("""
    **论文发表**：《国家生态文明试验区政策对省域能源安全的影响及空间溢出效应研究》  
    **发表平台**：《西安石油大学学报（社会科学版）》 | 作者：李善燊，**王高飞（第二作者）**，王君萍  
    """)

    st.markdown("""
    **💡 研究摘要**：基于 2012-2022 年中国 30 个省份的面板数据，构建多维省域能源安全指数。实证发现试验区政策显著提升了本地能源安全水平。
    """)
    st.divider()


    # 图表一：指标构建过程 (Treemap)

    st.subheader("一、 能源安全多维评价指标体系 (熵值法)")
    st.markdown("摒弃单一指标，从**供应韧性、市场结构、环境约束**三个维度选取18个二级指标，通过算法客观赋权构建综合指数。")

    df_indicators = pd.DataFrame({
        "一级指标": ["供应韧性"] * 6 + ["市场结构"] * 6 + ["环境约束"] * 6,
        "二级指标": ["能源自给率", "能源进口依赖度", "人均能源生产量", "新能源装机容量", "新能源发电量", "新能源占比",
                     "能源消费强度", "新能源强度", "能源工业投资强度", "能源行业投资强度", "经济结构多样性", "人均GDP",
                     "人均二氧化碳排放量", "碳排放强度", "人均二氧化硫排放量", "二氧化硫排放强度", "环境污染物利用率",
                     "森林覆盖率"],
        "权重": [0.026, 0.004, 0.080, 0.101, 0.121, 0.099,
                 0.012, 0.144, 0.078, 0.089, 0.028, 0.044,
                 0.006, 0.008, 0.002, 0.002, 0.112, 0.042]
    })

    fig_tree = px.treemap(df_indicators, path=['一级指标', '二级指标'], values='权重',
                          color='一级指标',
                          color_discrete_sequence=['#FF773C', '#10C378','#4757E8'])
    fig_tree.update_traces(textinfo="label+value")
    fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), height=350)
    st.plotly_chart(fig_tree, use_container_width=True)

    st.divider()

    # 提取底层面板数据 (各省11年数据)

    data_matrix = {
        "安徽": [0.160, 0.163, 0.166, 0.176, 0.187, 0.213, 0.184, 0.171, 0.164, 0.185, 0.206],
        "北京": [0.102, 0.110, 0.114, 0.114, 0.115, 0.127, 0.131, 0.137, 0.134, 0.137, 0.142],
        "福建": [0.176, 0.198, 0.212, 0.242, 0.271, 0.301, 0.322, 0.315, 0.288, 0.315, 0.342],
        "甘肃": [0.239, 0.247, 0.248, 0.266, 0.239, 0.248, 0.310, 0.274, 0.263, 0.289, 0.328],
        "广东": [0.264, 0.277, 0.298, 0.310, 0.284, 0.276, 0.327, 0.374, 0.300, 0.325, 0.346],
        "广西": [0.159, 0.167, 0.168, 0.172, 0.205, 0.214, 0.229, 0.234, 0.200, 0.212, 0.233],
        "贵州": [0.133, 0.139, 0.143, 0.152, 0.161, 0.151, 0.161, 0.186, 0.196, 0.209, 0.216],
        "海南": [0.138, 0.139, 0.143, 0.138, 0.196, 0.200, 0.207, 0.234, 0.219, 0.220, 0.234],
        "河北": [0.129, 0.160, 0.169, 0.181, 0.198, 0.215, 0.248, 0.236, 0.255, 0.295, 0.347],
        "河南": [0.150, 0.155, 0.157, 0.166, 0.176, 0.188, 0.212, 0.189, 0.169, 0.212, 0.250],
        "黑龙江": [0.187, 0.191, 0.192, 0.185, 0.172, 0.176, 0.176, 0.199, 0.183, 0.196, 0.217],
        "湖北": [0.139, 0.143, 0.148, 0.144, 0.156, 0.171, 0.164, 0.191, 0.155, 0.177, 0.196],
        "湖南": [0.147, 0.152, 0.159, 0.161, 0.163, 0.176, 0.180, 0.196, 0.145, 0.155, 0.172],
        "吉林": [0.151, 0.157, 0.161, 0.166, 0.179, 0.172, 0.186, 0.200, 0.179, 0.191, 0.223],
        "江苏": [0.177, 0.190, 0.199, 0.210, 0.214, 0.224, 0.272, 0.267, 0.243, 0.293, 0.328],
        "江西": [0.138, 0.144, 0.146, 0.153, 0.158, 0.167, 0.189, 0.207, 0.159, 0.173, 0.191],
        "辽宁": [0.152, 0.179, 0.190, 0.198, 0.246, 0.280, 0.249, 0.268, 0.231, 0.251, 0.269],
        "内蒙古": [0.271, 0.298, 0.323, 0.331, 0.319, 0.355, 0.396, 0.409, 0.453, 0.509, 0.576],
        "宁夏": [0.246, 0.243, 0.271, 0.321, 0.322, 0.329, 0.378, 0.375, 0.412, 0.468, 0.492],
        "青海": [0.135, 0.156, 0.158, 0.228, 0.231, 0.241, 0.303, 0.378, 0.414, 0.458, 0.510],
        "山东": [0.172, 0.189, 0.206, 0.204, 0.209, 0.210, 0.234, 0.277, 0.239, 0.289, 0.328],
        "山西": [0.198, 0.196, 0.209, 0.223, 0.213, 0.214, 0.203, 0.215, 0.242, 0.280, 0.291],
        "陕西": [0.157, 0.173, 0.175, 0.175, 0.189, 0.187, 0.197, 0.223, 0.200, 0.228, 0.243],
        "上海": [0.083, 0.087, 0.089, 0.092, 0.106, 0.111, 0.109, 0.116, 0.113, 0.123, 0.126],
        "四川": [0.190, 0.187, 0.195, 0.205, 0.166, 0.169, 0.207, 0.213, 0.140, 0.151, 0.156],
        "天津": [0.088, 0.095, 0.096, 0.097, 0.097, 0.105, 0.117, 0.120, 0.134, 0.145, 0.161],
        "新疆": [0.179, 0.220, 0.256, 0.308, 0.267, 0.276, 0.302, 0.325, 0.332, 0.357, 0.386],
        "云南": [0.173, 0.186, 0.189, 0.210, 0.233, 0.236, 0.236, 0.255, 0.226, 0.222, 0.233],
        "浙江": [0.230, 0.235, 0.241, 0.267, 0.280, 0.292, 0.308, 0.325, 0.278, 0.295, 0.322],
        "重庆": [0.085, 0.094, 0.099, 0.099, 0.116, 0.116, 0.101, 0.107, 0.106, 0.111, 0.118]
    }

    # 地图匹配全称映射
    prov_name_mapping = {
        "安徽": "安徽省", "北京": "北京市", "福建": "福建省", "甘肃": "甘肃省",
        "广东": "广东省", "广西": "广西壮族自治区", "贵州": "贵州省", "海南": "海南省",
        "河北": "河北省", "河南": "河南省", "黑龙江": "黑龙江省", "湖北": "湖北省",
        "湖南": "湖南省", "吉林": "吉林省", "江苏": "江苏省", "江西": "江西省",
        "辽宁": "辽宁省", "内蒙古": "内蒙古自治区", "宁夏": "宁夏回族自治区",
        "青海": "青海省", "山东": "山东省", "山西": "山西省", "陕西": "陕西省",
        "上海": "上海市", "四川": "四川省", "天津": "天津市", "新疆": "新疆维吾尔自治区",
        "云南": "云南省", "浙江": "浙江省", "重庆": "重庆市"
    }

    records = []
    # 填入已有数据的省份
    for prov, values in data_matrix.items():
        full_name = prov_name_mapping.get(prov, prov)
        for i, year in enumerate(range(2012, 2023)):
            records.append({"省份": prov, "全称": full_name, "年份": year, "能源安全指数": values[i]})


    missing_regions = [
        ("西藏", "西藏自治区"),
        ("台湾", "台湾省"),
        ("香港", "香港特别行政区"),
        ("澳门", "澳门特别行政区")
    ]
    for short_name, full_name in missing_regions:
        for year in range(2012, 2023):
            records.append({"省份": short_name, "全称": full_name, "年份": year, "能源安全指数": 0.0})

    df_all_map = pd.DataFrame(records)


    @st.cache_data
    def load_china_geojson():
        import urllib.request
        import json
        url = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"
        try:
            req = urllib.request.urlopen(url, timeout=5)
            return json.loads(req.read())
        except:
            return None



    # 图表二：省域热力地图

    st.subheader("二、 各省能源安全水平时空演变热力图")

    selected_year = st.slider("🕰️ 拖动时间轴，动态查看 2012-2022 年各省能源安全水平变化：", 2012, 2022, 2022)
    df_year = df_all_map[df_all_map["年份"] == selected_year]

    china_geojson = load_china_geojson()
    if china_geojson:

        fig_map = px.choropleth_mapbox(
            df_year,
            geojson=china_geojson,
            locations="全称",
            featureidkey="properties.name",
            color="能源安全指数",
            hover_name="省份",
            color_continuous_scale="YlOrRd",
            range_color=[0, 0.45],
            mapbox_style="carto-positron",
            zoom=3,
            center={"lat": 35.8617, "lon": 104.1954},
            opacity=0.85
        )
        fig_map.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=500)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("⚠️ 地图底层文件加载超时，已为您自动切换为该年份的柱状图。")
        fig_bar = px.bar(df_year.sort_values("能源安全指数", ascending=False),
                         x="省份", y="能源安全指数", color="能源安全指数", color_continuous_scale="YlOrRd")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()


    # 图表三：全国均值趋势 (高级平滑数据点折线图)

    st.subheader("三、 全国平均能源安全指数宏观演变趋势")
    st.markdown("10年间，全国能源安全指数稳步攀升，揭示了我国能源供应多样化和新能源转型的显著成效。")

    df_trend = pd.DataFrame({
        "年份": [str(y) for y in range(2012, 2023)],
        "全国均值": [0.165, 0.176, 0.184, 0.196, 0.202, 0.211, 0.228, 0.241, 0.226, 0.249, 0.273]
    })


    main_color = "#FF773C"
    fill_color = "rgba(255, 119, 60, 0.1)"

    fig_trend = go.Figure()


    fig_trend.add_trace(go.Scatter(
        x=df_trend["年份"],
        y=df_trend["全国均值"],
        mode='lines+markers',
        name="能源安全指数",
        line=dict(color=main_color, width=4, shape="spline"),
        marker=dict(size=10, color="white", line=dict(width=3, color=main_color)),
        fill='tozeroy',
        fillcolor=fill_color,
        hovertemplate="<b>%{x}年</b><br>指数: %{y:.3f}<extra></extra>"
    ))


    max_val = df_trend["全国均值"].max()
    max_year = df_trend.loc[df_trend["全国均值"].idxmax(), "年份"]

    fig_trend.add_annotation(
        x=max_year, y=max_val,
        text=f"🚀 2022 历史峰值: {max_val:.3f}",
        showarrow=True,
        arrowhead=0, arrowcolor=main_color,
        ax=0, ay=-35,
        font=dict(size=12, color="white"),
        bgcolor=main_color,
        borderpad=6,
        opacity=0.95
    )


    fig_trend.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        yaxis=dict(
            range=[0.14, 0.30],
            title="全国平均能源安全指数",
            showgrid=True,
            gridcolor="rgba(200, 200, 200, 0.3)",
            griddash="dash",
            zeroline=False,
            tickfont=dict(color="gray")
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor="rgba(200, 200, 200, 0.5)",
            tickfont=dict(color="gray")
        ),
        margin=dict(t=50, b=20, l=10, r=10),
        height=380
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 论文下载按钮
    st.markdown("#### 📎 获取完整版学术论文")
    col_dl, col_blank = st.columns([1, 2])
    with col_dl:
        try:
            with open("国家生态文明试验区政策对省域能源安全的影响及空间溢出效应研究.pdf", "rb") as pdf_paper:
                st.download_button(
                    label="📥 下载论文全文 PDF",
                    data=pdf_paper,
                    file_name="王高飞-国家生态文明试验区政策对省域能源安全的影响及空间溢出效应研究.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
        except FileNotFoundError:
            st.button("📥 下载论文全文 PDF", disabled=True, use_container_width=True)