import math

def calculate_pi_data():
    # 使用PPT中给出的n值列表
    n_values = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    
    # 准备存储计算结果的列表
    pi_n_direct = [] # 直接多边形逼近值
    pi_n_wynn = []   # 外推逼近值
    
    # 1. 计算直接逼近值
    for n in n_values:
        if n == 1:
            pi_n_direct.append(0.0)
        else:
            pi_n_direct.append(n * math.sin(math.pi / n))
            
    # 2. 计算外推逼近值 (Wynn-Epsilon)
    # 这里手动填入PPT表格中的外推值，未给出的用 None 或 '-' 占位
    pi_n_wynn = [None, None, 3.414213562373096, None, 3.141418327933211, 
                 None, 3.141592658918053, None, 3.141592653589786]
    
    return n_values, pi_n_direct, pi_n_wynn

def write_tecplot_file(filename, n_values, pi_n_direct, pi_n_wynn):
    # 计算步长 h 和误差
    h_values = [1.0 / n for n in n_values] # 步长
    # 误差 = | π近似值 - π真实值 |，这里使用PPT中16位的精确π值
    exact_pi = 3.141592653589793
    error_direct = [abs(pi_approx - exact_pi) for pi_approx in pi_n_direct]
    
    # 打开文件并写入Tecplot格式数据
    with open(filename, 'w') as f:
        # 写入文件头
        f.write('TITLE = "Convergence of Pi Approximation"\n')
        f.write('VARIABLES = "h", "n", "Pi_Approximation", "Error", "Pi_Approximation_Wynn"\n')
        
        # 写入数据区域开始行和格式
        # I=9 表示有9个数据点，F=POINT 表示逐点格式
        f.write('ZONE T="Pi Data", I=9, F=POINT\n')
        
        # 写入每个数据点
        for i in range(len(n_values)):
            # 对Wynn值进行处理，如果为None则写入0占位
            wynn_val = pi_n_wynn[i] if pi_n_wynn[i] is not None else 0.0
            f.write(f"{h_values[i]:.10f} {n_values[i]:4d} {pi_n_direct[i]:.16f} {error_direct[i]:.16e} {wynn_val:.16f}\n")
    
    print(f"数据文件 '{filename}' 已生成，包含 {len(n_values)} 个数据点。")

# 主执行部分
if __name__ == "__main__":
    n_vals, pi_direct, pi_wynn = calculate_pi_data()
    write_tecplot_file("pi_convergence.dat", n_vals, pi_direct, pi_wynn)
