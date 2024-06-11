from project.general_operations import DataProcessor, EPS, FileProcessor
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from project import general_operations
from datetime import datetime
from .models import Working
import tempfile
import base64
import json
import os

data_processor = DataProcessor()
file_processor = FileProcessor()
eps = EPS()



@api_view(['POST'])
def analyse(request):
    if request.method == "POST":
        file = request.FILES.get('file')

        if file:
            original_filename = os.path.splitext(file.name)[0]
            if not file.name.lower().endswith('.csv'):
                return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)

            modified_filename = original_filename.replace(' ', '')
            modified_filename = f'{modified_filename}_{datetime.now().strftime("%H-%M-%S")}.csv'

            data = data_processor.save_file(modified_filename, file)
            if data['flg'] == True:
                return Response({'Error': data['locations']})
            else:
                working_record = Working(filename=modified_filename, date=datetime.now())
                working_record.save()
                guest = working_record.id 
                print(f"Guest ID: {guest}")
                guest_str = str(guest)

                return Response({
                    'data': data['head'],
                    'columns': data['column_names'],
                    'columns_data': data['column_data'],
                    'columns_unique_data': data['column_data_unique'],
                    'type': data['type'],
                    'guest': guest_str
                }, status=200)
    else:
        return Response({'error': 'Wrong Request Method'}, status=400)


@api_view(['POST'])
def labels(request):
    if request.method == 'POST':
        x = request.data.get('x_label')
        y = request.data.get('y_label')

        guest = request.data.get('guest')
        try:
            working_record = Working.objects.get(id=guest)
        except Working.DoesNotExist:
            return Response({"error": "Working record not found"}, status=404)

        filename = working_record.filename

        print('\n', x, ' , ', y, ' , ', filename, '\n')

        labels = data_processor.get_labels(x, y, filename)

        labels = json.loads(labels)
        
        print('\n',labels,'\n')
        
        return Response({
                    'x': labels['x'],
                    'y': labels['y'],
                }, status=200)
    else:
        return Response({"error":'Wrong Request Method'}, status=400)
    

@api_view(['POST'])
def labels_legends(request):
    if request.method == 'POST':
        x = request.data.get('x_label')
        y = request.data.get('y_label')
        z = request.data.get('z')

        guest = request.data.get('guest')
        try:
            working_record = Working.objects.get(id=guest)
        except Working.DoesNotExist:
            return Response({"error": "Working record not found"}, status=404)

        filename = working_record.filename

        print('\n', x,' , ', y , ' , ', z ,  ' , ',filename,'\n')

        labels = data_processor.get_labels_legends(x, y, z, filename)

        labels = json.loads(labels)
        
        print('\n',labels,'\n')
        
        return Response({
                    'x': labels['x'],
                    'y': labels['y'],
                    'z': labels['z'],
                }, status=200)
    else:
        return Response({"error":'Wrong Request Method'}, status=400)
    

@api_view(['POST'])
def edit_value(request):
    if request.method == 'POST':
        guestId = request.data.get('guestId')
        rowIndex = request.data.get('rowIndex')
        columnIndex = request.data.get('columnKey')
        value = request.data.get('value')
        xLabel = request.data.get('xLabel')
        yLabel = request.data.get('yLabel')

        # Debugging: Print the input parameters
        print(f"Parameters - guestId: {guestId}, rowIndex: {rowIndex}, columnIndex: {columnIndex}, value: {value}, xLabel: {xLabel}, yLabel: {yLabel}")

        try:
            working_record = Working.objects.get(id=guestId)
        except Working.DoesNotExist:
            return Response({"error": "Working record not found"}, status=404)
        
        result = file_processor.edit_val(columnIndex, rowIndex, value, working_record.filename, xLabel, yLabel)

        if result == False:
            print(f'\n{guestId} - {rowIndex} - {columnIndex} - {value} - {xLabel} - {yLabel} - {working_record.filename}')
            return Response({"message": 'Value Updated successfully.'}, status=200)
    
        labels = json.loads(result)
        
        return Response({
                    'x': labels['x'],
                    'y': labels['y'],
                }, status=200)
    else:
         return Response({"error": 'Wrong Request Method'}, status=400)


@api_view(['POST'])
def convertEPS(request):
    try:
        if request.method == 'POST':
            if 'file' in request.FILES:
                image = request.FILES['file']
                result = eps.main(image)
                eps_data = base64.b64decode(result)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.eps') as temp_file:
                    temp_file.write(eps_data)
                    temp_file.flush()
                
                response = FileResponse(open(temp_file.name, 'rb'), content_type='application/postscript')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(temp_file.name)}"'
                return response
            else:
                return Response({"error": 'No file provided in the request'}, status=400)
        else:
            return Response({"error": 'Invalid request method'}, status=400)
    except Exception as e:
        return Response({"error": 'An error occurred while processing the file'}, status=500)