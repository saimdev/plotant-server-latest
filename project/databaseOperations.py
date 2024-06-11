from .models import GraphData, Logs

def logsToGraph(**kwargs):
    graph_data = GraphData.objects.create(**kwargs)
    return True


def updateData(id, **kwargs):
    kwargs.pop('currentGraphId', None)
    for key, value in kwargs.items():
        if isinstance(value, str) and value.lower() in ['true', 'false']:
            kwargs[key] = value.lower()

    graph_data = GraphData.objects.filter(id=id).update(**kwargs)
    return True


def Graph(accessType, msg, **kwargs):
    try:
        kwargs.pop('currentGraphId', None)

        # for key, value in kwargs.items():
        #     if isinstance(value, str) and value.lower() in ['true', 'false']:
        #         kwargs[key] = value.lower()

        graph_data = GraphData.objects.create(**kwargs)
        logs_data = Logs.objects.create(accessType=accessType, message=f'{msg} Graph', graph_id=graph_data.id, **kwargs)
        return True
    except Exception as e:
        return False
    

def logsData(accessType, msg, graph_id, **kwargs):
    try:
        kwargs.pop('currentGraphId', None)
        Logs.objects.create(accessType=accessType, message=f'{msg} Graph', graph_id=graph_id, **kwargs) 
        return True
    except Exception as e:
        return False
    
# def logsStore(accessType, msg, **kwargs):
#     try:
#         kwargs.pop('currentGraphId', None)
#         Logs.objects.create(accessType=accessType, message=f'{msg} Graph',  **kwargs) 
#         return True
#     except Exception as e:
#         return False


