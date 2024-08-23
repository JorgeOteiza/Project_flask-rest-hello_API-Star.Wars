import sys
import os
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from src.app import app  # Asegúrate de que la ruta de importación sea correcta
from src.models import db  # Asegúrate de que la ruta de importación sea correcta

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Crear el contexto de la aplicación
with app.app_context():
    # Crear el gráfico utilizando los metadatos de los modelos de SQLAlchemy
    graph = create_schema_graph(metadata=db.metadata,
                                engine=db.engine,  # Se agrega el engine necesario
                                show_datatypes=True,  # Mostrar tipos de datos
                                show_indexes=True,  # Mostrar índices
                                rankdir='LR',  # De izquierda a derecha
                                concentrate=False  # No unir los bordes juntos
                                )

    # Guardar el gráfico en un archivo
    graph.write_jpg('schema_diagram.jpg')