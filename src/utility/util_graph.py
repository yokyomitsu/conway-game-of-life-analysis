import os
import matplotlib.pyplot as plt

def plot_graph_2D(x_values, y_values, title: str = 'Example Plot', xlabel: str = 'X Axis Label', ylabel: str = 'Y Axis Label', filename=None):
    """任意の2つのリストを受け取り、グラフにプロットする"""
    if len(x_values) != len(y_values):
        print(f"[Notice] x_len and y_len doesn't match length! , x_values_len: {len(x_values)}, y_values_len: {len(y_values)}")
        return None
    
    # グラフを作成
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_values, y_values, marker='o', linestyle='-', color='b')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)

    if fig and filename:
        # フォルダが存在しない場合は作成
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # グラフを保存
        fig.savefig(filename)
        print(f"Plot saved to {filename}")
        plt.close(fig)
    else:
        print("Failed to create plot.")

def main():
    # 例として使用するデータ
    x_values = list(range(1, 11)) 
    y_values = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 
    plot_graph_2D(x_values,y_values)
    
    save_path = 'test/plot.png'
    plot_graph_2D(x_values,y_values,filename=save_path)

if __name__ == "__main__":
    main()