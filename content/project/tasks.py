import time
import csv
from celery import shared_task

@shared_task
def ingest_csv_task(file_path):
	"""Ingest a CSV file into the database"""
	from project.api.content import ingest_json_content
	data = []
	try:
		with open(file_path, "r") as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for row in csv_reader:
				data.append(row)
		# Insert JSON into database
		ingest_json_content(data)

	except Exception as e:
		raise e

@shared_task
def divide(x, y):
	"""Divide two numbers"""
	time.sleep(10)
	return x / y