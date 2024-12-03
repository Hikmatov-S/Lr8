import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PolygonClipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Clipper")

        self.create_widgets()
    
    def create_widgets(self):
        poly_frame = tk.Frame(self.root)
        poly_frame.pack(pady=5)
        
        self.poly_label = tk.Label(poly_frame, text="Координаты вершин многоугольника:")
        self.poly_label.pack(side=tk.LEFT, padx=5)
        
        self.poly_entry = tk.Entry(poly_frame, width=50)
        self.poly_entry.pack(side=tk.LEFT, padx=5)
        self.poly_entry.insert(0, "500,200, 581,387, 775,387, 619,500, 700,687, 500,575, 300,687, 381,500, 225,387, 419,387")

        clip_frame = tk.Frame(self.root)
        clip_frame.pack(pady=5)
        
        self.clip_label = tk.Label(clip_frame, text="Координаты вершин окна:")
        self.clip_label.pack(side=tk.LEFT, padx=5)
        
        self.clip_entry = tk.Entry(clip_frame, width=50)
        self.clip_entry.pack(side=tk.LEFT, padx=5)
        self.clip_entry.insert(0, "5,5, 750,15, 350,795")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.clip_button = tk.Button(button_frame, text="Отсечение", command=self.clip_polygon)
        self.clip_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Сохранить", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.canvas_frame = tk.Frame(self.root, width=800, height=800)
        self.canvas_frame.pack(pady=10)

    
    def clip_polygon(self):
        poly_coords = list(map(int, self.poly_entry.get().split(',')))
        clip_coords = list(map(int, self.clip_entry.get().split(',')))

        polygon = np.array(poly_coords).reshape(-1, 2)
        clipping_window = np.array(clip_coords).reshape(-1, 2)

        print("Координаты многоугольника:", polygon)
        print("Координаты окна отсечения:", clipping_window)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, 800)
        ax.set_ylim(0, 800)
        ax.set_facecolor('black')

        clip_path = Polygon(clipping_window, closed=True, fill=True, edgecolor='white', facecolor='white')
        ax.add_patch(clip_path)

        clipped_polygon = self.sutherland_hodgman(polygon, clipping_window)
        print("Отсеченный многоугольник:", clipped_polygon)
        
        if clipped_polygon.size > 0:
            poly_patch = Polygon(clipped_polygon, closed=True, color='red')
            ax.add_patch(poly_patch)

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def sutherland_hodgman(self, subjectPolygon, clipPolygon):
        def inside(p, cp1, cp2):
            return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) >= (cp2[1] - cp1[1]) * (p[0] - cp1[0])
        
        def intersection(cp1, cp2, s, e):
            dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
            dp = [s[0] - e[0], s[1] - e[1]]
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = s[0] * e[1] - s[1] * e[0]
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

        outputList = subjectPolygon
        cp1 = clipPolygon[-1]
        
        for cp2 in clipPolygon:
            print(f"Обработка ребра окна отсечения: {cp1} -> {cp2}")
            inputList = outputList
            outputList = []
            if len(inputList) == 0:
                break
            s = inputList[-1]
            
            for e in inputList:
                if inside(e, cp1, cp2):
                    if not inside(s, cp1, cp2):
                        inter = intersection(cp1, cp2, s, e)
                        print(f"Точка пересечения: {inter}")
                        outputList.append(inter)
                    outputList.append(e)
                    print(f"Точка внутри: {e}")
                elif inside(s, cp1, cp2):
                    inter = intersection(cp1, cp2, s, e)
                    print(f"Точка пересечения: {inter}")
                    outputList.append(inter)
                s = e
            cp1 = cp2
        return np.array(outputList)



    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.print_png(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonClipperApp(root)
    root.mainloop()
