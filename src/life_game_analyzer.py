import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class LifegameAnalyzer():
    def __init__(self,output_dir) -> None:
        self.save_dir = output_dir

    def save_all_states(self, all_states):
        """全ての状態を保存する"""
        for t, state in enumerate(all_states):
            file_path = os.path.join(self.save_dir, f"state_{t}.npy")
            np.save(file_path, state)

    def load_all_states(self,output_dir):
        if os.path.exists(output_dir) == False:
            print("No save_dir available.")
            return

        """指定したフォルダから全ての状態を読み込む"""
        files = sorted(
            [f for f in os.listdir(output_dir) if f.startswith("state_") and f.endswith('.npy')],
            key=lambda x: int(x.split('_')[1].split('.')[0])
        )
        all_states = [np.load(os.path.join(output_dir, file)) for file in files]
        return all_states

    def animate_life_game(self, all_states, interval=200):
        if all_states == None or len(all_states) <= 0:
            print("No states available for animation.")
            return
        
        """ライフゲームをアニメーションで表示する"""
        fig, ax = plt.subplots()
        ims = []
        for state in all_states:
            im = ax.imshow(state, animated=True, cmap='binary')
            ims.append([im])
        
        # 再生
        ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True, repeat=False)
        plt.show()

    def replay(self,alive_p):
        """フォルダを指定してライフゲームの状態を再生する"""
        output_dir_with_alive_p = os.path.join(self.save_dir,str(round(float(alive_p),2)))
        all_states = self.load_all_states(output_dir_with_alive_p)
        self.animate_life_game(all_states)

def main():
    # 再生
    alive_p = 0.1 # from 0.1 to 0.5 by 0.05
    output_dir = 'simulation_results_20240724_225144'
    analyzer = LifegameAnalyzer(output_dir)
    # analyzer.replay(alive_p)
    analyzer.replay(0.5)


if __name__ == "__main__":
    main()
