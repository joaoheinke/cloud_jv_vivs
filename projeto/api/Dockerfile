# FROM ubuntu:22.04
# #baixa a imagem
# RUN apt-get update && \ 
#     apt-get install -y net-tools iputils-ping
# #cria a layer -> e tufdo o que eu faco ex: instalar o python

# CMD ["tail", "-f", "/dev/null"] 
# #faz isso pra colocar a maquina no ar, faco ele fazer alguma coisa e parar, trava o terminal e abre o processo
# #docker cria um processo, mas tem que pedir p ele abrir porta, criar o basico

FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]