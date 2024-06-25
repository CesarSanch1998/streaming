from fastapi import FastAPI, Response, Header
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from os import getcwd, path
from db.connection import *
from models.movies import movies
from os import getcwd
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:49229",
    "http://127.0.0.1",
    "http://127.0.0.1:49229",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "10.7.110.233:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # O especifica los métodos que necesitas
    allow_headers=["*"],
)

# @app.get("/video/{video_id}")
# def get_video(video_id: str, request: Request):
#     video_path = f"videos/{video_id}.mp4"  # Ajusta la ruta

#     with open(video_path, "rb") as video:
#         file_size = video.seek(0, 2)  # Obtener el tamaño del archivo

#         # Analizar el encabezado Range (si existe)
#         range_header = request.headers.get("Range")
#         start = 0
#         end = file_size - 1
#         if range_header:
#             range_values = range_header.replace("bytes=", "").split("-")
#             if range_values[0]:  # Verificar si hay valor inicial
#                 start = int(range_values[0])
#             if range_values[1]:  # Verificar si hay valor final
#                 end = int(range_values[1])

#         # Limitar el final si excede el tamaño del archivo
#         end = min(end, file_size - 1)

#         # Leer los bytes solicitados
#         video.seek(start)
#         chunk_size = end - start + 1
#         bytes_to_read = video.read(chunk_size)

#         # Enviar la respuesta
#         headers = {
#             "Content-Range": f"bytes {start}-{end}/{file_size}",
#             "Accept-Ranges": "bytes"
#         }
#         return Response(content=bytes_to_read, status_code=206, headers=headers, media_type="video/mp4")

from fastapi import FastAPI, Header, Response
from os import path, getcwd
from typing import Optional

PORTION_SIZE = 1024 * 1024 * 5  # Tamaño de fragmento: 5 MB
current_directory = getcwd() + "\\videos\\"

app = FastAPI()

@app.get("/video/{name_video}")
def get_video(name_video: str, range: Optional[str] = Header(None)):
    video_path = path.join(current_directory, name_video)  # Uso de os.path.join

    try:
        with open(video_path, "rb") as myfile:
            file_size = path.getsize(video_path)

            if range:
                start, end = range.replace("bytes=", "").split("-")
                start = int(start)
                end = int(end) if end else start + PORTION_SIZE - 1  # Manejo de '-final'
            else:  # Si no hay Range, enviar todo el video
                start = 0
                end = file_size - 1

            # Asegurar que el rango sea válido
            end = min(end, file_size - 1)

            myfile.seek(start)
            data = myfile.read(end - start + 1)  # Corrección en la lectura

            headers = {
                'Content-Range': f'bytes {start}-{end}/{file_size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(len(data))  # Agregar Content-Length
            }
            return Response(content=data, status_code=206, headers=headers, media_type="video/mp4")

    except FileNotFoundError:
        return {"error": "El archivo de video no se encontró"}


@app.get("/images/{image_name}")
def get_image(image_name: str):
    image_path = getcwd() + "/images/" + image_name # Ajusta la ruta
    return FileResponse(image_path, media_type="image/png")  # O el tipo MIME adecuado


@app.get("/all-videos")
def get_image():
    try:
        returned = session.query(movies).all()
        if returned == None:
            return "Plan no existe en la DB"
        else:
            print("returned")
        return returned
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()
    return "" # O el tipo MIME adecuado