FROM python
WORKDIR /everis_tech_test
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt && \
    chmod +x /everis_tech_test/core.py

VOLUME /everis_tech_test
CMD [ "tail","-f", "/dev/null" ] 