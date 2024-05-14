# -*- coding: utf-8 -*-
# @Time    : 2024/05/10 17:01
# @Author  : endearqb

'''
Vn # 缺氧池容积 m3
Q # 生物反应池设计流量 m3/d
Nk # 生物反应池进水总凯氏氮浓度 mg/L
Nte # 生物反应池出水总氮浓度 mg/L
delta_Xv # 排出生物反应池系统的微生物量 kgMLVSS/d
Kde # 反硝化速率 kgN/(kgMLSS·d),20℃时可采用(0.03-0.06)
Kde_T # 温度为T时反硝化速率 kgN/(kgMLSS·d)
Kde_20 # 20℃时反硝化速率 kgN/(kgMLSS·d)
X # 生物反应池内混合液悬浮固体平均浓度 gMLSS/L
T # 设计温度 ℃
Y # 污泥产率系数（kgVSS/kgBOD5），根据试验资料确定，无资料时，可取0.3-0.6
So # 生物反应池进水五日生化需氧量浓度 mg/L
Se # 生物反应池出水五日生化需氧量浓度 mg/L




Vo # 好氧区容积 m3
t # 好氧区设计污泥龄 d
Yt # 污泥总产率系数（kgVSS/kgBOD5），根据试验资料确定，无资料时，有初沉池可取0.3-0.6，无初沉池取0.8-1.2
F # 安全系数，宜为1.5-3.0
miu # 硝化菌比生长速率 d-1 15℃时可取0.47
Na # 生物反应池进水氨氮浓度 mg/L
Kn # 硝化作用中氨氮的半速率常熟 mg/L


Q_Ri # 混合液回流量（硝化液回流）m3/d，混合液回流比Q_Ri/Q不宜大于400%
Nt # 生物反应池进水总氮浓度 mg/L
Nke # 生物反应池出水总凯氏氮浓度 mg/L
Q_R # 污泥回流量m3/d


# 1 缺氧池容积可按下列公式计算

Kde_T = Kde_20 * (1.08 ** (T - 20))
delta_Xv = Y * Q * (So - Se)/1000
Vn = (0.001* Q* (Nk - Nte) -0.12 * delta_Xv)/Kde_T*X 



# 2 好氧区容积按下列公式计算
miu = 0.47 * (Na/(Kn + Na))*math.exp(0.098*(T-15))
t = F / miu
Vo = Q*(So - Se)* t * Yt/(1000*X)

# 3 混合液回流量可按下式计算

Q_Ri= 1000*Vn*Kde*X/(Nt-Nke) - Q_R

'''
import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置全局字体
mpl.rc('font', family='Times New Roman', size=12)  # 可以选择你系统支持的字体

# streamlit run GB500142021AO.py


def AO(Q,Nt,Nte,Kde_20,X ,T,Y,So,Se,F,Na,Kn,Nke,R):
    Kde_T = Kde_20 * (1.08 ** (T - 20))
    delta_Xv = Y * Q * (So - Se)/1000
    Vn = (0.001* Q* (Nt - Nte) -0.12 * delta_Xv)/(Kde_T*X) 
    miu = 0.47 * (Na/(Kn + Na))*math.exp(0.098*(T-15))
    t = F / miu
    Vo = Q*(So - Se)* t * Y/(1000*X)
    Q_Ri_0 = 1000*Vn*Kde_T*X/(Nte-Nke) -Q*R
    Q_Ri= ((Nt-Nte)/(Nte-Nke) - R)*Q
    return (Vn,delta_Xv,Vo,miu,t,Q_Ri_0, Q_Ri)

def show_page1():
    st.title('室外排水设计标准AO计算')
    st.sidebar.header('缺氧池容积计算参数')
    input_labels_1 = [
        'Q 生物反应池设计流量 m3/d',
        'Nt 生物反应池进水总氮浓度 mg/L',
        'Nte 生物反应池出水总氮浓度 mg/L',
        'Kde_20 反硝化速率 kgN/(kgMLSS·d),20℃时可采用(0.03-0.06)',
        'X 生物反应池内混合液悬浮固体平均浓度 gMLSS/L',
        'T 设计温度 ℃',
        'Y 污泥产率系数（kgVSS/kgBOD5）可取0.3-0.6',
        'So 生物反应池进水五日生化需氧量浓度 mg/L',
        'Se 生物反应池出水五日生化需氧量浓度 mg/L'
    ]
    defaults_1 = [10000, 25, 8, 0.04, 1.8, 12, 0.35, 150, 5]
    inputs_1 = []

    for i, (label, default_value) in enumerate(zip(input_labels_1, defaults_1)):
        key = f"input_1_{label.replace(' ', '_')}"
        if 'Kde_20 反硝化速率' in label:
            input_val = st.sidebar.slider(label, 0.030, 0.060, float(default_value), 0.001, key=key)
        elif 'Y 污泥产率系数' in label:
            input_val = st.sidebar.slider(label, 0.3, 0.6, float(default_value), 0.01, key=key)
        elif '设计温度' in label:
            input_val = st.sidebar.slider(label, 12, 35, int(default_value), 1, key=key)
        elif 'X 生物反应池内混合液悬浮固体平均浓度' in label:
            input_val = st.sidebar.slider(label, 1.0, 5.0, float(default_value), 0.1, key=key)
        else:
            input_val = st.sidebar.text_input(label, str(default_value), key=key)
        inputs_1.append(input_val)

    st.sidebar.header('好氧池容积计算参数')
    input_labels_2 = [ 'F 硝化安全系数，宜为1.5-3.0', 'Na 生物反应池进水氨氮浓度 mg/L', 'Kn 硝化作用中氨氮的半速率常数 mg/L']
    defaults_2 = [3, 25, 1]
    inputs_2 = []

    for i, (label, default_value) in enumerate(zip(input_labels_2, defaults_2)):
        key = f"input_2_{label.replace(' ', '_')}"
        if '硝化安全系数' in label:
            input_val2 = st.sidebar.slider(label, 1.5, 3.0, float(default_value), 0.1, key=key)
        elif '硝化作用中氨氮的半速率常数' in label:
            input_val2 = st.sidebar.slider(label, 0.5, 3.0, float(default_value), 0.1, key=key)
        else:
            input_val2 = st.sidebar.text_input(label, str(default_value), key=key)
        inputs_2.append(input_val2)
    st.sidebar.header ('混合液回流量计算参数')
    input_labels_3 = [ 'Nke 生物反应池出水总凯氏氮浓度 mg/L', 'R 污泥回流比']
    # 为每个输入框添加默认值
    defaults_3 = [2, 0.8]
    # inputs_3 = [st.sidebar.text_input(label, default_value, key=f"input_{i+len(defaults_1)+len(defaults_2)}") for i, (label, default_value) in enumerate(zip(input_labels_3, defaults_3))]

    inputs_3 = []

    for i, (label, default_value) in enumerate(zip(input_labels_3, defaults_3)):
        key = f"input_3_{label.replace(' ', '_')}"
        if '污泥回流比' in label:
            input_val3 = st.sidebar.slider(label, 0.5, 1.2, float(default_value), 0.1, key=key)
        else:
            input_val3 = st.sidebar.text_input(label, str(default_value), key=key)
        inputs_3.append(input_val3)
    # 计算按钮
    if st.button('计算'):
        try:
            inputs_1 = [float(val) for val in inputs_1]
            inputs_2 = [float(val) for val in inputs_2]
            inputs_3 = [float(val) for val in inputs_3]
            result = AO(*inputs_1, *inputs_2, *inputs_3)

            output_str = "### 缺氧池容积计算计算\n\n"      
            output_str += f"缺氧池容积: {result[0]:.2f} m3 \n\n"
            output_str += f"排出生物反应池系统的微生物量 : {result[1]:.2f} kgMLVSS/d \n\n"
            output_str += "### 好氧池容积计算计算\n\n" 
            output_str += f"好氧池容积 : {result[2]:.2f} m3 \n\n"
            output_str += f"好氧池设计温度与氨氮浓度下比增长速率 : {result[3]:.2f} d-1 \n\n"
            output_str += f"好氧池设计泥龄 : {result[4]:.2f} d \n\n"
            output_str += "### 混合液回流量计算\n\n" 
            output_str += f"混合液/硝化液回流量 : {result[5]:.2f} m3/d \n\n"
            output_str += f"混合液/硝化液回流量(改) : {result[6]:.2f} m3/d \n\n"
            st.markdown(f" \n{output_str}\n ")
        
            st.markdown('**缺氧区体积、硝化液回流比与反硝化速率kde之间的关系图**')
            # Define kde20 range
            kde20_values = np.linspace(0.03, 0.06, 100)  # SRT from 0.1 to 20, 400 points
            Vn = np.zeros(len(kde20_values))
            QR = np.zeros(len(kde20_values))
            for i in range(len(kde20_values)):
                inputs_11 = inputs_1
                inputs_11[3] = kde20_values[i]
                Vn[i] = AO(*inputs_11, *inputs_2, *inputs_3)[0]
                QR[i] = AO(*inputs_11, *inputs_2, *inputs_3)[5]

            # Calculate fx1min

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # Plot orange curve on primary y-axis
            ax1.plot(kde20_values, Vn, color='orange', label='$Vn$ vs $K_{de(20)}$')
            ax1.set_xlabel('$K_{de(20)}$')
            ax1.set_ylabel('$Vn$')
            ax1.tick_params('y')

            ax2 = ax1.twinx()  

            # Plot red curve on secondary y-axis
            ax2.plot(kde20_values, QR, color='red', label='$Q_{Ri}$ vs $K_{de(20)}$')  
            ax2.set_ylabel('$Q_{Ri}$')
            ax2.tick_params('y')

            # Add title and grid
            ax1.set_title('Relationship between $K_{de(20)}$, $Vn$ and $Q_{Ri}$')
            ax1.grid(True, linestyle='--')

            # Add legends
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
            # Display the plot in Streamlit
            st.pyplot(fig)

            st.markdown('**缺氧区体积、硝化液回流比与污泥产率系数Y之间的关系图**')
            # Define kde20 range
            Y_values = np.linspace(0.3, 0.6, 100)  # SRT from 0.1 to 20, 400 points
            Vn1 = np.zeros(len(Y_values))
            QR1 = np.zeros(len(Y_values))
            for i in range(len(Y_values)):
                inputs_12 = inputs_1
                inputs_12[6] = Y_values[i]
                Vn1[i] = AO(*inputs_12, *inputs_2, *inputs_3)[0]
                QR1[i] = AO(*inputs_12, *inputs_2, *inputs_3)[5]

            # Calculate fx1min

            fig_1, ax_1 = plt.subplots(figsize=(10, 6))

            # Plot orange curve on primary y-axis
            ax_1.plot(Y_values, Vn1, color='orange', label='$Vn$ vs Y_values')
            ax_1.set_xlabel('Y_values')
            ax_1.set_ylabel('$Vn$')
            ax_1.tick_params('y')

            ax_12 = ax_1.twinx()  

            # Plot red curve on secondary y-axis
            ax_12.plot(Y_values, QR1, color='red', linestyle='--', label='$Q_{Ri}$ vs Y_values')  
            ax_12.set_ylabel('$Q_{Ri}$')
            ax_12.tick_params('y')

            # Add title and grid
            ax_1.set_title('Relationship between Y_values, $Vn$ and $Q_{Ri}$')
            ax_1.grid(True, linestyle='--')

            # Add legends
            lines_1, labels_1 = ax_1.get_legend_handles_labels()
            lines_2, labels_2 = ax_12.get_legend_handles_labels()
            ax_1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
            # Display the plot in Streamlit
            st.pyplot(fig_1)

        except ValueError:
            st.error('请输入正确的数值')
    st.markdown("""
                     
### 缺氧/好氧容积按下列公式计算
**缺氧区公式**
       
                
$$V_n = \\frac{0.001 Q (N_{t} - N_{te}) -0.12 \\Delta X_v}{K_{de(T)} X}$$
<br>
<br>$$K_{de(T)} = K_{de20}1.08^{T-20}$$
<br>
<br>$$\\Delta X_v = Y \\frac{Q (So - Se)}{1000}$$
<br>
                
**好氧区公式**
           

$$V_o = \\frac{Q(S_o-S_e)\\theta_{co}Y}{1000X}$$
<br>
<br>$$\\theta_{co} = F\\frac{1}{\\mu}$$
<br>
<br>$$\\mu = 0.47\\frac{N_{a}} {K_{n}+N_{a}} \\mathbf{e}^{0.098(T-15)}$$
<br>
                
**混合液回流量**

$$Q_{Ri} = (\\frac{N_t-N_{te}}{N_{te}-N_{ke}} - R)*Q$$
                
- $V_n$ 缺氧池容积 (m3)
- $Q$ 生物反应器设计流量 (m3/d)
- $N_{t}$ 生物反应池进水总凯氏氮浓度 (mg/L)
- $N_{te}$ 生物反应池出水总氮浓度 (mg/L)
- $K_{de(T)}$ 反硝化速率 (kgN/(kgMLSS·d))
- $X$ 生物反应池内混合液悬浮固体平均浓度 (gMLSS/L)
- $0.12\\Delta X_v$ 排出生物反应池系统的微生物量中的含氮量(kgN/d),0.12是微生物含氮比例，$\\Delta X_v$是排出生物反应池系统的微生物量 (kgMLVSS/d)
- $T$ 设计温度 (℃)
- $Y$ 污泥产率系数 (kgVSS/kgBOD5)
- $So$ 生物反应池进水五日生化需氧量浓度 (mg/L)
- $Se$ 生物反应池出水五日生化需氧量浓度 (mg/L)
- $K_{de(20)}$ 反硝化速率 (kgN/(kgMLSS·d))
- $N_{ke}$ 生物反应池进水总氮浓度 (mg/L)

**说明**
1. 缺氧区和好氧区容积计算时的污泥产率系数统一为Y，原标准中分为产率系数和总产率系数，有不同的取值范围，这里统一为初沉后的取值Y=0.3-0.6(kgVSS/kgBOD5)，一般市政废水中Y的值可取0.67(kgCOD/kgBOD5)，乙酸、乙醇、甲醇在0.4-0.45(kgCOD/kgBOD5)，单位转化为VSS需要/(0.92*1.42)，0.92是因为我们使用马弗炉测VSS时会残留微生物含有的8%左右的无机盐，1.42可以看作kgVSSS/kgCOD的转化系数，实际取值时可参考计算；
   <br>
2. 反硝化速率Kde(T)的计算按MLSS计不够严谨，因为MLSS中的VSS部分中的**活性微生物部分**才会产生反硝化，作为动力学参数这个值使用MLSS计算时活性微生物所占比例的影响非常大，MLSS中非VSS的比例主要和进水无机颗粒浓度与污水的硬度和碱度有关，VSS中活性微生物的比例主要和进水BOD5浓度、惰性VSS颗粒浓度以及泥龄有关，这两个比例不同地区不同污水的差别较大，影响因素太多，因此这里使用反硝化速率的取值Kde(T) = 0.03-0.06需要参考区域经验；
   <br>                
3. 对于标准中描述污泥浓度出现的MLSS、VSS、MLVSS，我的建议是在使用化学计量学计算的时候统一使用MLVSS，这样就不用在计算好氧区体积时还要增加一个包括进水中未沉淀有机无机污泥的总产率系数，以及MLVSS/MLSS在一定范围内取值，在二沉池设计时使用MLSS，根据二沉池的负荷选择合适的MLSS。
   <br>                
4. 在该计算规则下，缺氧区以反硝化负荷计算，好氧区使用BOD负荷计算，因此，缺氧区的体积会比较容易超过好氧区，甚至超过DWA德国手册中限制的 缺氧区/(缺氧区+好氧区)<0.6 的要求，在面对实际情况设计时可考虑适当延长好氧区停留时间，特别是在冬季存在硝化困难的地区；
   <br>                
5. 混合液回流量计算时修改了公式，原公式是根据计算缺氧区体积的公式变形而来，是用系统设计能处理硝态氮的浓度/出水硝态氮浓度后减去污泥回流，因为在系统设计是减去了排出生物反应池系统的微生物量中的含氮量，这个值的影响因素和我在第2点里讨论过的问题一致，存在较大的不确定性，实际计算中污泥产率系数Y的取值对该项的影响较大，因此在这里的计算中忽略了排泥排出的微生物中的含氮量，如需计算可参考DWA德国手册或书籍污水生物处理；
   <br>                
6. 标准内缺氧区和好氧区容积计算存在较多需要经验取值的部分，同时在公式和参数描述上缺乏一致性，心疼几秒新手工艺设计工程师，这个标准就不是让新手能设计好的标准；
   <br>                
7. 再次建议深入学习DWA-A-131德国手册与书籍《污水生物处理：原理、设计与模拟》第四、五章内容。
                
"""
    , unsafe_allow_html=True)
def main():
    show_page1()

if __name__ == '__main__':
    main()



