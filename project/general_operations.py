from io import StringIO
from io import BytesIO
from PIL import Image
import pandas as pd
import base64
import json
import os

main_storage = "Storage"
user_storage = "Users_Storage"

class DataProcessor:
    def __init__(self):
        self.file_path = None

    def get_column_names(self, data):
        column_names = []
        for column in data.columns:
            column_names.append(column)
        return json.dumps(column_names)

    def get_column_data(self, col, data):
        column_data = []
        for column in data[col]:
            column_data.append(column)
        return json.dumps(column_data)
    
    def get_column_data_unique(self, col, data):
        unique_values = data[col].unique().tolist()
        return json.dumps(unique_values)

    def get_column_unique_data(self, data):
        column_data_unique = {}
        for col in data.columns:
            unique_values = data[col].unique().tolist()
            column_data_unique[col] = unique_values
        return json.dumps(column_data_unique)

    def get_only_int_float_column_names(self, column_data):
        only_int_float_column_names = []
        for col, values in column_data.items():
            if all(isinstance(v, (int, float)) for v in values):
                only_int_float_column_names.append(col)
        return json.dumps(only_int_float_column_names)
    
    def get_sum_of_int_and_float_columns(self, data):
        int_float_columns = [col for col in data.columns if data[col].dtype in ('int64', 'float64')]
        sum_dict = {col: data[col].sum() for col in int_float_columns}
        json_sum_of_int_and_float_columns = json.dumps(sum_dict)
        return json_sum_of_int_and_float_columns

    def legends(self, x, y, z, data):
        flg = False
        unique_x_values = data[x].unique().tolist()
        y_values_with_respect_to_unique_x_values = []
        y_values_with_respect_to_unique_z_values = {}

        for product in unique_x_values:
            product_data = data[data[x] == product]
            if product_data[y].dtype != 'object':   
                product_quantity_sum = product_data[y].sum()
                y_values_with_respect_to_unique_x_values.append(round(float(product_quantity_sum),  1))
                
                z_grouped_data = product_data.groupby(z)[y].sum().to_dict()  # Change count to sum
                y_values_with_respect_to_unique_z_values[product] = z_grouped_data
            else:
                flg = True
                y_counts = product_data[y].value_counts().to_dict()
                y_values_with_respect_to_unique_x_values.append(y_counts)

                z_grouped_data = product_data.groupby(z)[y].apply(list).to_dict()  # Store corresponding values as lists
                y_values_with_respect_to_unique_z_values[product] = z_grouped_data

        if flg == True:
            final_list = []

            for entry in y_values_with_respect_to_unique_x_values:
                sum =  0
                for key, value in entry.items():
                    sum = sum + value
                final_list.append(sum)
            y_values_with_respect_to_unique_x_values = final_list

        return {'x': unique_x_values, 'y': y_values_with_respect_to_unique_x_values, 'z': y_values_with_respect_to_unique_z_values}

    def x_y_data(self, x, y, data):
        flg = False
        unique_x_values = data[x].unique().tolist()
        y_values_with_respect_to_unique_x_values = []

        for product in unique_x_values:
            product_data = data[data[x] == product]
            if product_data[y].dtype != 'object': 
                product_quantity_sum = product_data[y].sum()
                y_values_with_respect_to_unique_x_values.append(round(float(product_quantity_sum), 1))
            else:
                flg = True
                y_counts = product_data[y].value_counts().to_dict()
                y_values_with_respect_to_unique_x_values.append(y_counts)
        if flg == True:
            final_list = []

            for entry in y_values_with_respect_to_unique_x_values:
                sum = 0
                for key, value in entry.items():
                    sum = sum + value
                final_list.append(sum)
            y_values_with_respect_to_unique_x_values = final_list

        return {'x': unique_x_values, 'y': y_values_with_respect_to_unique_x_values}
  
    def save_file(self, file_name, file):
        # try:
            visitor_folder = os.path.join(main_storage, 'Visitor_Storage')
            csv_file_path = os.path.join(visitor_folder, file_name)
            data = pd.read_csv(StringIO(file.read().decode()))
            has_nan = data.isnull().values.any()
            locations = {'rows': [], 'cols': []}
            corrupt_file = []

            if has_nan:
                nan_locations = pd.DataFrame(data.isnull(), columns=data.columns).stack()
                for idx in nan_locations[nan_locations].index:
                    row_number, col_name = idx
                    locations['rows'].append(row_number+1)
                    locations['cols'].append(col_name.split(' ')[1])
                corrupt_file.append(True)
                return {'flg':True, 'locations':f'some cells are empty try fill them or remove them locations are: {locations}'}
            else:
            
                with open(csv_file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
            
            data = pd.read_csv(csv_file_path)

            json_data = data.to_json(orient='records')
            parsed_json_data = json.loads(json_data)

            head = data.head(5)
            json_head = head.to_json(orient='records')
            parsed_json_head = json.loads(json_head)

            column_names = data.columns.tolist()
            column_data = {}
            for col in column_names:
                column_data[col] = data[col].tolist()

            column_dataJ = json.dumps(column_data)
           

            result_data = {
                'flg':False,
                'json_data': parsed_json_head,
                'head': parsed_json_data,
                'column_names': json.loads(self.get_column_names(data)),
                'column_data': json.loads(column_dataJ),
                'column_data_unique': json.loads(self.get_column_unique_data(data)),
                # 'sum': json.loads(self.get_sum_of_int_and_float_columns(data)),
                'type': json.loads(self.get_only_int_float_column_names(column_data)),
            }
            return result_data

    def get_labels(self, x, y,guest):
        main_folder = os.path.join(main_storage, 'Visitor_Storage')
        data = ""
        if os.path.exists(main_folder):
            for file in os.listdir(main_folder):
                if file == guest:
                    data = pd.read_csv(os.path.join(main_folder, file))
                    int_columns = data.select_dtypes(include='int').columns
        # data[int_columns] = data[int_columns].astype(float)
        result = self.x_y_data(x, y, data)
        
        return json.dumps(result)
    
    def get_labels_legends(self, x, y, z,guest):
        main_folder = os.path.join(main_storage, 'Visitor_Storage')
        if os.path.exists(main_folder):
            for file in os.listdir(main_folder):
                if file == guest:
                    data = pd.read_csv(os.path.join(main_folder, file))
        int_columns = data.select_dtypes(include='int').columns
        # data[int_columns] = data[int_columns].astype(float)
        result = self.legends(x, y, z, data)
        
        return json.dumps(result)
    

data_processor = DataProcessor()
class FileProcessor:
    def save_file(self, filepath, data):
        data.to_csv(filepath, index=False)

    def update(self, data, col, row_no, value):
        if pd.api.types.is_integer_dtype(data[col]):
            value = int(value)
        elif pd.api.types.is_float_dtype(data[col]):
            value = float(value)
        elif pd.api.types.is_string_dtype(data[col]):
            value = str(value)
            
        data.loc[row_no, col] = value
        return data
        
    def edit_val(self, col, row_no, value, guest, x, y):
        main_folder = os.path.join(main_storage, 'Visitor_Storage')

        if os.path.exists(main_folder):
            for file in os.listdir(main_folder):
                if file == guest:
                    filepath = os.path.join(main_folder, file)
                    filename_without_extension, _ = os.path.splitext(file)
                    data = pd.read_csv(filepath)

                    updated_data = self.update(data, col, row_no, value)

                    new_file_path = os.path.join(main_folder, f'{filename_without_extension}_updated.csv')

                    updated_data.to_csv(new_file_path, index=False)

                    if os.path.exists(filepath):
                        os.remove(filepath)

                    os.rename(new_file_path, filepath)
                    if x != '':
                        labels = data_processor.get_labels(x, y, guest)

                        return labels
                    return False




class EPS:
    def __init__(self, png_dir=os.getcwd()):
        self.png_dir = png_dir
        self.eps_dir = os.path.join(self.png_dir, "converted")
        os.makedirs(self.eps_dir, exist_ok=True)

    def remove_transparency(self, im, bg_color=(255,   255,   255)):
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            alpha = im.convert('RGBA').split()[-1]

            bg = Image.new("RGBA", im.size, bg_color + (255,))
            bg.paste(im, mask=alpha)
            return bg
        else:
            return im

    def convert(self, img):
        im = Image.open(img)
        if im.mode in ('RGBA', 'LA'):
            im = self.remove_transparency(im)
            im = im.convert('RGB')
        name = os.path.splitext(img.name)[0]
        byte_stream = BytesIO()
        im.save(byte_stream, format='EPS', lossless=False)
        byte_stream.seek(0)
        save_dir = 'converted'
        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        file_path = os.path.join(save_dir, f"{name}.eps")
        
        with open(file_path, 'wb') as f:
            f.write(byte_stream.getvalue())
        
       
        base64_image = base64.b64encode(byte_stream.getvalue()).decode('utf-8')
        
        return base64_image

    def main(self, img):
        print("Converting png to eps...")
        out = self.convert(img)
        return out

