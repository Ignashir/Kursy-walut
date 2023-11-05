FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFERED 1
WORKDIR ./webapp
COPY Pipfile Pipfile.lock /webapp/
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
# TODO: [DEV-KONSULTACJE] chciałbym zeby wytlumaczyl mi Pan jak utworzyc wkhtmltopdf w kontenerze zeby moc z niego korzystac
# TODO: narazie sie poddaje i zrobie pdf-y przy uzyciu innej biblioteki, ale ta ktorą sobie odpuściłem jest znacznie lepsza bo
# TODO: daje mozliwosc przerabiania html-a
#RUN apt-get update
#RUN apt-get install -y xz-utils libxext6 fontconfig libxrender1
#RUN curl "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.focal_arm64.deb" > wkhtmltox.tar.xz && \
#    tar --directory=/usr/local --strip 1 -xJf wkhtmltox.tar.xz && \
#    apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old wkhtmltox.tar.xz
#ENTRYPOINT ["wkhtmltopdf"]

COPY . /webapp/