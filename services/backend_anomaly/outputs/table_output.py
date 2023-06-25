import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import matplotlib.path as mpath

class TableOutput:
    def __init__(self, data, session_id):
        self.contents = data
        self.session_id = session_id
        self.ids = None
    
    def make_plot(self):
        def sort_by_object_id_and_frame(file_path):
            colnames = ["time", "runtime", "Object_ID", "Frame", "cX", "cY"]
            data = file_path
            data.columns = colnames

            runtime = data["runtime"].tolist()
            frame = [0]
            count = 0
            for i in range(len(data) - 1):
                t0 = runtime[i]
                t1 = runtime[i+1]

                if t0 == t1:
                    pass
                elif t0 < t1:
                    count += 1
                frame.append(count)

            count += 1

            data["Frame"] = frame
            data.sort_values(by = ["Object_ID", "Frame"], inplace=True)

            return data
        
        def split_object_id(file_path):
            df = file_path

            columns = df.columns.values.tolist()
            columns_list = list(columns)

            indx_val = columns_list.index("Object_ID")
            column_to_split = columns[indx_val]
            unique_values = df[column_to_split].unique()

            labels = []
            df_by_object = []

            for label in unique_values:
                df_label = df[df[column_to_split] == label]
                df_label = df_label.iloc[:, 3:]
                labels.append(label)
                df_by_object.append(df_label)
            
            return labels, df_by_object

        def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
        linewidth=3, alpha=1.0):

            # Default colors equally spaced on [0,1]:
            if z is None:
                z = np.linspace(0.0, 1.0, len(x))

            # Special case if a single number:
            if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
                z = np.array([z])

            z = np.asarray(z)

            segments = make_segments(x, y)
            lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                                    linewidth=linewidth, alpha=alpha)

            ax = plt.gca()
            ax.add_collection(lc)

            return lc

        def make_segments(x, y):
            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            return segments

        def plot(file_path, i, session_id):
            data = file_path
            N = 10
            np.random.seed(101)
            x = data["cX"]
            y = data["cY"]
            frame = data["Frame"]

            fig, ax = plt.subplots()
            
            batas = len(data)
            xbegend = []
            ybegend = []
            fbegend = []
            xbeg = x[0]
            ybeg = y[0]
            xend = x[batas-1]
            yend = y[batas-1]
            
            fbeg = frame[0]
            fend = frame[batas-1]
            xbegend.append(xbeg)
            xbegend.append(xend)
            ybegend.append(ybeg)
            ybegend.append(yend)
            fbegend.append(fbeg)
            fbegend.append(fend)

            path = mpath.Path(np.column_stack([x, y]))
            verts = path.interpolated(steps=3).vertices
            x, y = verts[:, 0], verts[:, 1]

            z = np.linspace(0, 1, len(x))
            plt.scatter(x, y, color='white')
            col = plt.scatter(xbegend, ybegend, s=200, c=fbegend, cmap="plasma")
            colorline(x, y, z, cmap=plt.get_cmap('plasma'), linewidth=2)
            plt.colorbar(col, format="%d")

            plt.savefig("static/temp/{}_{}.png".format(session_id, i))
            plt.close()
            
            if len(self.contents) != 0:  
                self.ids, dataframes = split_object_id(sort_by_object_id_and_frame(self.contents))
                for i in self.ids:
                    dataframes[i] = dataframes[i].reset_index().drop(["index"], axis=1)
                    plot(dataframes[i], i, self.session_id)
                return True
            else:
                return False
    
    def get_contents(self):
        return self.contents
    
    def get_ids(self):
        return self.ids