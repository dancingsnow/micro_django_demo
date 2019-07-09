FROM python:3.6

ENV LANG=C.UTF-8

COPY . /work
WORKDIR /work

VOLUME /work/static

RUN pip install --upgrade pip && pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN cp prod_entrypoint.sh /usr/bin/ && chmod +x /usr/bin/prod_entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["prod_entrypoint.sh"]

CMD ["micro-django-start"]