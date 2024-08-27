FROM python

COPY . .

RUN  pip install --no-cache-dir -r requirements.txt

RUN playwright install-deps

RUN playwright install chromium

EXPOSE 5000
