import os
import numpy as np
import yaml
import shutil
from datetime import datetime
import time
from life_game_convolution import LifeGameConvolution
from life_game_analyzer import LifegameAnalyzer

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def run_convolution_simulation(size, max_t, probabilities, from_showing_graph):
    """ライフゲーム（畳み込み演算による高速化）"""
    game = LifeGameConvolution(size, probabilities)
    start_time = time.time()
    is_frozen, t, all_states = game.run(max_t, from_showing_graph)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return is_frozen, t, elapsed_time, all_states

def set_probabilities(alive_p):
    """発生確率を生成"""
    alive_p = round(float(alive_p), 2)
    dead_p = 1.0 - alive_p
    probabilities = [dead_p, alive_p]
    return probabilities

def run_and_save_all():

    # 設定ファイルを読み込む
    config = load_config()
    
    # 日付付きフォルダの作成
    current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"{config['save_path']}_{current_date}"
    os.makedirs(output_dir, exist_ok=True)

    # 設定ファイルのコピー
    shutil.copy('config.yaml', os.path.join(output_dir, 'config.yaml'))

    size = config['size']
    max_t = config['max_t']
    from_showing_graph = config['from_showing_graph']

    # 発生確率をコントロール(0.1~0.5に0.05刻み)
    start = 0.1
    end = 0.5
    step = 0.05
    for alive_p in np.arange(start, end + step, step):
        # 発生確率を生成
        probabilities = set_probabilities(alive_p)
        print(f"probabilities(Dead/Alive): {probabilities}") 

        # 畳み込みを使用したライフゲームのシミュレーション
        is_frozen_conv, t_conv, elapsed_time_conv, all_states = run_convolution_simulation(size, max_t, probabilities, from_showing_graph)
        print(f"Convolution Simulation[{size}x{size}] ended at step {t_conv} with frozen state: {is_frozen_conv} in {elapsed_time_conv:.4f} seconds")
        
        # 全ての状態を保存
        output_dir_with_alive_p = os.path.join(output_dir,str(round(float(alive_p),2)))
        os.makedirs(output_dir_with_alive_p, exist_ok=True)
        analyzer = LifegameAnalyzer(output_dir_with_alive_p)
        analyzer.save_all_states(all_states)
    return output_dir

def save_all_densities(output_dir):
     # 発生確率をコントロール(0.1~0.5に0.05刻み)
    start = 0.1
    end = 0.5
    step = 0.05
    analyzer = LifegameAnalyzer(output_dir)
    for alive_p in np.arange(start, end + step, step):
        analyzer.save_density_graph(alive_p)

def analyze_density(output_dir=None):
    if output_dir == None:
        output_dir = run_and_save_all()

    # 密度グラフを保存する
    save_all_densities(output_dir)

def main():

    # シミュレーションのみ実行する場合
    run_and_save_all()

    # 任意の結果フォルダを指定して実行する場合
    output_dir = "simulation_results_20240725_130331"
    analyze_density(output_dir) 

    # シミュレーションの実行と密度計算を行う場合
    analyze_density() 

if __name__ == "__main__":
    main()
