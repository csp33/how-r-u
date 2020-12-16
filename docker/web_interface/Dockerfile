FROM python:3.6.10-stretch
ENV PYTHONUNBUFFERED 1
# Copy config files
ADD config/requirements.txt /root/requirements.txt
ADD config/routes.json /etc/howru/cfg/routes.json
ADD config/initial_data.json /initial_data.json
# Install dependencies
RUN pip install -r /root/requirements.txt
# iPython for debugging
RUN pip3.6 install ipython gunicorn

ENV PYTHONPATH /projects/how-r-u/web_interface
RUN mkdir /var/log/how-r-u
# Run server
 #   python3 manage.py loaddata /initial_data.json && \
    #python3 manage_web_interface.py runserver 0:8080
WORKDIR /projects/how-r-u
CMD python3 manage_web_interface.py makemigrations && \
    python3 manage_web_interface.py migrate && \
    gunicorn web_interface.core.wsgi:application --pythonpath /projects/how-r-u -c /projects/how-r-u/web_interface/gunicorn_config.py
#CMD tail -f /dev/null
